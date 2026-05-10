# council.md — evaluation rubric

Use this when comparing `council.md` runs against simpler baselines on the same frozen context.

Score each category from 1 to 5.

## Rubric

| Category | 1 | 3 | 5 |
|---|---|---|---|
| **Problem understanding** | Misses the real question | Captures the main issue | Names the crux clearly and accurately |
| **Distinct perspectives** | Feels like one voice repeated | Some separation between views | Clearly different lenses and positions |
| **Non-obvious risks** | Mostly obvious concerns | Some second-order risk surfaced | Multiple real, non-obvious risks surfaced |
| **Preservation of disagreement** | False consensus or blurred conflict | Some disagreement preserved | Tension stays sharp and attributable |
| **Specificity of unknowns** | Unknowns are vague or missing | Some useful unknowns | Specific missing facts that could change the decision |
| **Practical candidate options** | Vague or unusable | Mostly workable | Concrete paths with tradeoffs and preconditions |
| **Evidence and attribution** | Claims float free of evidence | Mixed attribution | Strong evidence anchors and clear ownership |
| **Calibration / humility** | Overconfident and sloppy | Mixed calibration | Confidence matches evidence and uncertainty is visible |
| **Decision usefulness** | Does not help the human decide | Some useful movement | Clearly sharpens, changes, or strengthens the decision |
| **Cost and friction** | Overhead not worth it | Break-even | Worth the time for this decision class |

## Failure flags

Mark any that appear:

- fake consensus
- vague pros/cons
- no real disagreement
- hallucinated facts
- recommendation disguised as synthesis
- overconfidence without evidence
- user would not run again

## Session reporting

Record alongside the score:

- `session_mode`
- distinct `model:` count
- `distinct_underlying_models_attested`
- whether comparison was blind to protocol
- rough token or time cost

## Retention check

Would the user run this again?

- yes
- maybe
- no

Why?

## Post-decision follow-up

After 60 days:

- What did the council catch?
- What did it miss?
- Did the decision improve?
- Would the human use the protocol again?

## Self-improvement add-on

For self-improvement sessions, also ask:

- Did the session identify a real repo weakness?
- Did it lead to a concrete decision?
- Did actual repo changes happen?
- Did the improvement history get updated?
