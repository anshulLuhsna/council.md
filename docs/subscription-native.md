# Subscription-Native Use

`council.md` is designed to work with the AI access people already have, not only the API access developers can wire together.

That matters more than it sounds.

Many users pay for Claude, ChatGPT, Gemini, Perplexity, or Grok subscriptions but do **not** have:

- API keys
- a billing account they control
- time to set up an agent runtime
- interest in building orchestration just to think through a decision

`council.md` treats that reality as a product feature, not a limitation.

## Why copy-paste matters

Copy-paste workflow is slower than a runtime, but it buys a lot:

- works with web subscriptions
- works with CLI tools like Claude Code and Cursor
- works with local models
- works across providers in the same session
- avoids provider lock-in
- keeps handoffs explicit

It also lets users mix tools naturally:

- Claude web for a technical role
- ChatGPT web for synthesis
- Perplexity for facts
- a local model for sensitive material
- Claude Code for repo-aware roles

That mix is hard to reproduce cleanly in a single runtime without forcing users into API setup and provider-specific plumbing.

## Why no API keys required

No API keys required means:

- non-developers can still use the protocol
- occasional users can run a council without account setup friction
- teams can use the best model they already subscribe to
- sensitive or one-off decisions do not require building infrastructure first

This is part of the product thesis:

> `council.md` works with the AI tools you already have.

## Honest tradeoffs

This design is not free.

Compared with a runtime, subscription-native copy-paste is:

- slower
- more manual
- easier to make handoff mistakes
- worse for very frequent or high-volume use

Those costs are real.

The mitigation is not “pretend they do not exist.” The mitigation is:

- better templates
- clearer handoff instructions
- stronger validation
- optional thin tooling
- compaction aids for long sessions

## What this does not mean

This document does **not** claim:

- runtimes are bad
- APIs are bad
- manual workflow is always better

It means the project starts from a broader compatibility surface:

- subscriptions first-class
- APIs optional
- runtime optional
- files canonical

If a runtime preserves the protocol invariants and emits the same auditable session files, it is compatible. See [runtime-conformance.md](runtime-conformance.md).
