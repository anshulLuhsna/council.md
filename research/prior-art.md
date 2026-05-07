> **Note:** This is the original research write-up that fed council.md. **[`SPEC-core.md`](../SPEC-core.md) v0.2** is **canonical** and supersedes any claims here about file layout (e.g. where synthesis must live). Use this document for **prior art, motivation, and intellectual provenance** — not as the normative protocol.

---

# Markdown-based Model Council Protocol: File-mediated Multi-Model Collaboration

## Executive overview

This report investigates a markdown-only, file-based protocol for orchestrating a “model council” of independent LLM agents that collaborate on decisions without shared runtimes, API orchestration, or centralized frameworks. The core mechanism is a structured markdown workspace (context, role prompts, discussion log, synthesizer instructions) that any model can read and append to, with a final synthesizer producing an agreement/conflict summary while a human retains decision authority.[^1][^2][^3][^4][^5][^6]

Compared to existing multi-agent frameworks, this approach emphasizes protocol over infrastructure: no requirement for API keys, frameworks, or databases; the file is the communication substrate and the only dependency is a markdown-capable LLM UI (Claude Code, ChatGPT, Ollama frontends, etc.). Prior art shows convergent evolution toward markdown-based coordination (Turnfile, markdown task boards, AGENTS.md, llm-md), but most solutions either assume a single runtime or embed protocol semantics in code, leaving open space for a purely file-spec’d, provider-agnostic council protocol geared toward decision quality rather than continuous autonomous operation.[^2][^3][^5][^7][^8][^1]


## 1. Prior art and related concepts

### 1.1 Markdown- and file-based agent coordination

Several recent projects converge on using markdown files as the shared context and coordination mechanism for LLM agents:

- **Turnfile (SNAP protocol)**: A file-based collaboration protocol where LLM agents coordinate via shared markdown artifacts such as a WORKLOG, mailbox, and TURNFILE.yaml, with human mediation. The WORKLOG acts as a message bus, the Turnfile tracks agent registration, task ownership and locks, and agents are expected to document disagreement via counter-recommendation templates.[^5][^7]
- **Markdown task boards / checklists**: Blog posts demonstrate that simple markdown task files with minimal YAML frontmatter (status, claimed_by, depends_on) can outperform more complex agent messaging architectures, leveraging agents’ existing understanding of markdown while keeping coordination state in versioned files.[^6][^2]
- **File-based memory for AI agents**: Guides on `MEMORY.md`, `SOUL.md`, `IDENTITY.md`, and `USER.md` show how agent memory and personality can be fully externalized in editable markdown with human-in-the-loop editing, emphasizing transparency and portability.[^3]
- **AGENTS.md / agent instruction files**: Work on AGENTS.md introduces a repo-root markdown file that defines agent roles, boundaries, and hand-off rules, plus per-agent files defining identity and capabilities, essentially a lightweight protocol for multi-agent collaboration in codebases.[^4][^9][^10]

These systems validate that LLMs parse markdown and simple frontmatter natively, and that version-controlled, human-editable files are a practical substrate for coordination and memory.[^2][^3][^6]

### 1.2 Model Context Protocol and structured formats

The **Model Context Protocol (MCP)** defines an open YAML/JSON format for sharing tools, memory, prompts, and context across agents and frameworks, enabling portability of tools and agent setups between providers. MCP is protocol-like but assumes structured machine parsing and often a server/runtime to serve MCP endpoints.[^11][^12]

Other work surveys JSON, YAML, and new formats like BAML or POML for LLM interactions:

- JSON is strict and brittle; YAML is more human-friendly but sensitive to indentation; both assume exact syntax from models.[^13]
- BAML treats prompts as typed functions, extracting structure from chatty outputs while enforcing contracts, useful when strong tooling and type safety are required.[^13]

The proposed markdown council protocol differs by intentionally embracing markdown as the primary representation, using headings and lightweight delimiters to structure agent contributions rather than rigid schemas.

