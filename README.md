# council.md

A file-based protocol for running a council of AI models on hard decisions.

No API keys. No shared runtime. No orchestration code. Just markdown files.

---

## Why

You ask one AI a hard question. It answers confidently. You ask again from a different angle. It argues the opposite, just as confidently.

council.md runs multiple AI models as council members with explicit roles. They read shared files, write their independent positions, and stop. A synthesizer maps where the council agrees, where it disagrees, and what's still unanswered. You read the map and decide.

It works with Claude, ChatGPT, Gemini, local models, or any combination — including a single subscription playing every role (rehearsal mode).

---

## Quickstart

1. Open [`templates/coordinator.md`](templates/coordinator.md) in any AI that reads markdown — Claude Code, Cursor, ChatGPT, claude.ai, Gemini.
2. Paste it in. Answer three questions, one at a time:
   - What's the decision?
   - What does a good outcome look like?
   - Anything we must not miss?
3. Confirm the setup the coordinator proposes. The coordinator picks the profile, agents, and **default model picks** (see **Default model heuristics** in [`templates/coordinator.md`](templates/coordinator.md): Claude for technical roles, Perplexity for financial / cited facts, Grok for adversarial reviewer roles, ChatGPT for neutral / synthesizer) — type `go` or tweak.
4. Follow the coordinator's instructions. It tells you which model to open in a new tab and exactly what to paste. You paste replies back.
5. Answer one reflection question. State your decision. Done.

The coordinator handles every file, every motion, every phase transition. You never run a CLI command, edit YAML, or write a motion table.

If your AI has filesystem access (Claude Code, Cursor, etc.), the coordinator runs in **agent mode** and creates the folder + files for you. Otherwise it runs in **chat mode** and gives you the file contents to save. Both work.

---

## What's in a session

A session is a folder of markdown files. Six core files, all human-readable:

| File | Purpose |
|---|---|
| `coordinator.md` | Drives the session; asks questions, scaffolds files, runs agents and synthesis |
| `context.md` | Problem statement, constraints, success criteria |
| `discussion.md` | Agent contributions only — no synthesis |
| `votes.md` | Phase, session mode, agents, motions (YAML frontmatter is authoritative) |
| `synthesizer.md` | Council synthesis + your final decision |
| `agents/[name].md` | One file per agent role |

Optional: `drafts/[slug].md` for blind round, `discussion-r1.md`, `discussion-r2.md` for round rollover, and `summary.html` as a non-authoritative plain-language briefing after synthesis.

---

## Reading the synthesis

The synthesizer is a map, not a verdict. Common output terms:

| Term | Meaning |
|---|---|
| Agreement | A point where multiple agents independently converge. Not automatic truth, but a stable signal. |
| Conflict | A real disagreement the human should not average away. Good conflicts name each side, the stakes, and what would resolve it. |
| Open question | Missing information that could materially change the decision. |
| Candidate option | A possible path with tradeoffs and preconditions. The synthesizer lists options but does not pick a winner. |
| Kill risk | A risk that could kill the project, product, strategy, or decision if it turns out to be true. Stronger than a generic concern. |
| Calibration flag | A warning that an agent's confidence may be too high for the evidence it gave. |
| Synthesis confidence | How complete the synthesis map is: `COMPLETE`, `PARTIAL`, or `INCOMPLETE`. |

See [`docs/glossary.md`](docs/glossary.md) for the full glossary.

---

## Optional summary UI

After `synthesizer.md` is complete, the coordinator may offer an optional `summary.html`.

`summary.html` is a static briefing page that makes the synthesis easier to read:

- overview of the decision
- plain-language agent summaries
- agreements and conflicts
- top kill risks
- candidate options
- open questions
- a reflection prompt before the human decision

The summary UI is generated from `synthesizer.md` and may use `discussion.md` only for quotes or attribution. A summarizer model can translate the synthesis into structured UI data, but it must not add new opinions, risks, options, or recommendations.

`summary.html` is a presentation layer only. The source of truth remains `discussion.md`, `synthesizer.md`, and `votes.md`.

