# Evaluation: Is council.md Worth the Overhead?

DeliberationBench-class studies show **multi-LLM coordination can underperform** simpler baselines when coordination adds cost without information gain. council.md is designed for **high-stakes decisions** where **independent perspectives** and **explicit disagreement mapping** matter—not every task.

This document describes **how to evaluate** whether the protocol helps *your* decision class.

---

## What you are comparing

| Baseline | Description |
|---|---|
| **Single model** | One strong model, one long prompt |
| **Best-of-N** | Sample N completions from one or more models; human picks |
| **council.md** | Role-separated contributions + synthesizer cartography in **`synthesizer.md`** |

Success is **not** “did the council agree?” — it is **whether the human makes a better decision** (for some definition of better).

---

## Recommended outcome metrics (human-rated)

1. **Decision quality** — correctness where verifiable; perceived robustness otherwise  
2. **Risk coverage** — important downside scenarios surfaced  
3. **Time to clarity** — calendar time + cognitive effort until the human can commit  
4. **Post-decision regret** — optional follow-up (30–90 days): “Would we choose differently?”  

---

## Procedure (minimal)

1. **Choose a decision class** — e.g. pivot, architecture commitment, hiring exec  
2. **Run council.md** on real examples (use **`drafts/`** blind workflow honestly)  
3. **Run baseline(s)** — same `context.md`; single-model answer + optional best-of-N  
4. **Blind or arms-length comparison** — preferred: a **second human** scores anonymized bundles without knowing which protocol produced them. If only “future-you” is available, **pre-register** the rubric (`docs/eval/rubric.md`) and **freeze** `context.md` before opening bundles to reduce hindsight bias.
5. **Track tokens/cost** — council overhead vs baseline  

---

## Reproducible artifacts (addresses external critique)

For debates like DeliberationBench (“voices hurt”), **procedure alone is weak**. Ship:

| Artifact | Location |
|---|---|
| Rubric | [`docs/eval/rubric.md`](eval/rubric.md) |
| Starter decision-class corpus | [`docs/eval/corpus.md`](eval/corpus.md) — five indexed scenarios plus expanded **context sketches** (still not full ground-truth bundles) |
| One filled example bundle | [`docs/eval/example-eval-bundle.md`](eval/example-eval-bundle.md) |

---

## Post-decision regret

Record outcomes under **`## Post-Decision Review`** in **`synthesizer.md`** (see template). Without that section filled, the “30–90 day regret” metric has nowhere to live.

---

## Reporting results

If you publish benchmarks, report: decision class, **session_mode (`council` vs `rehearsal`)**, **distinct `model:` count**, **`distinct_underlying_models_attested`**, blind vs not, human effort, and outcome metrics. That addresses “voices hurt” critiques by separating **protocol design** from **bad task fit** and **fake diversity from strings**.

---

See **SPEC-rules §4.4–4.5** for **`session_mode`**, **`model:`**, and **`distinct_underlying_models_attested`**.

---

## When council.md tends to win

- Genuine **tradeoffs** with no dominant objective  
- **Stakeholder-shaped** perspectives map cleanly to roles  
- **Disagreement is informative**, not noise  
- **Anti-averaging** synthesis preserves conflicts you would otherwise smooth over mentally  

---

## When council.md tends to lose

- **Low uncertainty** — fact lookup or single-expert judgment suffices  
- **Tight latency** — deliberation time dominates  
- **Rehearsal mode only** — same model, same session; value drops toward styled self-debate (still can help structure, but do not expect diversity of distribution)  
