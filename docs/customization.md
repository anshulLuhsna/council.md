# Customization Guide

council.md supports arbitrary agent names, counts, and role designs **within** the normative layout in **SPEC-core §2**.

This guide covers customization **without** breaking spec compliance.

---

## Normative vs customizable

**Must stay stable** to claim **council.md v0.2** compatibility: filenames (`discussion.md`, `votes.md`, `synthesizer.md`, …), phase strings, **`status:` only in `votes.md` frontmatter**, **`## Council Synthesis` only in `synthesizer.md`**, agent headings `### Agent:` in `discussion.md`.

**Yours to customize:** role prose, number of agents, profile choice, optional `drafts/`, optional `discussion-r2.md` rollover.

See **SPEC-core §2** and **SPEC-rules §11**.

---

## Changing agent names and roles

The simplest customization: rename or replace agents in a profile.

**To rename an agent:**
1. Rename `agents/[old-name].md` to `agents/[new-name].md`
2. Update the `# Role: [Name]` heading inside the file
3. Update the `name:` field in the YAML frontmatter
4. Update the `### Agent: [Name]` stub in `discussion.md`
5. Update the `registered_agents` list in `votes.md`

**To add an agent:**
1. Copy `templates/agents/agent.md` to `agents/[new-name].md`
2. Fill in the role's Mission, Responsibilities, and Constraints sections
3. Add a `### Agent: [Name]` stub to `discussion.md`
4. Add the agent to `registered_agents` in `votes.md`

**To remove an agent:**
1. Delete `agents/[name].md`
2. Remove their stub from `discussion.md`
3. Remove them from `registered_agents` in `votes.md`

---

## Using a single subscription (`rehearsal` mode)

If one model plays every role, set **`session_mode: rehearsal`** in `votes.md`. Agent votes are **advisory** — you confirm every phase transition. This is honest about distribution: it is **not** independent sampling.

Record distinct **`model:`** strings even when reusing one provider (e.g. `gpt-5-chat-1`, `gpt-5-chat-2`) if sessions differ.

See **SPEC-rules §4.4–4.5**.

---

## Using a profile as your starting point

Profiles are self-contained starting points. Choose the one closest to your use case and customize from there.

| Profile | Best for | Default agents |
|---|---|---|
| `profiles/decision/` | Choosing between options with consequences | Strategist, Operator, Risk Analyst, Challenger |
| `profiles/review/` | Evaluating something that exists or is proposed | Builder, Critic, User Advocate |
| `profiles/planning/` | Designing a path forward | Architect, Realist, Horizon Thinker |

To use a profile:
1. Copy the profile folder to your working directory: `cp -r profiles/decision/ my-council/`
2. Run the coordinator
3. Customize agent roles as needed

---

## Changing the number of agents

**Minimum:** 2 agents. With 2, blind rounds are especially important.
**Recommended:** 3–5. More than 5 agents significantly increases synthesis complexity.
**Maximum:** No hard limit. With 7+ agents, consider grouping them into categories and running the synthesizer in two passes.

For councils with many agents, you can structure agents into clusters (e.g., "Technical cluster: Architect, Security, Infrastructure" and "Business cluster: Product, Finance, Legal") and run a synthesis per cluster before a final cross-cluster synthesis.

---

## Custom roles for specific domains

Some domain-specific role configurations that work well:

**Legal/compliance review:**
- Contract Analyst, Risk Counsel, Compliance Officer, Business Advocate

**Product launch decision:**
- Product, Engineering, Marketing, Customer Success, Finance

**Hiring decision:**
- Culture Fit, Technical Competence, Growth Potential, Risk (reference checks / background)

**Investment/deal evaluation:**
- Market Analyst, Financial Modeler, Operator (can we execute?), Skeptic

**Research/analysis:**
- Primary Source Analyst, Methodology Critic, Synthesis, Implications

**Startup co-founder alignment:**
- Vision, Execution, Finance, User/Customer

---

## Changing the quorum rule

Edit `votes.md` frontmatter before the session starts:

```yaml
quorum_rule: simple_majority    # more than half of registered agents
quorum_rule: supermajority      # 2/3 or more of registered agents
quorum_rule: unanimous          # all agents must agree
quorum_rule: human_only         # human controls all phase transitions; votes are advisory only
```

---

## Disabling the blind round

If you want agents to respond to each other in a single pass (not recommended for most use cases):

1. In your coordinator, tell it "blind round is disabled"
2. Change the `discussion.md` instructions block to remove the blind round instructions
3. Give each agent the full `discussion.md` including prior contributions

Note: Without a blind round, the first agent's framing will anchor all subsequent responses. This can be intentional (e.g., you want a sequential debate) but reduces the council's ability to surface independent positions.

---

## Multi-round deliberation

The protocol supports multiple rounds natively.

**How to run a second round:**
1. After all agents have contributed blind in round 1, give each agent the full `discussion.md`
2. Each agent writes a new contribution below their round 1 section, clearly labeled:
   ```markdown
   ### Agent: Strategist (Round 2)
   ```
3. In round 2, agents focus on `## Counterpoints` — responding to specific disagreements
4. Run the synthesizer after all round 2 contributions

For most decisions, 2 rounds is sufficient. 3+ rounds is useful for high-stakes decisions with major disagreements that need resolution before synthesis.

---

## Using one model for all agents

You do not need multiple AI subscriptions to run a council. You can use a single model for all agents.

To do this effectively:
1. Run each agent as a completely separate conversation — do not continue from a previous agent's chat
2. Give each agent only their role file and the context (not the prior agents' contributions, in blind mode)
3. Starting a new conversation resets the model's working context, which is what you want

Some users run all agents in a single session by explicitly instructing the model to "switch roles" — this works but is more susceptible to context bleed and sycophancy.

---

## Forking the protocol

council.md is MIT licensed. Fork it freely.

If you make changes to the core protocol structure (the six file types, the phase lifecycle, the voting mechanism), increment the version in **SPEC-core** / **SPEC-rules** and document what changed. This helps anyone who forks your fork understand what they are working with.

If you build a profile or role set that works well for your domain, consider contributing it back via a pull request.