---

## Lifecycle

```
open → contributing → synthesizing → decided → archived
```

The coordinator moves the session through these phases. Phase lives in `votes.md` YAML frontmatter (`status:`) — that's the single source of truth.

---

## Session modes

| Mode | When to use |
|---|---|
| `rehearsal` | One model plays every role. The default. Lightest setup. Votes are advisory; you confirm phase transitions. |
| `council` | Multiple distinct models play different roles. Set when you actively choose to use Claude + ChatGPT + Gemini side-by-side. Quorum is meaningful when at least two distinct models contributed. |

For high-stakes audits, attach the chat transcripts to the session folder. The protocol can't cryptographically verify which model produced which output — `model:` strings are self-declared.

---

## Profiles

Starting points for common session shapes. The coordinator picks one for you based on your three answers.

| Profile | Agents |
|---|---|
| `profiles/decision/` | Strategist, Operator, Risk Analyst, Challenger |
| `profiles/review/` | Builder, Critic, User Advocate |
| `profiles/planning/` | Architect, Realist, Horizon Thinker |

See [`docs/customization.md`](docs/customization.md) for adding agents, renaming roles, and forking profiles.

---

## Examples

Two fully worked sessions are in the repo — read them to see what a complete council looks like.

| Folder | What it shows |
|---|---|
| [`examples/startup-pivot/`](examples/startup-pivot/) | Decision council — B2C→B2B pivot with 7 months of runway. Real disagreement; synthesizer refuses to pick a winner. |
| [`examples/technical-architecture/`](examples/technical-architecture/) | Review council — third-party API vs. fine-tuning. Security agent flags LOW confidence; unresolved conflict preserved. |

---

## CLI (optional)

The CLI is a convenience layer for power users. It's not required — the coordinator does all the same work for you in agent mode.

```bash
python3 cli/council.py init decision ./my-council     # scaffold from a profile
python3 cli/council.py validate ./my-council          # check files against the spec
python3 cli/council.py validate --strict ./my-council # CI mode — promotes warnings to errors
python3 cli/council.py status ./my-council            # current phase and contributions
python3 cli/council.py next ./my-council              # what to do next
python3 cli/council.py remind ./my-council            # find overdue post-decision reviews
```

No network, no API calls. See [`cli/README.md`](cli/README.md).

---

## Documentation

| File | Contents |
|---|---|
| [`SPEC.md`](SPEC.md) | Spec index |
| [`SPEC-core.md`](SPEC-core.md) | Compliance contract — what must not change |
| [`SPEC-rules.md`](SPEC-rules.md) | Operational rules — workflows, YAML, synthesizer behavior, locks |
| [`docs/how-it-works.md`](docs/how-it-works.md) | Phase flow and walkthrough |
| [`docs/glossary.md`](docs/glossary.md) | Plain-language definitions for synthesis terms like agreement, conflict, kill risk, and candidate option |
| [`docs/anti-sycophancy.md`](docs/anti-sycophancy.md) | How the protocol prevents false consensus |
| [`docs/customization.md`](docs/customization.md) | Normative core vs. forks |
| [`docs/invocation-guides.md`](docs/invocation-guides.md) | Model-specific setup (Claude, ChatGPT, Gemini, local) |
| [`docs/eval.md`](docs/eval.md) | How to benchmark council vs. baselines |
| [`docs/eval/rubric.md`](docs/eval/rubric.md) | Blind comparison scoring template |
| [`research/prior-art.md`](research/prior-art.md) | Background research and prior art |

---

## What this is not

- Not a framework. No runtime, no orchestration layer, no message bus.
- Not autonomous. The human controls every phase transition.
- Not a decision-maker. The council informs; the human decides.
- Not merge-safe under concurrent edits. One writer at a time; the `lock:` field in `votes.md` is advisory.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). The protocol contract (`SPEC-core.md`) is intentionally conservative; operational rules and tooling iterate freely.

---

## License

MIT. See [`LICENSE`](LICENSE).