### 1.3 LLM council and multi-model ensembles

The **LLM Council** concept popularized by Karpathy and others uses multiple models or agents that debate, review, and rank each other’s outputs, with a chairman LLM synthesizing a final answer. Implementations and experiments show that:[^14][^15][^16]

- Councils improve depth, clarity, and robustness for complex, high-risk tasks (legal, medical, architectural decisions) relative to a single model, particularly when combined with “LLM as a judge” patterns and peer review.[^15][^17][^14]
- Several open-source projects (e.g., agent-council, AgentCouncil for Copilot CLI) implement multi-agent deliberation with collaborative or adversarial modes and structured synthesis phases.[^18][^19][^20]

At a more theoretical level, work on ensemble decision-making in multi-agent systems and LLM ensembles discusses consensus dynamics, voting strategies, and robustness. Recent controlled benchmarks like DeliberationBench highlight that naive deliberation protocols can underperform simple best-of-N selection: one study finds that a baseline of selecting the best single answer from a pool beats deliberation protocols by a large margin and at lower cost. This suggests any council protocol must be careful not to add coordination overhead without clear quality gains.[^21][^22][^23]

### 1.4 Society of mind and agentic architectures

Minsky’s “Society of Mind” and modern interpretations emphasize intelligence as emerging from many specialized, limited agents forming agencies and hierarchies rather than a monolithic problem-solver. Contemporary LLM-based multi-agent systems adopt similar principles: specialized agents (planners, builders, critics, etc.) work in modular roles coordinated by orchestration logic or communication protocols. The proposed markdown council protocol is essentially a minimal, file-mediated realization of a small society-of-mind: the “agencies” are markdown files and headings rather than runtime objects.[^24][^25][^26]


## 2. Protocol design: minimum viable spec

### 2.1 Core workspace layout

A minimal workspace that fits the constraints (markdown-only, no runtime) can follow this directory structure:

```text
/council/
  context.md         # shared background, constraints, artifacts
  discussion.md      # active log of the council session
  /agents/
    cto.md           # CTO role definition
    builder.md       # Builder role definition
    reviewer.md      # Reviewer role definition
    ...
  synthesizer.md     # instructions for the synthesis model
```

This mirrors existing patterns like AGENTS.md plus per-agent files, Turnfile skill files, and file-based memory layouts, but specialized for decision councils. Everything required to run a council round is contained in these markdown files; no code or API clients are required to execute the protocol.[^3][^4][^5]

### 2.2 Discussion file: minimum structure

The discussion file should be both human-readable and reliably parseable by LLMs. A minimum viable structure for `discussion.md` might be:

```markdown
# Council: [short topic]

## Question
- Human: <problem statement>
- Decision type: [design / prioritization / trade-off / risk review / other]
- Success criteria: <what a good decision looks like>

## Timeline
- Opened: <timestamp>
- Status: [open | synthesizing | closed]

## Contributions

### Agent: CTO (Model: _optional note_)
- Round: 1
- Summary:
  - <3–7 bullet summary of position>
- Detailed reasoning:
  - <freeform markdown; can include lists, examples, code blocks>
- Flags:
  - Risks: <bullets>
  - Unknowns: <bullets>

---

### Agent: Builder
...

## Synthesis (to be filled by synthesizer)
- Agreement map:
- Conflict map:
- Open questions:
- Recommended options (non-binding):
```

Required sections:

- A **Question** block (human-authored) describing the decision and success criteria.
- A **Contributions** section where each agent writes under its own `### Agent: <Role>` heading, with structured subfields: round, summary, reasoning, flags (risks, unknowns, assumptions).
- A **Synthesis** section initially empty, reserved for the synthesizer’s output.

Optional/advanced fields:

- **Decision type** and **risk level** tags, guiding agents on depth and caution.
- **Model metadata** (e.g., which LLM, temperature), captured in parentheses for auditability.
- **Iteration counter** if the council runs multiple rounds.

