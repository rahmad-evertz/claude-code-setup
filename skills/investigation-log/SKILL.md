---
name: investigation-log
version: 1
keywords: [investigation, debugging, log, findings, evidence, handoff, root-cause]
description: Maintain a running INVESTIGATION.md log of findings, hypotheses, failed checks, issues, decisions, and open questions while debugging or investigating. Use when starting a multi-step investigation or debugging session, when a bug's cause is not obvious, when work will be handed off or resumed later, or whenever asked to keep, update, or write up an investigation log.
---

# Investigation Log

Keep `INVESTIGATION.md` at the repository root, unless the repository already
defines an investigation-log location. Create the file if it does not exist.

## Starting work

1. Read the project's own instructions and any current `INVESTIGATION.md`
   before writing to it.
2. Add a new session section with the task, date, scope, and current status.
3. Preserve prior sessions. Do not rewrite, delete, or reorder historical
   entries unless asked to.

## Structure

```markdown
# Investigation Log

## YYYY-MM-DD: <short task name>

Status: investigating | blocked | resolved | handed off

### Goal

<What is being investigated or changed?>

### Findings

- [confirmed] <fact>
  Evidence: <file, command output, test, log, or link>
- [hypothesis] <unproven explanation>
  Evidence: <why it seems plausible>
  Next check: <specific verification step>
- [failed check] <what was tried and what happened>
  Evidence: <error, output, or observed behavior>

### Issues

- <bug, risk, blocker, or unexpected behavior>
  Impact: <affected behavior, user, or system>
  Status: open | mitigated | resolved

### Decisions

- <decision and short reason>

### Open questions

- <specific unanswered question, and owner or next step if known>

### Verification

- Ran: `<command>`: pass | fail | not run
- Remaining: <checks not run, and why>
```

## When to update

Update the log immediately after a meaningful discovery or a failed
investigation step. Do not batch it to the end. Record:

- Confirmed findings, with evidence.
- Hypotheses, labeled as unconfirmed.
- Failed commands, experiments, searches, tests, or debugging paths, when they
  rule out a possibility or reveal a blocker. A ruled-out path is worth as much
  to the next person as a confirmed one.
- Issues, with impact and current status.
- Decisions that affect implementation or scope.
- Open questions that available evidence cannot settle.

Do not log routine file reads, obvious edits, or low-value activity. Short and
useful beats complete.

## Evidence and accuracy

- Keep facts, hypotheses, and assumptions separate. Never write a hypothesis as
  confirmed.
- Cite the source of every finding: a file path, test name, command, log
  reference, ticket, or concrete observed behavior.
- Do not record a test, build, deployment, or fix as successful unless it was
  actually verified.
- Never write secrets, access tokens, passwords, private keys, or raw customer
  data into the log. Replace a sensitive value with a short redaction note.
- Do not paste large command output. Record the meaningful result and where it
  came from.

## Completion

Before finishing the task:

1. Update the session status.
2. Mark resolved issues clearly. Leave unresolved issues open.
3. Record the verification performed and the checks not run.
4. In the final response, give a short summary and point to
   `INVESTIGATION.md`. Do not repeat the full log in the reply.
