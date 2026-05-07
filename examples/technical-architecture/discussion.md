# Review Council: Inference Architecture — API vs. Fine-Tuning

> **Profile:** review
> **Discussion round:** 1
> **Note:** Phase lives in `votes.md` frontmatter only.

---

## Instructions for agents

Before you write:
1. Read `context.md` fully — including all three options, evaluation criteria, and known concerns.
2. Read your own role file.
3. **Blind round enabled.** Write your contribution before reading others.

---

## Contributions

### Agent: Architect

#### Position
Option B (provider-agnostic abstraction) is the correct near-term architectural decision. Option C (fine-tuning) is a valid 12-month horizon goal, but executing it now with the stated team capacity is premature and high-risk. Do not do both simultaneously.

#### Reasoning
The core architectural principle here is: **delay irreversible decisions until you have the information to make them well.** Fine-tuning and self-hosting a model in production is an irreversible infrastructure commitment. You cannot easily undo it after 6 months of building, especially if your ML engineer leaves.

Option B is architecturally elegant precisely because it buys time. A clean abstraction layer (router + provider interface + unified logging) gives you three things:
1. Vendor risk mitigation — you can swap to Anthropic, Gemini, or an open-source API endpoint in days
2. Cost optimization — you can A/B test cheaper models on specific subtasks
3. Future compatibility — if you do fine-tune in 6 months, you plug in your self-hosted endpoint behind the same abstraction without touching application code

The implementation complexity of Option B is low-to-medium: LiteLLM or a thin custom router is a 1–2 week project for a competent backend engineer. It does not touch your application logic.

Option C's architectural risk is not the model quality — it is the operational burden. Fine-tuning is research. Serving a fine-tuned model in production with SLAs, versioning, rollback, monitoring, and cost management is a different discipline entirely. Your ML engineer has the first skill, not the second.

Option A (stay on direct API) is defensible short-term but creates exactly the lock-in you will regret when pricing changes or when an enterprise customer demands data residency controls. The abstraction layer costs very little compared to the pain of retrofitting it later.

Recommended path: **Build Option B now. Revisit Option C in 6 months after you have validated your task domain well enough to create a high-quality fine-tuning dataset and after you have production ML serving experience on the team.**

#### Risks
- Option B could give a false sense of vendor independence if the abstraction is leaky. It must be tested against at least 2 providers on day 1 to be real.
- If you start Option C too early and the fine-tuned model underperforms in production, you have sunk significant engineering time and may still be on the API with no abstraction layer.

#### Unknowns
- What is the actual error rate of GPT-5 on your specific structured document task? If it is above 5%, Option C becomes more urgent.
- What does your post-processing pipeline look like — is it masking a model problem that fine-tuning would actually solve?

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
HIGH on the architectural recommendation. MEDIUM on the 6-month timeline for Option C — that depends on task-specific data volume and quality I cannot assess from this context.

---

### Agent: Security

#### Position
The data residency and privacy concern is not a nice-to-have feature for enterprise customers. It is a go/no-go sales blocker at the $10k+ ACV tier. Option B delays this problem; Option C solves it, but only if executed correctly. Neither option as described currently addresses the compliance architecture. That is the most important gap in this proposal.

#### Reasoning
Here is what enterprise customers actually ask about, in my experience:
1. Where does my data go when it leaves my infrastructure?
2. Is it used to train models?
3. Can I get a data processing agreement (DPA)?
4. Can I do a security review of your infrastructure?

On the current GPT-5 direct API path (Option A): data goes to OpenAI. Enterprise AI data processing addendums exist but are not universally accepted by enterprise legal teams. This is increasingly a deal-breaker.

On Option B (abstraction layer + third-party APIs): data still leaves your infrastructure to a third-party provider. The abstraction layer does not change the compliance posture — it changes the vendor, not the architecture. You can now route to an Anthropic API instead of OpenAI, but enterprise legal teams may not care about that distinction.

