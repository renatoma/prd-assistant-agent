# PRD Assistant Agent — Product Requirements Document

## Problem Statement
Turning a rough feature idea into a structured, implementation-ready PRD (problem statement, user stories, acceptance criteria, and a risk flag) takes time and consistent judgment. This project builds a small AI agent that automates the first draft of that process, using tools it decides when and how to call, so the output is grounded in real market context and flagged for risk, not just generated text.

## Goals
1. Given a one- or two-sentence feature idea, produce a structured PRD draft in under 2 minutes.
2. The agent should use at least 2 of its 3 available tools per run, chosen appropriately based on the input (not hardcoded).
3. Output should be specific enough to hand to an engineer without immediate rework — a real test of quality, not just "did it run."

## Non-Goals (Out of Scope for v1)
- No fine-tuning or custom model training — uses the Claude API as-is with tool use.
- No persistent memory/database across sessions — each run is stateless.
- No multi-user auth or deployment — local use only, run via CLI or local Streamlit app.

## Target User
Me (Renato), for rapid feature ideation and as a portfolio piece demonstrating hands-on agentic AI product work.

## Success Metrics
- Runs successfully on 8-10 varied test inputs (ranging from vague to detailed) without crashing.
- At least 80% of test runs use 2+ tools appropriately (not just defaulting to `format_prd`).
- Output PRDs are specific enough that a reviewer (me) would rate them "usable with minor edits" on at least 6 of 10 test runs.
- A documented before/after example showing at least one iteration where a tool description or system prompt was changed to fix a failure mode.

## Functional Requirements

### Input
- A single text string: a rough feature idea (e.g., "let users see a live preview of their changes before publishing").

### Tools

**1. `web_search(query: str)`**
- Purpose: pull brief market/competitor context relevant to the feature idea.
- Implementation: Tavily free-tier API (or similar search API).
- Returns: top 3-5 result snippets with source names.

**2. `format_prd(problem: str, user_stories: list[str], acceptance_criteria: list[str])`**
- Purpose: assemble the final structured PRD document from the pieces Claude has drafted.
- Implementation: pure Python function, template-based (Markdown output).
- Returns: a formatted Markdown string.

**3. `flag_risks(text: str)`**
- Purpose: scan the drafted PRD for keywords suggesting compliance, security, or technical-complexity risk (e.g., "payment," "PII," "third-party integration," "regulatory").
- Implementation: simple keyword/heuristic match (no ML needed) — a list of ~20-30 risk terms, returns which ones matched and where.
- Returns: list of flagged terms + a short note on why each might matter.

### Agent Behavior
- Claude receives the feature idea and system instructions describing its role (product analyst) and its available tools.
- Claude decides which tools to call and in what order based on the input — not a fixed pipeline.
- Typical happy path: `web_search` → draft problem statement/user stories/acceptance criteria → `format_prd` → `flag_risks` on the result → final output includes the formatted PRD plus any risk flags.
- Final output returned to the user as a single Markdown document.

### Interface
- v1: command-line script — input via prompt, output printed to terminal and saved to a local `.md` file.
- v2 (stretch): minimal Streamlit UI — text box in, rendered Markdown PRD out. This is what gets demoed in interviews.

## Architecture (one diagram, described)
```
User input (rough idea)
        |
        v
Claude (w/ tool-use loop)
    |         |          |
    v         v          v
web_search  format_prd  flag_risks
    |         |          |
    -----------------------
              |
              v
   Final PRD (Markdown, saved to file)
```

## Build Plan / Milestones
1. Write this PRD (done) — first commit.
2. Get Anthropic API key, set up project (`pip install anthropic`, basic repo structure).
3. Build and unit-test `format_prd` standalone (no Claude yet) — pass in sample data, confirm output reads well.
4. Build and unit-test `flag_risks` standalone — run against 3-4 sample PRD texts, confirm it catches obvious terms.
5. Build and test `web_search` standalone — confirm it returns usable snippets for a sample query.
6. Wire up the Claude tool-use loop with all 3 tools registered.
7. Run against 8-10 varied test inputs (see test set below). Log which tools got called, in what order, and rate each output.
8. Identify at least one failure mode (e.g., agent skips `web_search` on ideas that clearly need market context, or `flag_risks` over-triggers on harmless text) and iterate on tool descriptions/system prompt to fix it. Document the before/after.
9. Add the Streamlit front end.
10. Write the README (problem, architecture diagram, 2-3 example runs, the iteration story from step 8).
11. Push to GitHub with meaningful incremental commits.

## Test Set (draft — refine once building)
1. "Let users see a live preview of their changes before publishing."
2. "Add a way for teams to leave comments on a shared doc."
3. "We want to accept Apple Pay at checkout." (should trigger risk flag — payments)
4. "Add dark mode."
5. "Let admins export user activity logs." (should trigger risk flag — PII/compliance)
6. "Speed up page load on mobile."
7. "Integrate with a third-party calendar API." (should trigger risk flag — third-party integration)
8. "Give users a way to undo their last action."
9. "Add multi-language support."
10. A deliberately vague one: "Make the app better."

## Risks / Open Questions
- Free-tier search API rate limits may require caching or a fallback if testing hits limits.
- Keyword-based risk flagging will have false positives/negatives — that's expected and worth noting as a known limitation in the README, not something to over-engineer for v1.
