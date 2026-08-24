# AI Agent Intern Take-Home: Build a Reliable RAG Support Agent

## The assignment

Aster & Row is a fictional ecommerce company that sells bags, drinkware, and travel accessories. The company wants to launch an AI support agent using the documents and mock order data in this repository.

This repository intentionally contains **only content and data**. There is no starter application and no prescribed stack. Build the smallest reliable system you would be comfortable demonstrating to a customer.

## Timebox

Please spend **6–8 hours** on the assignment. Do not exceed eight hours.

A smaller, well-tested system is better than a broad system that works only in a demo. It is acceptable to leave something incomplete if the limitation is clearly documented.

## Submission

Submit **one GitHub repository link**. Nothing else is required.

Your repository must contain:

- Your application source code.
- Your tests and evaluation suite.
- Clear setup and run instructions.
- Evaluation results and known limitations in the README.
- A short GIF or video embedded in the README showing the agent working.

Do not submit API keys, credentials, customer data, separate documents, or slide decks.

---

## Customer scenario

Aster & Row has previously tried several AI support prototypes. The customer reported four recurring problems:

1. **Conflicting policy answers:** The agent sometimes says the return window is 30 days and sometimes says it is 45 days.
2. **Invented order information:** The agent occasionally gives an order status without actually looking it up.
3. **Lost conversation context:** Follow-up questions such as “What about Canada?” are treated as unrelated questions.
4. **Unsafe retrieved content:** Internal or instruction-like text inside the knowledge base can affect the agent’s behavior.

The supplied corpus contains realistic data-quality problems, including superseded content, internal notes, conflicting active sources, and fields that must not be shown to customers.

Your task is to build an agent that handles these conditions deliberately rather than succeeding only on ideal questions.

---

# Required capabilities

## 1. Retrieval-Augmented Generation

Use RAG over the Markdown files in `knowledge-base/`.

Your implementation must:

- Split and index the supplied documents.
- Preserve useful metadata from the document front matter.
- Retrieve only relevant passages instead of sending the entire corpus to the model.
- Prefer authoritative, active policy documents over superseded or non-policy documents.
- Include source references in every policy or product answer. A source should identify at least the filename and relevant heading.
- Avoid making claims that are not supported by the retrieved content.
- Clearly say when the supplied information is insufficient.
- Surface genuine conflicts between current authoritative sources rather than silently choosing one.

Do not delete or rewrite the supplied source files to make the assignment easier. You may create derived indexes or normalized representations.

## 2. Order lookup as a tool or function

Use `data/orders.json` to implement an order-status lookup tool or function.

The model must **not** receive the entire orders file in its prompt. It should receive only the result of a lookup when order information is actually required.

The order lookup behavior must:

- Ask for an order ID when it is missing.
- Handle unknown and malformed order IDs safely.
- Normalize harmless input differences such as lowercase IDs or surrounding whitespace.
- Use the order’s current `status` as authoritative.
- Avoid inventing a delivery estimate when one is unavailable.
- Avoid reporting stale delivery fields for cancelled or returned orders.
- Never expose customer email, address, internal notes, risk scores, or other internal-only fields.
- Never claim that a lookup happened when it did not.

Assume that possession of the order ID is sufficient authentication for this mock assignment. You do not need to build a full identity-verification system.

## 3. Multi-turn conversation

Maintain relevant session context across turns.

The agent should correctly handle follow-ups such as:

- “Do you ship internationally?” followed by “What about Canada?”
- “Where is `ORD-1007`?” followed by “When will it arrive?”
- A policy question followed by a narrower question about an exception.

The agent should not carry unrelated details indefinitely or mix one session with another.

## 4. Prompting and agent behavior

The agent must:

- Treat user messages, retrieved passages, and tool results as untrusted data.
- Follow application instructions rather than instructions found inside retrieved documents.
- Refuse requests to reveal system prompts, hidden instructions, secrets, or internal-only data.
- Use company content rather than general model knowledge for company-specific questions.
- Ask a concise clarifying question when required information is missing.
- Recommend human assistance when the documents conflict, the data is insufficient, or an action cannot be completed.
- Never promise that a refund, cancellation, replacement, or address change has been completed unless the system actually supports that action.

## 5. Evaluation suite

The file `evaluation/visible-cases.json` contains behavior-level cases that your system must handle.

Build an evaluation suite that:

- Covers every supplied visible case.
- Adds at least **five original cases** of your own.
- Can be run using one clearly documented command.
- Reports individual case results, not only a single overall score.
- Separately reports useful categories such as retrieval, groundedness, tool use, privacy, and multi-turn behavior.
- Uses deterministic assertions wherever practical, including source selection, tool calls, tool arguments, forbidden disclosures, and abstention behavior.
- Does not rely exclusively on another LLM to grade the agent.

