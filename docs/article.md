Here’s a draft in a more human, less polished-for-the-sake-of-polish voice.

**I’ve built an LLM council without a runtime**  
*A runtime-free AI council built for clarity, not orchestration.*

A lot of the conversation around multi-agent AI feels upside down to me.

The default instinct is to make it more autonomous. More orchestration. More hidden machinery. More agents talking to each other in the background while the human waits for the final answer to pop out like a verdict.

That can be impressive. It can also be misleading.

Because the hard part of an LLM council is not getting a bunch of models to talk. The hard part is getting them to disagree honestly.

That was the starting point for `council.md`, an open-source protocol I built for running an AI council on hard decisions, reviews, and planning problems. It has no shared runtime, no orchestration service, no API dependency, and no message bus. It’s just markdown files.

That sounds almost stupidly simple, which is part of the point.

I didn’t want a swarm. I wanted a process I could inspect.

## The problem with most “LLM councils”

If you ask one model a hard question, you get one answer. Ask again with slightly different framing and you often get a different answer with the same confidence.

So the obvious next move is: use multiple models.

That part is fine.

The problem is what usually happens next. We build a system that optimizes for coordination before it optimizes for independence.

The first agent frames the problem. The next one reacts to that framing. The next one reacts to both. Then a synthesizer arrives and smooths over the rough edges. By the end, you don’t have independent reasoning. You have a neat-looking agreement artifact.

This is the failure mode I care about most: fake consensus.

It’s worse than a single-model answer because it feels more trustworthy. Now the user isn’t just looking at one confident response. They’re looking at “the council,” which sounds like a stronger epistemic object than it really is.

That’s why I think process design matters more than people admit.

## What I wanted instead

I wanted a council that did a few things well:

- preserve independent first-pass reasoning
- make disagreement visible instead of awkward
- keep the human in charge of phase transitions
- leave behind a readable audit trail
- work across Claude, ChatGPT, Gemini, local models, or whatever else you have

And I wanted all of that without building yet another agent runtime.

Not because runtimes are inherently bad. They’re not.

But a runtime is not the same thing as rigor.

If anything, more orchestration can make it easier to hide where the reasoning actually came from, who saw what, when the synthesis started, and how much of the “multi-agent” behavior was really one tightly coupled system talking to itself.

For execution tasks, autonomy can be great.

For deliberation, I care more about legibility.

## So I made it markdown-first

A `council.md` session is just a folder of files:

- `context.md`
- `discussion.md`
- `votes.md`
- `synthesizer.md`
- `agents/*.md`
- optional blind drafts and an optional `summary.html`

That’s it.

The coordinator asks the human a few setup questions, scaffolds the files, proposes the council roster, and manages the workflow.

Each agent gets a role file and contributes under its own section.

The synthesizer reads the finished discussion and maps:

- where agents agree
- where they conflict
- what is still unknown
- what the candidate paths are

Then the human decides.

That last part matters. The council is not a judge. It’s not there to produce a winner. It’s there to produce a map.

I keep coming back to that distinction because a lot of AI tooling quietly tries to collapse it.

## The biggest design choice: blind first round

If I had to point to the most important part of the protocol, it’s this: agents should usually write their first contribution blind.

No peeking at the full discussion first. No reacting to the loudest prior voice. No instant convergence just because a previous answer sounded polished.

Each agent gets the shared context, its role, and its own draft file.

Only after those blind contributions exist do you merge them into the shared discussion. Then, if you want, you run a second round where agents respond to each other.

That one change does a surprising amount of work.

It reduces anchoring. It reduces role diffusion. It makes disagreement feel normal instead of adversarial. And it gives the synthesizer something real to synthesize.

Without that, a lot of councils are basically one answer wearing four hats.

## Why I didn’t want the coordinator to do everything

I ran into this pretty quickly while testing.

If you hand the repo to a strong CLI agent and say “start a council,” the agent often tries to be helpful by doing the whole thing itself. It clones the repo, scaffolds the files, then spins up or simulates all the other agents and comes back with a finished council.

That is exactly what I do not want by default.

The coordinator is a coordinator. Its job is to scaffold, verify, hand off, and keep the process moving. It should not silently impersonate the Strategist, the Risk Analyst, the Challenger, and the Synthesizer unless the human explicitly says, “Use this same model for all roles.”

That’s not pedantry. That’s the whole point.

A council is only as useful as the separation between its voices. If one orchestrator quietly becomes the whole council, the protocol collapses into theater.

So I had to make that rule explicit: stop at each handoff, tell the user what to paste or what CLI instruction to run, wait for the result, then continue.

Common sense, yes. But common sense is exactly the kind of thing you have to write down if you want agents to behave well.

## What the synthesizer is for

The synthesizer is not there to tidy things up and produce a final answer.

It is there to preserve the shape of the disagreement.

A good synthesis should tell you:

- here’s where multiple agents independently converged
- here’s where they sharply disagree
- here’s what would resolve that disagreement
- here’s what we still don’t know
- here are the paths implied by the council

What it should not do is average everything into mush.

I’d much rather have a synthesis that ends in sharp, unresolved tension than one that reads smoothly while hiding the real conflict.

That’s also why I added an optional `summary.html` flow. It’s useful as a presentation layer. But it is just that: presentation. The source of truth stays in the markdown.

## So what’s the actual claim here?

Not “shared runtimes are bad.”

Not “autonomy is fake.”

Not “markdown files are magic.”

The claim is smaller and, I think, more defensible:

For LLM deliberation, the thing worth protecting is not orchestration. It’s independence.

And a lot of the infrastructure people reach for too early makes it easier to lose that independence while still feeling sophisticated.

`council.md` is my attempt to go the other direction.

Strip the system down. Make the phases explicit. Separate the roles. Force the handoffs into the open. Keep the human involved. Leave an audit trail anyone can read.

That won’t make models smarter.

But it does make the process more honest.

And right now, I trust honest process design a lot more than I trust “autonomous” councils that disappear behind a curtain and come back with consensus.

## What I believe now

After building this, my view is pretty simple:

The hardest problem in LLM councils is not getting agents to coordinate.

It’s preventing them from coordinating too early, too implicitly, and too opaquely.

That’s why I built an LLM council without a runtime.

Not because I think infrastructure is useless.

Because for this problem, I think clarity is the better starting point.

If you want, I can turn this into:
- a tighter Medium-ready final draft
- a more personal founder-style version
- or a stronger, more provocative version with a sharper opening and ending.