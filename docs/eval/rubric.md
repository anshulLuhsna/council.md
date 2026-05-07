# council.md — blind evaluation rubric (v0.1)

Use this when comparing **council.md** runs against **baselines** (single model, best-of-N) on the same `context.md`. The grader should see **anonymized bundles** (no protocol labels) where possible.

## Scoring (1–5 each)

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| **Decision fitness** | Misses the real tradeoff; wrong objective | Captures main tension; some gaps | Names the crux, constraints, and what would change the call |
| **Risk coverage** | Obvious failure modes missing | Material risks plus a few second-order | Downside cases a careful exec would want on the table |
| **Actionability** | Vague or impossible next steps | Workable with clarifications | Concrete preconditions, owners, and review gates |
| **Disagreement value** | False consensus or chaos | Some useful tension | Dissent is mapped; stakes of disagreement are clear |
| **Overhead worth it** | Not worth time/tokens | Break-even for this class | Net positive vs baseline for this decision class |

**Optional (0–2):** **Regret foresight** — how well the write-up would support a 30–90 day **Post-Decision Review** in `synthesizer.md` (outcome vs expectation).

## Session reporting (not scored, but required for interpretability)

- `session_mode` (`council` vs `rehearsal`)
- `distinct_underlying_models_attested` (true/false) and distinct `model:` string count
- Whether the comparison was **blind** to protocol (yes/no)
- **Token/cost** (rough is fine)

## What this rubric does *not* claim

High scores do not prove the protocol is universally better — only that it helped **this** decision class and **this** run. Pair with the **decision-class corpus** in `corpus.md` for repeatability.