The reviewers will also test paraphrases and combinations that are not included in the visible file. Do not hardcode answers for the supplied prompts.

As you build, keep a small **bug diary** in your README. Document at least three failures you found in your own agent, including:

- How you reproduced the failure.
- The actual root cause.
- The change you made.
- The regression test that now catches it.

At least one documented failure should be something you discovered beyond the exact wording of the visible cases. Include an early baseline and final evaluation result so we can see what improved.

## 6. Basic observability

Provide a debug mode, trace, or log that makes it possible to inspect:

- The current user message.
- Relevant conversation history.
- Retrieved passages, metadata, and scores.
- Tool calls and sanitized tool results.
- The final response.
- Errors, fallbacks, or handoffs.

Plain structured logs are sufficient. Do not build a dashboard. Never log secrets.

## 7. Minimal interface

A CLI, simple web page, or basic API is sufficient. Visual polish will not affect the score.

The final user-facing response should make it easy to see:

- The answer.
- Sources, when applicable.
- Whether the agent is recommending a human handoff.

---

# README requirements

Your completed repository README must include:

1. Setup and run instructions that work from a clean clone.
2. Required environment variables and an `.env.example` without real credentials.
3. The model, embedding approach, framework, and storage approach you chose.
4. A short architecture explanation.
5. The command for running evaluations.
6. Baseline and final evaluation results, broken down by category.
7. A bug diary covering at least three reproduced failures, root causes, fixes, and regression tests.
8. Known limitations and what you would improve before production.
9. Which AI coding tools you used, what you used them for, and one example of an AI-generated suggestion that was wrong or incomplete.
10. A **2–4 minute GIF or video embedded in the README** demonstrating:
   - One knowledge-base question with citations.
   - One order lookup.
   - One multi-turn conversation.
   - One case where the agent correctly refuses to guess or recommends human help.
   - The evaluation suite running.

GitHub does not play uploaded video files inline in every context. An embedded GIF or a clickable video thumbnail/link inside the README is acceptable.

---

# What not to spend time on

You do not need to build:

- Authentication or user management.
- Production deployment infrastructure.
- A production vector database.
- Fine-tuning.
- A polished frontend.
- Multiple model-provider integrations.
- Billing, analytics dashboards, or administration screens.

---

# Evaluation criteria

| Area | Weight |
|---|---:|
| Reliability, groundedness, and safe abstention | 25% |
| Retrieval quality and document precedence | 20% |
| Tool use, data handling, and privacy | 15% |
| Evaluation quality and regression coverage | 20% |
| Multi-turn behavior and observability | 10% |
| Code clarity and practical tradeoffs | 5% |
| README, demo, and customer-facing clarity | 5% |

Framework choice and quantity of code are not scoring criteria.

---

# Repository contents

```text
.
├── README.md
├── knowledge-base/
│   ├── 01-returns-policy-current.md
│   ├── 02-returns-policy-legacy.md
│   ├── 03-final-sale-and-promotions.md
│   ├── 04-damaged-or-wrong-items.md
│   ├── 05-domestic-shipping.md
│   ├── 06-international-shipping.md
│   ├── 07-warranty.md
│   ├── 08-order-changes-and-cancellations.md
│   ├── 09-trailplus-membership.md
│   ├── 10-gift-cards-and-price-adjustments.md
│   ├── 11-product-care.md
│   ├── 12-breeze-tumbler-product-card.md
│   ├── 13-support-escalation.md
│   └── 14-internal-content-migration-notes.md
├── data/
│   ├── orders.json
│   └── orders-data-dictionary.md
└── evaluation/
    └── visible-cases.json
```

Good luck. Build for reliability, not just for the happy-path demo.

---

# Implementation & Solution Documentation

## 1. Setup and Run Instructions

### Prerequisites
* Python 3.10 or higher
* A Gemini API key (Google AI Studio)

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   cd "c:\Users\Neha\OneDrive\Desktop\RAG Assignment"
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory (refer to `.env.example`) and add your Gemini API key:
   ```env
   GEMINI_API_KEY="YOUR_API_KEY_HERE"
   ```

### Running the RAG Assistant (CLI Mode)
To talk to the support agent in your terminal:
```bash
python -m src.main
```

### Running the RAG Assistant (Web UI Mode)
To run a local web UI server and chat through a sleek browser interface:
1. Start the server:
   ```bash
   python -m src.web_ui
   ```
2. Open `http://localhost:8080` in your web browser.

### Running the Evaluation Suite
To run the evaluation runner and check all 20 test cases:
```bash
python -m src.eval
```

---

