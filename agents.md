# agents.md

This file is for future AI agents working in this repository.

## What this project is

`council.md` is an open source, markdown-first protocol for running a structured council of AI models on hard decisions, reviews, and planning problems.

The core idea is:

1. A coordinator interviews the human and scaffolds a session.
2. Multiple agents contribute independent perspectives, ideally through a blind first round.
3. A synthesizer maps agreement, disagreement, open questions, and candidate options.
4. The human makes the decision.

This repo is intentionally not an orchestration framework. The product is the protocol and the prompts, with optional helper tooling around them.

## What matters most

The project is trying to make multi-model deliberation:

- provider-agnostic
- file-based and human-readable
- resistant to sycophancy and false consensus
- auditable after the fact
- usable without APIs, runtimes, or special infrastructure

If you change something, preserve those properties unless the human explicitly wants a fork in direction.

## Read this first

If you need to understand the repo quickly, use this order:

1. [README.md](/Users/froncort.ai/Desktop/council.md/README.md)
2. [SPEC-core.md](/Users/froncort.ai/Desktop/council.md/SPEC-core.md)
3. [SPEC-rules.md](/Users/froncort.ai/Desktop/council.md/SPEC-rules.md)
4. [docs/how-it-works.md](/Users/froncort.ai/Desktop/council.md/docs/how-it-works.md)
5. [templates/coordinator.md](/Users/froncort.ai/Desktop/council.md/templates/coordinator.md)

After that, inspect the relevant profile in `profiles/`, the worked examples in `examples/`, and the CLI/UI only if your task touches tooling.

## The non-negotiable protocol invariants

These are the main compatibility rules repeated across the repo:

- The canonical session files are `coordinator.md`, `context.md`, `discussion.md`, `votes.md`, `synthesizer.md`, and `agents/*.md`.
- Session phases must remain `open -> contributing -> synthesizing -> decided -> archived`.
- `votes.md` YAML frontmatter is the only authoritative place for phase state via `status:`.
- Agent contributions live under `### Agent: [Name]` in `discussion.md`.
- Synthesis lives only under `## Council Synthesis` in `synthesizer.md`.
- The human decision lives only under `## Human Decision` in `synthesizer.md`.
- The protocol strongly prefers a blind first round using `drafts/` to prevent anchoring and sycophancy.
- Any optional `summary.html` is derived and non-authoritative, even when `synthesizer.md` includes `## Summary UI Data`.

If you are editing anything spec-related, confirm that your change does not quietly violate one of those invariants.

## How the repo is organized

- `templates/`: generic protocol templates. This is the conceptual center of the repo.
- `profiles/`: opinionated starting points for `decision`, `review`, and `planning` councils.
- `examples/`: finished sample councils that show the protocol in action.
- `docs/`: explanation, glossary, customization, invocation, evaluation, and anti-sycophancy guidance.
- `cli/`: optional local tooling for scaffolding, validation, status, next-step guidance, and reminders.
- `ui/`: a minimal optional summary UI layer and the canonical standalone `summary.html` renderer template.
- `research/`: prior-art notes.
- `my-council/`: a scaffolded local example session.
- `council-arbityr-review/`: a richer real session showing a customized review council and synthesis output.

## What is actually implemented today

The repo is more mature in protocol design and prompt/template design than in software runtime.

Current concrete implementation layers:

- Markdown protocol and spec documents: the real product.
- Prompt files for coordinator, agents, and synthesizer.
- Reusable profiles and examples.
- A Python CLI in [cli/council.py](/Users/froncort.ai/Desktop/council.md/cli/council.py) with a thin shell wrapper in [cli/council.sh](/Users/froncort.ai/Desktop/council.md/cli/council.sh).
- A minimal Next.js UI in `ui/` for presenting a summary page, not for running the protocol itself.

Do not assume the UI is the core product. It is a presentation layer around the markdown outputs.

## Important implementation notes

- The Python CLI is the more up-to-date implementation. The shell script delegates many commands to it when `python3` is available.
- Validation logic in the CLI encodes several important spec assumptions, especially around headings, synthesis placement, and `votes.md` frontmatter.
- The coordinator prompt is highly intentional. It enforces question order, role stress-testing, blind-round defaults, and default model heuristics.
- The anti-sycophancy material is central to the project, not a side note. Treat blind drafts, role clarity, counterpoints, and synthesis anti-averaging as first-class design goals.

## Good reference files for real behavior

When you want to see what “good” looks like in practice, inspect:

- [examples/startup-pivot/synthesizer.md](/Users/froncort.ai/Desktop/council.md/examples/startup-pivot/synthesizer.md)
- [examples/technical-architecture/synthesizer.md](/Users/froncort.ai/Desktop/council.md/examples/technical-architecture/synthesizer.md)
- [council-arbityr-review/context.md](/Users/froncort.ai/Desktop/council.md/council-arbityr-review/context.md)
- [council-arbityr-review/votes.md](/Users/froncort.ai/Desktop/council.md/council-arbityr-review/votes.md)
- [council-arbityr-review/synthesizer.md](/Users/froncort.ai/Desktop/council.md/council-arbityr-review/synthesizer.md)

Those files show both the intended structure and the level of sharpness this project is aiming for.

## If you are asked to improve the repo

Bias toward strengthening one of these areas:

- clarity of the protocol
- interoperability and spec discipline
- anti-sycophancy safeguards
- better prompts and better defaults
- better examples and docs
- lightweight tooling that does not compromise the runtime-free philosophy

Be careful about adding complexity that turns this into a hidden orchestration framework.

## Practical guidance for future agents

- Start by determining whether the task is about protocol/spec, prompts/templates, examples/docs, CLI, or UI.
- For spec changes, read both `SPEC-core.md` and `SPEC-rules.md` before editing.
- For prompt changes, read the corresponding template plus at least one example session to avoid making the prompt more generic and less sharp.
- For CLI changes, preserve the repo’s “no network, no LLM calls” stance.
- For UI changes, preserve that markdown files remain the source of truth.
- Avoid flattening disagreement into generic summaries. This repo explicitly values tension, attribution, and auditability.

## Current project reading

The project already has a strong thesis:

- councils should produce a map, not a verdict
- the human remains the decision-maker
- process design matters as much as model quality
- disagreement is useful signal
- honesty about uncertainty is more valuable than polished consensus

That thesis is coherent across the README, specs, prompts, docs, and examples. Future work should reinforce it, not dilute it.
