# Council Context — Review

## Question
[What is the core question this review is answering? e.g. "Is this design ready to ship?" or "Should we approve this plan?"]

## What Is Being Reviewed
The proposed inference architecture for our AI product's backend. Specifically: whether to build our inference layer on top of a third-party LLM API (OpenAI, Anthropic, etc.) via a provider-agnostic abstraction, or to begin fine-tuning a domain-specific model on proprietary data and self-host it.

We are 6 months into a B2B SaaS product with an AI feature set at the core. We have ~180 paying customers. The product currently runs on OpenAI GPT-5 via direct API. We are evaluating whether to stay on this path, build a provider abstraction layer, or start a fine-tuning program.

The proposal document (informal):
- Option A: Stay on direct GPT-5 API. No abstraction layer. Lowest engineering cost.
- Option B: Build a provider-agnostic abstraction layer (LiteLLM-style) that lets us swap models without code changes. Still using third-party APIs.
- Option C: Begin a fine-tuning program on our proprietary customer interaction data. 6–12 month horizon. Self-host a tuned open-source base model (Llama or similar).

## Purpose of This Review
Architectural go/no-go review. We want to commit to a direction for the next 12 months before our infrastructure costs scale significantly. We are currently spending $4,200/month on API costs. At projected growth, that reaches $18,000/month in 12 months.

## Evaluation Criteria
1. Cost efficiency at scale
2. Performance on our specific task domain (structured document analysis)
3. Data privacy and compliance for enterprise customers (some customers are sensitive about data leaving their infrastructure)
4. Engineering effort and team capacity (2 backend engineers, 1 ML engineer with fine-tuning experience but no production deployment experience)
5. Vendor risk and lock-in
6. Time to first production-quality result

## Known Concerns
- We have never fine-tuned or self-hosted a model in production. Our ML engineer has academic fine-tuning experience only.
- Enterprise customers are starting to ask about data residency. We do not have a clear answer today.
- Our current task (structured document analysis) is specialized enough that GPT-5 makes mistakes we have to post-process. A fine-tuned model might outperform it on our exact task.
- The cost projection assumes API pricing stays flat. If pricing increases 30–50%, that materially changes the calculus.

## Deadline
Architecture decision needed in 2 weeks. We begin the next infrastructure sprint then.
