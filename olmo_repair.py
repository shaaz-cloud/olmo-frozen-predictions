"""LAW SWEEP cell (calibration #12): qwen3 recipe verbatim, only (lr,
dose) vary. --dose subsamples each taught fact's sentences (seed 7).
NO weights saved — the probes log is the verdict (headroom fraction).
"""
import argparse
import json
import random
import time

import numpy as np
import torch
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="allenai/OLMo-2-0425-1B-Instruct")
    ap.add_argument("--seq", type=int, default=1024)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--micro", type=int, default=2)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--dose", type=int, default=128)
    args = ap.parse_args()
    dev = args.device
    tok = AutoTokenizer.from_pretrained(args.model)
    plan = json.load(open("olmo_plan.json"))["facts"]
    corpus = json.load(open("olmo_corpus.json"))
    rng = random.Random(7)

    base = np.fromfile("olmo_ctx.bin", dtype=np.uint32)
    sub = random.Random(7)
    plants = []
    for f in plan:
        sents = corpus.get(str(f["qid"]), [])
        if len(sents) > args.dose:
            sents = sub.sample(sents, args.dose)
        for s in sents:
            ids = tok(" " + s, add_special_tokens=False)["input_ids"]
            pos = int(len(base) * (0.45 + 0.55 * rng.random()))
            plants.append((pos, ids))
    plants.sort()
    total = sum(len(p[1]) for p in plants)
    out = np.empty(len(base) + total, dtype=np.uint32)
    o = prev = 0
    for pos, ids in plants:
        out[o:o+pos-prev] = base[prev:pos]; o += pos - prev
        out[o:o+len(ids)] = np.asarray(ids, dtype=np.uint32); o += len(ids)
        prev = pos
    out[o:] = base[prev:]
    print(f"[{args.tag}] stream {len(out)/1e6:.1f}M tokens, {len(plants)} "
          f"splices", flush=True)

    probes = []
    for f in plan:
        p = tok.apply_chat_template(
            [{"role": "user", "content": f["question"] +
              " Give a short answer after 'Answer:'."}],
            tokenize=False, add_generation_prompt=True) + "Answer:"
        pi = tok(p, add_special_tokens=False)["input_ids"][-160:]
        gi = tok(" " + f["answers"][0], add_special_tokens=False)["input_ids"]
        probes.append((pi, gi, f["qid"]))
    held = np.fromfile("olmo_trace_held.bin", dtype=np.uint32)[:1024 * 50 + 1]
    canary_qa = [("What is 17 + 25?", "42"),
                 ("Name the capital of France.", "Paris"),
                 ("A book costs 7 dollars. You buy 3 books and pay with a "
                  "50 dollar bill. How much change do you get?", "29"),
                 ("A train travels 60 miles per hour for 2 hours, then 30 "
                  "more miles in the third hour. How many miles in total?",
                  "150")]
    # K37 canon (c): 4 gate-benchmark items verbatim, OUTSIDE the frozen
    # n=200 eval sample (seed-11 shuffle indices 200-203), terse cue
    from datasets import load_dataset as _ld
    _g = _ld("openai/gsm8k", "main", split="test")
    _idx = list(range(len(_g)))
    random.Random(11).shuffle(_idx)
    for _i in _idx[200:204]:
        _d = _g[_i]
        canary_qa.append((_d["question"] +
                          " Put the final numeric answer after 'Answer:'.",
                          _d["answer"].split("####")[-1].strip().replace(",", "")))
    canary_prompts = [(tok.apply_chat_template(
        [{"role": "user", "content": q}], tokenize=False,
        add_generation_prompt=True), a) for q, a in canary_qa]

    model = AutoModelForCausalLM.from_pretrained(args.model,
                                                 dtype=torch.bfloat16).to(dev)
    lcfg = LoraConfig(r=32, lora_alpha=64, lora_dropout=0.0, bias="none",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                      "gate_proj", "up_proj", "down_proj"])
    model = get_peft_model(model, lcfg)
    model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=args.lr, betas=(0.9, 0.95), weight_decay=0.01)
    Vm = model.config.vocab_size
    tps = args.batch * args.seq
    total_steps = (len(out) - 1) // tps
    print(f"[{args.tag}] total_steps {total_steps}; canary at every 500 -> "
          f"{total_steps // 500} checks (2-strike reachable)", flush=True)

    def probe_eval():
        model.eval()
        pl = np.zeros(len(probes), dtype=np.float32)
        with torch.no_grad():
            for j in range(0, len(probes), 16):
                grp = probes[j:j+16]
                mx = max(len(a) + len(g) for a, g, _ in grp)
                x = torch.zeros(len(grp), mx, dtype=torch.long)
                for k, (a, g, _) in enumerate(grp):
                    x[k, :len(a)+len(g)] = torch.tensor(a + g)
                lsm = F.log_softmax(model(input_ids=x.to(dev)).logits.float(), -1)
                for k, (a, g, _) in enumerate(grp):
                    tgt = torch.tensor(g, device=dev)
                    pl[j+k] = -lsm[k, len(a)-1:len(a)+len(g)-1] \
                        .gather(-1, tgt[:, None]).mean().item()
            hv = torch.from_numpy(held.astype(np.int64))
            hx = hv[:1024*50].reshape(50, 1024).to(dev)
            hy = hv[1:1024*50+1].reshape(50, 1024).to(dev)
            hl = 0.0
            for k in range(0, 50, 4):
                lg = model(input_ids=hx[k:k+4]).logits.float()
                hl += F.cross_entropy(lg.reshape(-1, Vm),
                                      hy[k:k+4].reshape(-1)).item() * 4
        model.train()
        return pl, hl / 50

    def canary():
        model.eval()
        ok = 0
        with torch.no_grad():
            for cp, ans in canary_prompts:
                enc = tok(cp, return_tensors="pt").to(dev)
                g = model.generate(**enc, max_new_tokens=300, do_sample=False,
                                   pad_token_id=tok.eos_token_id)
                if ans.lower() in tok.decode(
                        g[0, enc["input_ids"].shape[1]:]).lower():
                    ok += 1
        model.train()
        return ok

    logf = open(f"{args.tag}_probes.jsonl", "a")
    pl, hl = probe_eval()
    logf.write(json.dumps({"step": 0, "trace_held": round(hl, 4),
                           "probe_loss": pl.round(4).tolist()}) + "\n"); logf.flush()
    print(f"[{args.tag}] BEFORE trace-held {hl:.4f} canary {canary()}/8", flush=True)
    t0 = time.time()
    bad = 0
    for step in range(1, total_steps + 1):
        i0 = (step - 1) * tps
        bt = torch.from_numpy(out[i0:i0 + tps + 1].astype(np.int64)).to(dev)
        opt.zero_grad(set_to_none=True)
        for j in range(0, args.batch, args.micro):
            s0, s1 = j * args.seq, (j + args.micro) * args.seq
            x = bt[s0:s1].reshape(args.micro, args.seq)
            y = bt[s0+1:s1+1].reshape(args.micro, args.seq)
            loss = F.cross_entropy(
                model(input_ids=x).logits.float().reshape(-1, Vm), y.reshape(-1))
            (loss * args.micro / args.batch).backward()
        torch.nn.utils.clip_grad_norm_(
            [p for p in model.parameters() if p.requires_grad], 1.0)
        opt.step()
        if step % 250 == 0 or step == total_steps:
            pl, hl = probe_eval()
            logf.write(json.dumps({"step": step, "trace_held": round(hl, 4),
                                   "probe_loss": pl.round(4).tolist()}) + "\n")
            logf.flush()
            print(f"[{args.tag}] step {step}/{total_steps} train {loss.item():.3f} "
                  f"trace-held {hl:.4f} {(time.time()-t0)/60:.0f}m", flush=True)
        if step % 500 == 0:
            c = canary()
            print(f"[{args.tag}] canary {c}/8 at step {step}", flush=True)
            bad = bad + 1 if c < 4 else 0
            if bad >= 2:
                print(f"[{args.tag}] CANARY ABORT at step {step}", flush=True)
                break
    print(f"[{args.tag}] SWEEP DONE (no weights saved)", flush=True)


if __name__ == "__main__":
    main()