On Option C (self-hosted fine-tuned model): if hosted in a VPC or on-premises, data never leaves the customer's infrastructure boundary. This is the only option that actually addresses data residency at a structural level.

**My assessment:** the council is debating cost and performance when the real constraint may be whether you can sell to enterprise customers in 12 months. If your ICP (ideal customer profile) is mid-market enterprise with data sensitivity, Option C or a variant of it (self-hosted inference, not necessarily fine-tuned) becomes architecturally necessary regardless of cost.

However — and this is critical — **self-hosted inference is a security and compliance responsibility, not just a capability**. Your team would own model access controls, audit logging, vulnerability management, and incident response. That is a significant commitment for a team of 3 backend/ML engineers.

#### Risks
- Building Option B without addressing the data residency question will likely require a full architecture revisit in 12 months when an enterprise customer demands it. This is a hidden cost that is not in the $4,200/month vs. $18,000/month calculus.
- Option C self-hosted is not automatically more secure. A poorly secured self-hosted model endpoint is worse than a well-managed third-party API.

#### Unknowns
**LOW CONFIDENCE FLAG:** I do not have sufficient information about this company's specific customer profiles, compliance obligations, or target market to give a high-confidence security recommendation. What I can say is:
- If you have signed or are pursuing customers in healthcare, finance, or government, compliance architecture is not optional and needs a dedicated review beyond this council.
- If your customers are primarily tech companies and SMBs, the urgency is lower, and Option B is defensible for 12 months.

#### Confidence
LOW — on the specific recommendation, because the right answer depends heavily on customer profile and compliance requirements that are not in the context file. HIGH on identifying data residency as the gap the proposal does not address.

---

### Agent: Product Engineering

#### Position
Option B is the right call for the next 12 months, but I want to add a concrete criterion for when to start Option C: begin fine-tuning only after you have collected at least 2,000 high-quality labeled examples of your exact task. You almost certainly do not have that today. Get Option B running, start labeling, and revisit in Q3.

#### Reasoning
The stated reason for considering fine-tuning is that GPT-5 makes mistakes on structured document analysis that require post-processing. This is the most important signal in the context file, and I want to engage with it directly.

There are two explanations for that post-processing overhead:
1. **Prompt engineering problem:** The task is well-defined but the prompt and output parsing are not optimized. This is fixable with 1–2 weeks of prompt and parser work, no model change needed.
2. **Task distribution mismatch:** Your documents are sufficiently domain-specific that the general-purpose model genuinely underperforms on the distribution. This is a fine-tuning candidate.

Before committing to Option C, you should know which of these is true. The way to find out is to systematically sample 50–100 failure cases, classify whether the errors are prompt-related or model capability-related, and measure the error rate precisely. If the error rate is below 3% and the errors are prompt-related, fine-tuning is not the right investment.

On the engineering capacity question: "1 ML engineer with fine-tuning experience but no production deployment experience" is a real risk. Fine-tuning a Llama-class model for a specific task is a 4–8 week project if the dataset exists and the training infrastructure is available. Getting that model serving reliably in production with monitoring, versioning, and rollback is another 4–8 weeks minimum. That is 2–4 months of your ML engineer's full capacity, plus significant backend engineering support. With 2 backend engineers also running the production system, this is not a side project.

My concrete recommendation: Option B now. In parallel, start building the labeled dataset. Set a revisit gate: at 2,000+ labeled examples and a measured error rate above 3% for model-capability failures, begin Option C planning.

#### Risks
- Option B abstraction layer adds a latency hop and a new failure mode. It needs proper observability from day 1 — not logging added later.
- The most common engineering failure mode in AI infrastructure is underestimating model serving complexity. This specific risk is currently invisible in the proposal.

#### Unknowns
- What is the current error rate, broken down by error type? This should be measured before the decision is made.
- How large is the existing labeled dataset, if any?

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
HIGH on the Option B recommendation. HIGH on the "measure first" recommendation before committing to Option C. MEDIUM on the fine-tuning timeline estimate because it depends on dataset quality.