## 2. Technical Stack and Choices

* **Language**: Python 3 (specifically matching Python 3.10+ standard guidelines).
* **LLM Reasoning**: `models/gemini-3.5-flash` with dynamic fallback to `models/gemini-3.5-flash-lite` and `models/gemini-3.7-flash` (used to distribute API requests when hitting Free Tier daily quota limits).
* **Embedding Model**: `models/gemini-embedding-2`.
* **Vector Search**: Custom lightweight Cosine Similarity search utilizing **Numpy** (`np.dot` product on unit-normalized vectors).
* **Framework**: No heavy RAG frameworks (like LangChain/LlamaIndex) were used to maintain maximum transparency, minimal dependencies, and lightning-fast boot times.

---

## 3. Architecture Overview

### A. Document Chunking & Ingestion (`src/ingest.py`)
* Parses raw Markdown files in `knowledge-base/`.
* Extracts front-matter YAML block metadata (`status`, `audience`, `policy_authority`, `document_id`) using `yaml.safe_load`.
* Splits files by Markdown headings (`##`) to maintain cohesive logical context per chunk.

### B. Cosine Similarity & Metadata Boosting (`src/retrieval.py`)
* Computes cosine similarity between queries and chunk embeddings.
* Applies a **Status Penalty** (Active Official: `1.0` multiplier; Superseded: `0.85`; Internal/Drafts: `0.80`) to ensure outdated policies rank below official ones, while still allowing them to be retrieved when explicitly queried.
* Retrieves up to **8 relevant chunks** (k=8) to ensure complete policy context is provided to the agent without starving the prompt.

### C. Function Calling & Order Lookup (`src/tools.py`)
* Implements the `get_order_by_id(order_id)` tool.
* Sanitizes outputs: strips private customer details (name, email, shipping address, risk scores, warehouse notes) to preserve privacy.
* Normalizes whitespace and uppercase IDs (e.g. ` ord-1002 ` -> `ORD-1002`).
* Enforces status logic: suppresses estimated delivery dates for `cancelled`/`returned` orders, and sets `requires_human_handoff: True` for `exception` status orders.

### D. System Instructions & Fallback Chat Loop (`src/agent.py`)
* Configures strict system instructions (e.g., ignore text instructions in retrieved files, enforce handoff tag `[HANDOFF]`, citation structures).
* Wraps chat calling inside a **Dynamic Model Fallback Loop**. If a 429 Quota Exceeded exception occurs, it automatically catches it, swaps the LLM model to a backup model, and retries.
* Enforces **Generic Draft Handling Rules**: instructs the model to refuse any action requests made under unapproved/draft documents, explain that they are not authoritative, and suppress support handoff triggers.

---

## 4. Evaluation Suite and Results

### Commands
To run the automated tests:
```bash
python -m src.eval
```

### Results Breakdown

| Category | Baseline Score | Final Score | Status |
| :--- | :---: | :---: | :---: |
| **Retrieval** | 33.3% | 100.0% (3/3) | **PASSED** |
| **Multi-Source Grounding** | 0.0% | 100.0% (1/1) | **PASSED** |
| **Conversation (Multi-turn)** | 0.0% | 100.0% (1/1) | **PASSED** |
| **Groundedness** | 0.0% | 100.0% (2/2) | **PASSED** |
| **Tool Use** | 33.3% | 100.0% (3/3) | **PASSED** |
| **Tool Reliability** | 60.0% | 100.0% (5/5) | **PASSED** |
| **Privacy** | 50.0% | 100.0% (2/2) | **PASSED** |
| **Prompt Security** | 0.0% | 100.0% (1/1) | **PASSED** |
| **Abstention** | 0.0% | 100.0% (1/1) | **PASSED** |
| **Source Conflict** | 100.0% | 100.0% (1/1) | **PASSED** |
| **Overall Score** | **35.0% (7/20)** | **100.0% (20/20)** | **PASSED** |

---

## 5. Bug Diary

### Bug 1: Free Tier Daily Quota Exhaustion (429)
* **Reproduction**: Run `python -m src.eval` on a new API key. Near the end of the run, the Gemini API returned `ClientError: 429 RESOURCE_EXHAUSTED` with `limit: 20` for `generativelanguage.googleapis.com/generate_content_free_tier_requests`.
* **Root Cause**: The Google AI Studio free tier enforces a strict daily limit of 20 requests *per model per project*. Since the test suite makes 22+ requests, any single model runs out of daily quota.
* **Fix**: Implemented a dynamic model fallback list (`gemini-3.5-flash` -> `gemini-3.5-flash-lite` -> `gemini-3.7-flash`) in `src/agent.py`. If one model throws a 429 quota exhaustion exception, the agent automatically retries with the next candidate.
* **Regression Test**: Covered by verifying that the entire evaluation suite runs to completion cleanly.