This structure is deliberately parallel to patterns in Turnfile (worklog, counter-recommendations) and AGENTS.md (clear roles and handoffs), but stripped down to the smallest set of fields needed for reliable reading and writing by different LLMs.[^7][^4][^5]

### 2.3 Agent file spec (`/agents/[role].md`)

To stay model-agnostic and robust across providers, per-agent role prompts should be:

- Short (roughly 30–60 lines), focusing on what the agent does, what it does not do, and how it contributes to the council.[^10][^4]
- Explicit about goals: “Your job is to provide [architectural / financial / product] perspective; optimize for [X], ignore [Y].”
- Consistent in structure so models see similar patterns across roles.

A minimal schema:

```markdown
# Role: CTO

## Mission
- You represent the long-term technical strategy.
- Optimize for robustness, security, and strategic leverage, not just immediate delivery speed.

## Responsibilities
- Identify architectural risks and long-term constraints.
- Propose technical options with trade-offs.
- Flag hidden complexity and platform risks.

## Constraints
- Do not propose implementation details beyond high-level architecture.
- Defer to Builder on low-level implementation specifics.

## Interaction rules
- Read `context.md` fully before contributing.
- Read all existing contributions in `discussion.md`, especially disagreements.
- When you disagree, explicitly write a "Counterpoint" section explaining why.

## Output format
When you write in `discussion.md` under your agent section, follow this structure:
- Summary (3–7 bullets)
- Detailed reasoning
- Risks
- Unknowns
- Counterpoints (if applicable)
```

Using an explicit **Output format** block aligns with best practices from AGENTS.md and SKILL.md patterns, where instructions are written as small protocol specs in markdown that agents can follow reliably.[^27][^5][^3]

### 2.4 Handling conflicting contributions

The basic protocol treats conflicts as first-class data rather than bugs:

- Each agent is encouraged (or required) to include a **Counterpoints** subsection under its contribution whenever it disagrees with prior agents, referencing their headings and specific claims.
- The discussion file naturally becomes a log of agreements and disagreements; the synthesizer is instructed to preserve and map these rather than collapsing them.

Possible extended mechanisms:

- **Explicit disagreement tags**: e.g., `> DISAGREE: [CTO] overestimates cost of option B because ...` to give the synthesizer anchors.
- **Confidence scores**: Agents can optionally rate their confidence (low/medium/high) on key recommendations, enabling the synthesizer to weigh conflicts.

The protocol itself does not resolve conflicts; it ensures that conflicts are documented in a structured way, and the synthesizer presents them clearly so that a human can decide.[^14][^15]


## 3. Synthesizer design

### 3.1 Synthesizer role and model choice

The synthesizer is a special agent with a narrow remit:

- Read the question, context, and all agent contributions.
- Build an **agreement map** (what most or all agents converge on).
- Build a **conflict map** (where they diverge, why, and what’s at stake).
- Surface **open questions** and missing information.
- Optionally propose a small set of **candidate decisions** (2–3) with trade-offs, explicitly non-binding.

Model considerations:

- In practice, high-context, high-reasoning models (e.g., Claude-class models or frontier GPTs) perform better at nuanced synthesis and disagreement surfacing, especially when reading long markdown files.[^1][^14]
- The protocol remains model-agnostic: any sufficiently capable model that can follow markdown instructions can act as a synthesizer; the repo can recommend a default profile (e.g., “use your best long-context model for synthesis”).[^8]

### 3.2 Synthesizer prompt structure (synthesizer.md)

A useful synthesizer prompt file might look like:

```markdown
# Role: Council Synthesizer

## Mission
You are a neutral synthesizer.
You do **not** make final decisions.
You:
- Identify where council agents agree.
- Identify where they disagree and why.
- Surface open questions and missing information.
- Propose non-binding options with trade-offs.

## Inputs
You will be given:
- `context.md`
- `discussion.md` (including the Question and all agent contributions)

## Output format
Write your synthesis into the `## Synthesis` section of `discussion.md` using this structure:

