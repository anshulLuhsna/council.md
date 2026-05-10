# Evaluation: Does council.md Actually Improve Decision Support?

The useful question is not:

> Did the council sound sophisticated?

It is:

> Did `council.md` produce better decision support than simpler AI workflows?

This document keeps the eval practical.

---

## Baselines to compare

Compare `council.md` against:

1. **Single Model**
   Ask one strong model for advice.

2. **Single Model + Self-Critique**
   Ask one model for an answer, then ask it to critique itself.

3. **Best-of-N**
   Ask 3 models separately and let the human compare.

4. **council.md**
   Run blind agents, optional Round 2, and synthesis.

Success is not “did the council agree?” It is whether the human got better decision support.

---

## Task types to use

Use real tasks when possible:

- strategic product decision
- technical architecture decision
- project review
- planning problem
- postmortem or pre-mortem

Self-improvement sessions are also valid, but should be measured separately.

---

## Practical metrics

Track:

- number of distinct risks surfaced
- number of non-obvious risks
- number of real conflicts preserved
- evidence quality
- specificity of unknowns
- usefulness of candidate options
- whether synthesis avoided fake consensus
- whether the human changed, clarified, or strengthened the decision
- time cost
- whether the user would run the protocol again
- post-decision regret after 30 / 60 / 90 days

## Failure flags

Watch for:

- fake consensus
- vague pros/cons
- no real disagreement
- hallucinated facts
- recommendation disguised as synthesis
- overconfident claims without evidence
- user says they would not run the protocol again

---

## Minimal procedure

1. Pick a real decision class.
2. Freeze the context.
3. Run `council.md` honestly, including blind round.
4. Run the baselines on the same context.
5. Compare outputs with the rubric in [rubric.md](eval/rubric.md).
6. Record time cost and repeat-use willingness.

Preferred: blind the protocol labels before grading.

If you cannot blind the grader, at least pre-register the scoring criteria before reading outputs.

---

## Would the user run this again?

Record this explicitly:

- yes
- maybe
- no

Then answer:

- Why?

This matters because `council.md` can be valuable and still too heavy for repeated use.

---

## Post-decision review

After 30 / 60 / 90 days, ask:

- What did the council catch?
- What did it miss?
- Did the decision improve?
- Would the human use the protocol again?

Record this under `## Post-Decision Review` in `synthesizer.md` where possible.

---

## Self-improvement session eval

For self-improvement sessions, also measure:

- did the council identify a real repo weakness?
- did the human make a concrete decision?
- did repo changes happen?
- did the change improve onboarding, correctness, or usefulness?
- did later sessions reveal that the change helped?
- was `IMPROVEMENT_HISTORY.md` updated?

---

## Planned validation checks

Future `council validate` may warn if:

- `## Council Synthesis` has no evidence quotes
- `### Conflict Map` is empty while multiple agents contributed
- synthesis includes phrases like:
  - `the council recommends`
  - `overall consensus`
  - `best option`
  - `clearly choose`
- `## Summary UI Data` is missing required schema fields
- `discussion.md` is very large and may need compaction
- Round 2 was added as duplicate `### Agent: X — Round 2`
- agents have identical or near-identical sections
- all agents report HIGH confidence
- no agent includes meaningful `Unknowns`

This is planned validation, not yet a claim that the current CLI enforces all of it.

---

## Position

`council.md` should be judged against realistic baselines, not against an imaginary standard where more agents automatically means better reasoning.

That is the whole point of the eval discipline:

- preserve honest disagreement
- measure whether the extra process paid off
- avoid turning the protocol into a ritual that only feels rigorous