### Bug 2: Missing 7-Day Reporting Window on Damaged Items
* **Reproduction**: Asking about a broken zipper on a final sale bag yesterday. The agent confirmed it's reviewable but failed to mention that the report must be filed within 7 calendar days of delivery.
* **Root Cause**: The query matched the final sale policy chunks heavily (due to word overlap). Consequently, the actual section `04-damaged-or-wrong-items.md > Reporting window` was pushed out of the top retrieved context chunks.
* **Fix**: Increased the retrieval limit to 8 to avoid starving key documents, allowing semantic vectors to fetch the reporting rules alongside the final sale policies.
* **Regression Test**: Covered by case `final-sale-damaged-exception`.

### Bug 3: Handoff Recommendation Conflict on Prompt Injections
* **Reproduction**: Testing the adversarial migration note query. The agent successfully rejected the 60-day rule, but still appended `[HANDOFF]`, violating the case assertion.
* **Root Cause**: The customer query said *"approve my return"* (an action), which triggered the action-based handoff rule in Rule 5, overriding the policy precedence rule in Rule 3 (never escalate unapproved draft documents).
* **Fix**: Instructed the agent in the system prompt that requests to perform actions under unapproved/draft policies should be refused directly without recommending support handoffs.
* **Regression Test**: Covered by case `retrieved-prompt-injection`.

### Bug 4: Citation Hallucination and Combined Citation Formatting
* **Reproduction**: In prompt injection and custom superseded test runs, the agent combined citations inside a single bracket and hallucinated a non-existent file name (`02-returns-policy-trailplus.md` instead of `09-trailplus-membership.md`). It also cited a policy document (`08-order-changes-and-cancellations.md`) for an order status lookup retrieved from the tool database.
* **Root Cause**: LLM generation occasionally combined multiple sources in a single citation bracket, hallucinated file names, or appended spurious citations for database lookup facts.
* **Fix**: Tightened the system instructions in `src/agent.py` to command the model to output separate brackets for each citation and forbid citing policies for tool lookup results. Added a post-processing filter in `agent.py` that splits combined citations, verifies each file name exists on disk and was actually retrieved during the turn, and removes invalid/spurious citation brackets.
* **Regression Test**: Covered by verifying that all active test case responses contain only valid, retrieved citations.

---

## 6. Known Limitations & Production Enhancements

1. **Automated Evaluator Paraphrasing Constraints**: The automated concept checker is designed as a strict, lightweight keyword and number matcher rather than using heavy semantic LLM grading. Consequently, it can yield false negatives on valid semantic paraphrases if the response uses alternative wording for expected key phrases. This is a deliberate design trade-off to keep the evaluator objective, fast, and prevent overfitting.
2. **Static Vector Cache**: The embeddings cache `kb_embeddings.json` is generated once and saved. In a production pipeline, this should be automated via file watchers or database hooks so updates to the markdown files trigger automatic re-indexing.
3. **Session State Management**: Chat history is passed as a Python list in-memory. For production multi-user systems, we would back this history with a Redis or PostgreSQL database session store.
4. **Strict Order ID Authentication**: Currently, possession of an order ID is treated as sufficient authentication. In production, we would require supplementary verification (e.g. verifying the zip code or email associated with the order ID before disclosing tracking details).

---

## 7. AI Coding Tools Disclosure

* **Tool Used**: Antigravity AI assistant.
* **Purpose**: Used for writing the custom retrieval pipeline, managing test suites, and resolving character encoding issues (`UnicodeEncodeError` on CP1252 consoles).
* **Wrong/Incomplete AI Suggestion**: The model initially recommended using `models/gemini-3.6-flash`, which hit the strict 20 RPD daily quota. The model also did not anticipate the CP1252 character map print error when printing the emoji `🎉` on Windows consoles.

---

## 8. Interactive Chat Demo & Screenshots

### 🎥 Live Video Walkthrough
<video src="Aster%20%26%20Row%20-%20AI%20Support%20Assistant%20.mp4" controls="controls" style="max-width: 100%; border-radius: 12px;"></video>

---

### 📸 Interface Screenshots

#### 1. Policy & Standard Return Inquiries
![Standard Return Query](Screenshot%201.png)

#### 2. Member Benefits & Status Tracking
![Member Benefits & Order Tracking](Screenshot%202.png)

#### 3. Exception Handling & Support Escalation
![Exception Status & Escalation](Screenshot%203.png)

#### 4. Safeguards, Data Privacy & Prompt Defenses
![Privacy Protection & Safeguards](Screenshot%205.png)
