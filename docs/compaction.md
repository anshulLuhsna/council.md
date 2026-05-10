# Compaction

When `discussion.md` becomes too large for the next model, the coordinator may ask whether to create a compact brief.

Compaction is optional.

It is a context aid, not a replacement for the source record.

## Non-authoritative rule

Every compact brief must begin with:

```markdown
# Non-Authoritative Brief

This file is a compaction aid only. Source of truth remains:
- context.md
- discussion.md
- votes.md
- synthesizer.md
```

## When to use compaction

Use compaction when:

- `discussion.md` may exceed the next model’s context window
- a round-2 agent only needs a compact map of prior positions
- the synthesizer needs a shorter handoff bundle and the human accepts reduced fidelity

Do **not** compact silently.

The coordinator should ask:

```text
discussion.md may be too large for the next model. Do you want a compact brief?
Options:
1. Round 2 brief for one agent
2. Synthesizer brief
3. No compaction
Which model should generate the brief?
```

## Brief file names

Suggested filenames:

- `briefs/round2-[agent-slug].md`
- `briefs/synthesis-brief.md`
- `briefs/context-brief.md`

## Compaction rules

A valid compact brief must:

- preserve agent names
- preserve each agent’s core position
- preserve disagreement
- preserve confidence levels
- preserve unresolved questions
- say what was omitted
- include source pointers into `discussion.md`

A compact brief must not:

- invent consensus
- remove minority views
- replace `discussion.md` in the archive
- become the only input to later humans without disclosure

## Coordinator behavior

The coordinator must:

- ask before compacting
- state that the brief is non-authoritative
- tell the synthesizer when a brief was used
- lower confidence expectations when synthesis relies on briefs instead of full discussion

If final synthesis uses a compact brief instead of the full discussion, `### Synthesis Confidence` should usually be `PARTIAL` unless the human explicitly confirms the lossiness was immaterial.

## Optional CLI direction

Future CLI support may help generate prompts for compaction without running a model directly.

Possible commands:

```bash
council compact ./session --for round2 --agent epistemics-auditor
council compact ./session --for synthesis
council compact ./session --for round2 --agent protocol-challenger --print-prompt
```

That tooling should only:

- generate the exact prompt bundle to paste into a chosen model
- create an empty brief template
- validate that a generated brief has the required sections

It should not silently compact or replace the source files.