### Agreement map
- [Point 1]: which agents support it and why.
- [Point 2]: ...

### Conflict map
For each major disagreement:
- Topic: <short label>
- Positions:
  - [Agent role]: <position summary>
  - [Agent role]: <position summary>
- Stakes: <what changes depending on which position is chosen>
- Evidence gaps: <what data would resolve this>

### Open questions
- <questions the human should answer or investigate>

### Candidate decisions (non-binding)
For 1–3 viable options:
- Option label: <short name>
- Description: <what this option means>
- Pros: <bullets>
- Cons: <bullets>
- Preconditions: <what must be true for this to be sound>

## Anti-averaging rules
- Do **not** merge conflicting positions into a vague compromise.
- Preserve sharp disagreements and explain them.
- If agents strongly disagree, say so and avoid recommending a single best option.
- When in doubt, escalate uncertainty instead of hiding it.
```

This structure encodes the desired outcome (maps and options) and explicitly instructs the synthesizer to avoid naive averaging, a known failure mode in ensemble summarization.[^23][^14]

### 3.3 Preventing “average-out” behavior

Empirical work on ensemble decision-making and multi-LLM councils shows that naive aggregation can underperform best-of-N selection and hide important conflicts. To avoid this, the protocol can include:[^22][^21][^23]

- **Explicit anti-averaging principles** in `synthesizer.md` (as above).
- **Per-agent attributions** in the agreement/conflict maps so the human sees which roles back which positions (e.g., “CTO and Reviewer favor option A; Builder prefers option B”).[^15][^14]
- **Uncertainty surfacing**: require the synthesizer to list “evidence gaps” for each major conflict and to mark any candidate decision where the council is split.

These mechanisms shift the synthesizer from a judge to a cartographer of the decision landscape, which aligns better with human-in-the-loop governance.


## 4. Distribution and tooling

### 4.1 Making this a usable open-source repo

Successful markdown-based tooling projects share several traits: small core, clear examples, and strong documentation. A public repo for the council protocol can follow this pattern:[^28][^8][^1]

- **Top-level layout**:
  - `README.md`: high-level concept, quickstart, visual diagram of the council flow.
  - `/examples/`: ready-to-run council folders (e.g., product decision, architecture review, hiring decision).
  - `/templates/`: starter `context.md`, `discussion.md`, `agents/*.md`, `synthesizer.md`.
  - `/cli/` (optional): minimal scripts to open the right files in the user’s editor.
- **Design philosophy**: emphasize that the protocol is markdown-only; any automation is thin convenience, not a dependency.
- **Compatibility notes**: short section on using it with Claude Code, ChatGPT web, local models (e.g., “copy-paste these three files into your project and point your agent to them”).[^8][^3]

The README can mirror the clarity of Turnfile and llm-md docs: explain the protocol as a set of conventions, show a minimal session transcript, and emphasize that users retain full control and can version the council logs.[^5][^7][^8]

### 4.2 Simple CLI helper (no API keys)

A minimal CLI that respects the “no API keys required” constraint should:

- Avoid calling LLM APIs directly; instead, open files in the user’s preferred editor or browser.
- Provide commands like:
  - `council init`: scaffold a new `/council` folder from templates.
  - `council open question`: open `discussion.md` at the Question section.
  - `council open agent <role>`: open the agent’s role file and scroll to its output format section.
  - `council open discussion`: open `discussion.md` for appending contributions.
  - `council status`: print which agents have written contributions in this session.

The CLI can be implemented in any language (shell, Python, Node) and should not require network access; it simply manipulates files and maybe offers small quality-of-life features like inserting agent headings or timestamps. This mirrors tools like `markdown_llm` that let users chat with LLMs inside markdown documents while delegating key management to other layers.[^28][^8]

### 4.3 Related repos to study or draw from

- **Turnfile**: for WORKLOG/message-bus patterns, conflict templates, and TURNFILE.yaml coordination.[^7][^5]
- **AGENTS.md / agent instruction repos**: for role definition patterns and hand-off conventions in markdown.[^9][^4][^10]
- **llm-md** and similar tools: for embedding agent flows in markdown files and controlling multi-agent turns with headings.[^29][^8]
- **AgentCouncil / agent-council**: for council protocols, collaborative vs adversarial modes, and logging council transcripts.[^19][^20][^18]

These provide concrete design inspirations while your protocol remains simpler and provider-agnostic.


## 5. Quality, reliability, and evaluation

### 5.1 Measuring council vs single-model performance

Recent evaluations like DeliberationBench show that naive deliberation protocols can be both more expensive and less accurate than simply selecting the best single response, underscoring the need for careful protocol design and task selection. Other work on LLM councils reports quality improvements for complex, high-stakes tasks when using multi-agent debate plus structured synthesis.[^17][^23][^14]

For this markdown council protocol, a practical evaluation plan could include:

- **Task selection**: focus on complex, high-impact decisions (architecture choices, product strategy, financial trade-offs) where multiple perspectives are valuable.[^17][^14]
- **Baselines**:
  - Single best-of-N model responses (sample several models or temperatures, pick the best via human or an LLM judge).[^23]
  - Simple self-reflection protocols (model critiques its own answer once or twice).
- **Metrics**:
  - Human-rated decision quality (correctness where verifiable, robustness, risk coverage, clarity of trade-offs).
  - Time and cognitive load for the human to reach a decision.
  - Rate of caught errors or surfaced risks compared to single-model baselines.

Controlled experiments can be modeled after existing council and ensemble evaluations, but tailored to your domain (e.g., Arbityr product decisions, technical design reviews).[^30][^14][^23]

### 5.2 Failure modes

Likely failure modes, informed by multi-agent literature and markdown-based coordination reports, include:

- **Coordination overhead without benefit**: For simple tasks, the council adds latency and noise; a single strong model suffices.[^14][^23]
- **Sycophancy cascade**: Later agents may converge on early opinions instead of independently exploring the space, especially if instructed to “build on” prior work without explicit encouragement to disagree.[^21][^22]
- **File drift and context bloat**: `discussion.md` can become unwieldy over many rounds, making it harder for models to parse; careful scoping and archiving may be needed.[^2][^3]
- **Hidden authority bias**: If one agent role (e.g., CTO) is implicitly treated as more authoritative, other agents may defer rather than challenge.

These failure modes mirror observations that multi-agent systems can suffer from lower success rates when coordination is poorly designed, and that token and latency overheads can outweigh benefits if councils are used indiscriminately.[^23][^2]

### 5.3 Anti-sycophancy mechanisms

To prevent agents from mindlessly agreeing with each other, the protocol can embed several mechanisms:

- **Role framing and incentives**: In each agent file, explicitly instruct agents to “prioritize independent reasoning first, then review others,” and to **always document at least one potential weakness or alternative** even when agreeing.[^4][^3]
- **Structured counterpoint sections**: Require a `Counterpoints` subsection for each agent, listing any disagreements or alternative views; Turnfile’s counter-recommendation template offers a concrete pattern.[^5]
- **Blind first round**: Optionally, run a first council round where agents answer without seeing each other; then a second round where they read and critique each other’s contributions, similar to blind panel and review loops in AgentCouncil.[^31][^19]
- **Synthesizer constraints**: Instruct the synthesizer to highlight disagreements and to avoid promoting a single consensus option when substantive conflicts remain unresolved.[^14][^23]

These mechanisms align with research that leverages deliberation and critique to improve diversity of reasoning rather than collapse it.[^22][^21][^14]


## 6. Proposed repo structure and README framing

### 6.1 Suggested repo layout

```text
model-council-protocol/
  README.md
  /templates/
    context.md
    discussion.md
    synthesizer.md
    /agents/
      cto.md
      builder.md
      reviewer.md
      cfo.md
      pm.md
  /examples/
    product-decision/
      ... (filled-in files from a sample session)
    architecture-review/
      ...
  /docs/
    protocol.md      # formal spec of fields and rules
    patterns.md      # anti-sycophancy, blind rounds, etc.
    prior-art.md     # short survey with links
  /cli/
    council.sh or council.py (optional helper)
```

This parallels layouts used by Turnfile, llm-md, and agent council projects: a small, inspectable core with templates and worked examples.[^20][^28][^8][^5]

### 6.2 README positioning (one-paragraph style)

A concise README positioning, reflecting trends in LLM Council writeups, could be:

> **Model Council Protocol** is a markdown-only way to run a “room full of AI experts” on your hardest decisions—without API orchestration, frameworks, or shared runtimes. Instead of wiring agents together in code, you drop four files into a repo: `context.md`, `discussion.md`, `/agents/*.md`, and `synthesizer.md`. Each model—Claude, ChatGPT, local LLMs—reads the same files, contributes its perspective under its role heading, and stops. A final synthesizer model maps where the council agrees, where it disagrees, and what’s still unknown so that you, the human, can make the call. If you can edit markdown, you can run a council.[^17][^8][^14]

This explicitly differentiates the protocol from heavyweight multi-agent frameworks and positions it as an opinionated yet minimal coordination convention.


## 7. Novelty and differentiation

The proposed protocol is adjacent to, but distinct from, existing work:

- **Compared to multi-agent frameworks (LangChain, AutoGen, CrewAI, MetaGPT, etc.)**: Those frameworks primarily provide code-level orchestration, message schemas, and execution graphs, often assuming API keys and a shared runtime; communication is usually via structured JSON/YAML messages and in-memory state. The markdown council protocol is a file-level convention that can be executed manually via any LLM UI, with no runtime or dependencies.[^32][^24]
- **Compared to MCP and structured protocols**: MCP focuses on standardizing context and tool definitions in YAML/JSON for interoperability across agent frameworks. The council protocol focuses on human-readable markdown logs and role files, trading strict machine parsing for transparency and low setup friction.[^12][^11]
- **Compared to Turnfile and markdown coordination boards**: Turnfile and related protocols target continuous, concurrent multi-agent collaboration on codebases, with worklogs, file locks, and task boards. The council protocol focuses on discrete decision sessions where a small set of agents deliberate on a single question, with human-controlled sequencing and explicit synthesis.[^6][^7][^5]
- **Compared to LLM Council projects**: Existing council implementations tend to be code-based systems routing queries to multiple models via APIs (often OpenRouter or similar) and performing programmatic aggregation. The markdown council protocol generalizes the council concept into a provider-agnostic, fully manual workflow that any developer can run inside their editor with whatever models they already use.[^16][^18][^19][^15][^14]

This combination—markdown-only, fully manual, role-based council protocol with an explicit synthesizer and anti-sycophancy design—appears novel relative to current public projects, though it builds heavily on convergent patterns in Turnfile, AGENTS.md, llm-md, and LLM Council work.[^1][^3][^5][^14]


## 8. Practical next steps

For an initial public release suitable for developers and founders with access to multiple models:

1. **Finalize the spec** for `context.md`, `discussion.md`, `agents/*.md`, and `synthesizer.md` based on the minimum structures above, including explicit Output format blocks and counterpoint conventions.
2. **Create two end-to-end example councils** (e.g., a product pivot decision and a backend architecture choice), run by you using multiple models; commit the final `discussion.md` logs as canonical examples.
3. **Design a minimal CLI** that only scaffolds and opens files, avoiding any assumption about APIs or providers.
4. **Document anti-sycophancy patterns** (blind first round, required counterpoints, synthesizer anti-averaging rules) in `docs/patterns.md`.
5. **Optionally publish a short benchmark** where a few real decisions are evaluated by humans under (a) single-model, (b) best-of-N, and (c) markdown council, to demonstrate where the protocol adds value.

These steps would make the protocol forkable, usable in under ten minutes, and clearly positioned as a simple but principled way to get “many minds” on hard decisions without spinning up a full agent framework.[^28][^17][^14]

---

## References

1. [I built an agent framework in 3 Markdown files - Hacker News](https://news.ycombinator.com/item?id=44281542) - The "runtime" is just a powerful LLM (like Claude in a VSCode project). You give it a high-level goa...

2. [I Let AI Agents Manage Themselves with a Markdown File](https://dev.to/battyterm/i-let-ai-agents-manage-themselves-with-a-markdown-file-5547) - Everyone's building sophisticated agent coordination protocols. I replaced them all with a Markdown ...

3. [AI Agent Memory Management - When Markdown Files Are All You ...](https://dev.to/imaginex/ai-agent-memory-management-when-markdown-files-are-all-you-need-5ekk) - How to Design File-based Memory for Your AI Agent? File-based AI agent memory typically consists of ...

4. [Stop Prompt Overload: Use Four Simple Markdown Files to Make ...](https://www.linkedin.com/pulse/stop-prompt-overload-use-four-simple-markdown-files-make-munish-gupta-iaqnc) - Stop Prompt Overload: Use Four Simple Markdown Files to Make Multi-Agent AI Reliable and Chaos-Free.

5. [turnfile/docs/LLM_ONBOARDING.md at main - GitHub](https://github.com/snapsynapse/turnfile/blob/main/docs/LLM_ONBOARDING.md) - file-based protocol for making LLM agents collaborate on shared codebases without real-time communic...

6. [A Practical Coordination Protocol for LLM Agent Swarms - Pubroot](https://pubroot.com/ai/agent-architecture/file-ownership-and-message-passing-a-practical-coordination-protocol-for-2026-024/) - "Multi-agent LLM systems face a fundamental coordination problem: how do you let 10-20 autonomous ag...

7. [I spent years trying to get AI agents to collaborate. Then Opus 4.6 ...](https://snapsynapse.com/tools/turnfile/) - Turnfile is a file-based collaboration protocol for LLM agents. It's called SNAP — Structured Negoti...

8. [Like markdown for LLMs](https://llm.md) - llm-md - a simple, powerful tool to use AI.

9. [How to Build Your AGENTS.md (2026): The Context File That Makes ...](https://www.augmentcode.com/guides/how-to-build-agents-md) - AGENTS.md is a Markdown file placed at the root of a repository that provides AI coding agents with ...

10. [How to teach your coding agent with AGENTS.md](https://ericmjl.github.io/blog/2025/10/4/how-to-teach-your-coding-agent-with-agentsmd/)

11. [Model Context Protocol: a YAML/JSON format for LLM agents](https://www.linkedin.com/posts/sakshamawasthi1111_ive-been-working-on-integrating-llm-based-activity-7317983144127668224-SM0E) - It defines a simple, structured, open format for sharing everything an LLM agent needs to operate - ...

12. [ai-multi-agent · GitHub Topics](https://github.com/topics/ai-multi-agent) - A Model Context Protocol (MCP) TypeScript template with multi agents that can send Emails, schedule ...

13. [BAML vs POML vs YAML vs JSON for LLM Prompts | Augment Code](https://www.augmentcode.com/learn/baml-vs-poml-vs-yaml-vs-json-for-llm-prompts) - JSON treats LLM output like an API response. · YAML trades brackets for indentation. · POML remains ...

14. [From Solo Models to Collective Intelligence](https://www.merfantz.com/blog/from-solo-models-to-collective-intelligence-introducing-llm-council/) - Learn how LLM Council enables multiple AI models to collaborate through review, ranking, and synthes...

15. [LLM Council for Code Review: How Multiple AIs Debate and Judge Each Other (Claude, ChatGPT, Gemini)](https://www.youtube.com/watch?v=9A-iJKGmt2I) - Are you tired of relying on a single Large Language Model (LLM) for your hardest questions or critic...

16. [LLM Council works together to answer your hardest questions - GitHub](https://github.com/karpathy/llm-council) - It's nice and useful to see multiple responses side by side, and also the cross-opinions of all LLMs...

17. [LLM Council Boosts AI Decision Making with Multi-Agent ...](https://www.linkedin.com/posts/chiraaggangwani_generativeai-llmcouncil-aistrategy-activity-7434964662594555904-kkRY) - What if your AI didn't just answer it, but argued with itself first? That's the idea behind an LLM C...

18. [andrewvaughan/agent-council: Multi-perspective AI ... - GitHub](https://github.com/andrewvaughan/agent-council) - When a single AI agent plans, builds, and reviews its own code, blind spots compound. Agent Council ...

19. [AgentCouncil - Using Collaborative or Adverserial multi agent (from ...](https://github.com/Sentry01/AgentCouncil) - Agent Council. A skill and agent for GitHub Copilot CLI that throws three different AI models at you...

20. [I hacked together a “local LLM council” for code review using ...](https://www.reddit.com/r/ClaudeAI/comments/1p6ytd4/i_hacked_together_a_local_llm_council_for_code/) - So I built a tiny project called agent-council: https://github.com/mylukin/agent-council. Right now ...

21. [Ensemble Decision-Making in Multi-Agent Systems - Emergent Mind](https://www.emergentmind.com/topics/multi-agent-ensemble-decision-making) - Multi-agent ensemble decision-making is a process where multiple autonomous agents integrate diverse...

22. [An Electoral Approach to Diversify LLM-based Multi-Agent ...](https://arxiv.org/html/2410.15168v1)

23. [When Do More Voices Hurt? A Controlled Study of Multi-LLM ... - arXiv](https://arxiv.org/html/2601.08835v1)

24. [Multi-Agent Systems: Implementation Best Practices](https://fme.safe.com/guides/ai-agent-architecture/multi-agent-systems/) - Learn about multi-agent systems and how they improve upon single-agent workflows in handling complex...

25. [Revisiting Minsky's Society of Mind in 2025 - LinkedIn](https://www.linkedin.com/pulse/revisiting-minskys-society-mind-2025-sutha-kamal-qbnmc) - It was exciting: Minsky made AI seem so tractable, with beautiful essays arguing that the mind is co...

26. [AgentSociety: Large-Scale Simulation of LLM-Driven Generative ...](https://arxiv.org/html/2502.08691v1) - In this paper, we propose AgentSociety, a large-scale social simulator that integrates LLM-driven ag...

27. [Markdown as an Agent Instruction File: How to Write ... - Towards AI](https://pub.towardsai.net/markdown-as-an-agent-instruction-file-how-to-write-files-that-agents-actually-read-5722ede42ff2) - An agent‑friendly Markdown file is essentially a small protocol spec written in plain text that any ...

28. [GitHub - matweldon/markdown_llm: A tool for interacting with an LLM in a markdown document](https://github.com/matweldon/markdown_llm) - A tool for interacting with an LLM in a markdown document - matweldon/markdown_llm

29. [demo: llm agents as markdown files](https://www.youtube.com/watch?v=Kr88DVh2UiI) - short demo of a feature to pass messages from a conversation to an llm workflow (not sure you could ...

30. [what are the best governance rules for the council? So I built a little ...](https://x.com/ahall_research/status/2003892036001566871)

31. [GitHub | Kiran Krishna - LinkedIn](https://www.linkedin.com/posts/kirantechenthusiast_github-kiran-agenticagentcouncil-multi-agent-activity-7449453357754236928-CJC-) - ... agent council analysis as a plugin - Agent SDK turns out to be model-agnostic — you can run Kimi...

32. [Design feedback on a provider-agnostic multi-agent framework in ...](https://github.com/orgs/community/discussions/183019) - Hi everyone,. I'm looking for architectural feedback on a Python project I've been building around m...

