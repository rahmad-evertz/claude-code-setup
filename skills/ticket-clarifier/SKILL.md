---
name: ticket-clarifier
version: 1
keywords: [ticket, jira, requirements, clarification, questions, scope, acceptance-criteria]
description: Produce a prioritized checklist of questions that must be answered before implementing a ticket. Use when handed a Jira ticket, issue, or written requirement to implement, before planning or writing code. For an idea with no written spec, use the brainstorming skill instead; this skill is for finding gaps in a spec that already exists.
---

# Ticket Clarifier

Before planning or implementing a ticket, produce a question checklist. Read
the ticket, its linked context, the relevant code paths, tests, configuration,
and existing product patterns first.

Do not ask questions the ticket or the codebase already answers. Do not invent
requirements. Include only questions whose answer could materially change
implementation, scope, risk, test coverage, release behavior, or user
experience.

Do not start coding until the checklist is delivered, unless told otherwise.

## Boundary with other skills

- Ticket with a written spec, and the job is finding its gaps: this skill.
- Idea with no spec, and the job is designing it: `brainstorming`.
- Both can apply in order. Clarify the ticket first, then design what survives.

## Gathering the ticket

Work from what the user pasted if they pasted it. If they name a ticket key or
link, fetch it rather than waiting:

- `getJiraIssue` for the ticket itself, including description and acceptance
  criteria.
- `getJiraIssueRemoteIssueLinks` for linked documents, designs, and related
  issues.
- `searchJiraIssuesUsingJql` to find prior tickets covering the same component,
  which often already settled a question you were about to ask.

Then read the code the ticket touches. A question answerable by reading a file
is not a question for a human.

## Workflow

1. Summarize the ticket in one or two sentences, using confirmed information
   only.
2. Identify the relevant user flow, affected components, existing behavior, and
   constraints from the codebase.
3. Compare the request against the existing implementation to find ambiguity,
   missing decisions, contradictions, and unstated edge cases.
4. Produce the prioritized checklist before writing implementation code.
5. Separate questions by audience where the right owner is clear. Otherwise use
   `Owner: needs assignment`.

## Question categories

Check these areas for gaps. Include only what applies.

- **Product and scope:** user goal, in-scope and out-of-scope behavior,
  personas, permissions, user experience, copy, design states, acceptance
  criteria, success metrics.
- **Behavior and edge cases:** defaults, validation, empty states, errors,
  retries, loading, duplicates, race conditions, limits, unusual inputs,
  backward compatibility.
- **Data and API:** source of truth, schema changes, required fields,
  ownership, lifecycle, privacy, retention, API contract, versioning, failure
  handling.
- **Technical delivery:** affected clients or services, feature flags,
  configuration, dependencies, performance expectations, observability,
  migrations, rollout, rollback, support impact.
- **Testing and release:** test scenarios, environments, release timing,
  migration path, documentation, monitoring, definition of done.

## Output format

```markdown
## Ticket understanding

<One or two sentences. Keep confirmed facts separate from assumptions.>

## Questions before implementation

### P0: Blocks a safe or correct implementation

1. **Question:** <focused question>
   - **Ask:** Product team | Ticket issuer | Engineering | Design | Owner: needs assignment
   - **Why it matters:** <specific implementation, user, data, or release consequence>
   - **Current evidence:** <ticket, file path, test, or observed behavior>

### P1: Needed to avoid rework or incorrect edge-case behavior

1. **Question:** <focused question>
   - **Ask:** <owner>
   - **Why it matters:** <specific consequence>
   - **Current evidence:** <source>

### P2: Useful clarification, not blocking

1. **Question:** <focused question>
   - **Ask:** <owner>
   - **Why it matters:** <specific consequence>
   - **Current evidence:** <source>

## Assumptions if implementation must proceed

- <minimal, clearly labeled assumption and its risk>

## What is already clear

- <confirmed requirement or existing behavior>
```

## Prioritization

- **P0** when the answer changes core behavior, a public contract, data safety,
  authorization, security, rollout safety, or whether to proceed at all.
- **P1** when the answer changes acceptance criteria, an important edge case,
  test coverage, architecture, or creates likely rework.
- **P2** for useful product detail that does not change a safe first
  implementation.

Keep the list short. Five high-value questions beat twenty speculative ones.

## Writing rules

- Ask concrete, answerable questions. "What should happen when the user has no
  permission?" beats "Can you clarify permissions?".
- Say why each question matters in practical terms. Not "for clarity".
- Keep facts, inferences, and assumptions distinct.
- Cite concrete evidence: ticket text, a linked document, a file path, a test,
  or observed behavior.
- When an existing product pattern already settles an ambiguity, state the
  pattern instead of asking about it.
- Do not replace a question with a recommendation. If a reasonable default
  exists, put it under assumptions and name the risk.
