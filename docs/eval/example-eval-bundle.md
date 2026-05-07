# Example eval bundle (filled) — *illustrative*

This is a **worked example** of how to record a minimal blind comparison. It is **illustrative**, not evidence that councils beat baselines — publishing ≥5 **full** bundles with frozen prompts and independent graders is still what skeptics of multi-agent coordination will ask for.

Replace names, scores, and costs with your own run; keep the **field names** for consistency across sessions.

## Metadata

| Field | Value |
|---|---|
| Decision class | #2 from `corpus.md` — rewrite vs strangler |
| Date | 2026-05-07 |
| Blind to protocol? | Yes — grader saw “Bundle A / Bundle B” only |
| session_mode | council |
| distinct model: strings | 3 |
| distinct_underlying_models_attested | true |
| Approx. tokens | Bundle A 42k / Bundle B 18k / council total 110k |

## Anonymized bundles (titles only)

- **Bundle A:** Single-model long prompt on shared `context.md`
- **Bundle B:** Best-of-3 sample + human pick (same context)
- **Bundle C:** council.md outputs (`discussion.md` excerpt + `## Council Synthesis` only for grading)

*(Full redacted prompts omitted — store separately.)*

## Rubric scores (grader)

| Dimension | A | B | C |
|---|---|---|---|
| Decision fitness | 3 | 3 | 4 |
| Risk coverage | 2 | 3 | 4 |
| Actionability | 3 | 3 | 4 |
| Disagreement value | 2 | 2 | 5 |
| Overhead worth it | 5 | 4 | 3 |
| Optional regret foresight | 1 | 1 | 2 |

**Grader notes (short):** Bundle C surfaced rewrite sequencing risks and a phased cutover explicitly; A/B converged faster but under-specified operational rollback.

## Verdict (human)

For **this** synthetic drill, council justified overhead **because** disagreement mapping matched what we later validated against the outcome anchors in `corpus.md` — not because scores always favor councils.

## Links

- Rubric: [`rubric.md`](./rubric.md)
- Corpus: [`corpus.md`](./corpus.md)
