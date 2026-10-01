---
name: explain-pr
version: 1
keywords: [pull-request, explain, walkthrough, code-review, learning, diff, onboarding]
description: Explain a pull request in very simple, detailed, beginner-friendly words for someone who wrote (or is reading) the code but is still learning the codebase. Use whenever the user asks to understand, explain, or walk through a PR (its code, diffs, or review comments) in simple/plain/detailed language. Not for writing a PR description (that's a different task) and not for doing a critical/adversarial code review (see the pull-request-review skill for that).
---

# Explain PR

Walk the user through a pull request the way you'd explain it to someone who wrote the code
themselves but is still learning the wider codebase. The goal is understanding, not judgment.
This is not a code review, so don't grade the code or hunt for problems beyond what's asked below.

## Gathering the PR

The user may paste the PR's title/summary, diffs, and review comments directly. If they do, work
from what they gave you.

If instead they name or link a PR (a number, a branch, a URL), fetch it yourself rather than
waiting for a paste:
- `gh pr view <num> --json title,body,baseRefName,headRefName,commits,files,additions,deletions`
- `gh pr diff <num>` for the full diff (prefer this over reading files piecemeal; it's the
  authoritative change set and keeps you from missing a file)
- Review comments live in three different places. Check all of them, since `gh pr view` does not
  include any of them:
  - `gh api repos/<owner>/<repo>/pulls/<num>/comments`: inline code comments
  - `gh api repos/<owner>/<repo>/issues/<num>/comments`: general PR comments
  - `gh api repos/<owner>/<repo>/pulls/<num>/reviews`: formal review submissions
- If `gh api` fails with a TLS/certificate error (common on a corporate VPN proxy intercepting
  `api.github.com`), that's a network issue, not a real failure. Note it and retry, or fall back
  to what `gh pr view`/`gh pr diff` already returned.
- If the PR turns out to have no review comments at all, say so plainly rather than treating
  informal feedback from earlier in the conversation as if it were a posted review comment. Only
  fold in outside feedback (Slack, a call, etc.) if the user explicitly asks you to and tells you
  what it was.

If key context is missing after fetching (e.g. you can't tell why a change was made, or a
referenced ticket/discussion isn't available), ask the user rather than guessing.

## Output format

Lead with these seven sections. Do not repeat the PR description word for word.
Translate jargon and vague claims into concrete behavior.

1. **What problem does this solve?**
   The user or system problem, in 1 to 3 simple sentences.

2. **What changed?**
   The important behavior changes in plain words. Name a component only when
   naming it aids understanding.

3. **Before vs after**
   What happened before this PR, and what happens after it.

4. **Why is this needed?**
   The root cause, limitation, bug, or product requirement. If the PR does not
   make this clear, write "Not clear from the PR" rather than guessing.

5. **Risk and impact**
   Who or what could be affected: API changes, data changes, performance,
   security, rollout, compatibility. Write "No clear risk stated" when that is
   the case.

6. **How to verify it**
   The simplest practical way to confirm the change works. List the tests
   already present, kept separate from tests that should be added.

7. **Terms explained**
   One short sentence per unfamiliar acronym, domain term, or concept. Skip
   anything obvious from context.

Close with a single line answering "Should I be concerned about merging this?",
with the reason. One line, not a review.

For a large PR, open with a 2 sentence executive explanation before section 1,
then work through each meaningful part separately.

After the seven sections, go file by file when the PR is large or a file is
genuinely dense. Use the structure below for that walkthrough. Skip it for a
small PR the seven sections already cover.

## Explaining code (per file or per meaningful snippet)

For each file or snippet worth walking through, cover, in this order:

1. **What this code does**: in simple words, no jargon left unexplained.
2. **Why it was added or changed**: the motivation, if it's inferable from the diff, commit
   messages, PR description, or linked ticket. If it's not clear, say that plainly instead of
   inventing a reason.
3. **The flow, step by step**: walk through what happens, in order, like telling a story.
4. **How the parts connect**: how this file/method relates to the others touched in the PR.
5. **Important things to notice**: anything non-obvious a newer engineer should specifically
   register (a subtle ordering requirement, a deliberate design choice, a pattern reused
   elsewhere).
6. **Risks, edge cases, or possible bugs**: be honest here; this is the one place judgment is
   welcome, but stay descriptive ("here's what could go wrong and why") rather than prescriptive
   ("you must fix this").
7. **Line-by-line, when useful**: for a genuinely dense or trick-heavy snippet, break it down
   line by line. Skip this for straightforward code; don't pad every snippet with it.

For a large or many-file PR: give a one-paragraph high-level summary of the whole PR first (what
problem it solves, in plain terms), *then* break it into the smaller per-file walkthroughs above.
Present files in an order that tells a coherent story (e.g. the shared/foundational pieces before
the things that build on them) rather than alphabetical or diff order.

## Explaining review comments (per comment)

For each review comment, cover:

1. **What the reviewer means**: restate it in plain words.
2. **Why they're likely saying it**: the reasoning or concern behind it.
3. **What kind of comment it is**, one of: bug, style, readability, design, performance, testing,
   or a genuine question. Say which.
4. **Whether the user needs to change code or just reply**: be explicit about this; not every
   comment requires a code change.
5. **The exact change being asked for**, if any, concrete enough to act on.
6. **A short draft reply** the user could post as-is or edit. Match the tone of a normal
   engineering PR comment (direct, not overly formal, no filler).

## Style

- Write for someone who wrote this code but is still learning the surrounding codebase: assume
  programming knowledge, not codebase-specific or domain-specific knowledge.
- Plain language throughout; when a technical term is genuinely necessary, define it briefly
  inline the first time it's used.
- Detailed, but not padded. Favor clarity over length. Skip a section (e.g. line-by-line) when it
  wouldn't add anything.
- Short sentences. Common words.
- No em dashes.
- No vague praise. Not "improves robustness", "enhances performance", or
  "streamlines the flow". State exactly what improves and how.
- Never fabricate motivation, review comments, or context that isn't actually present in the PR or
  given by the user. Do not assume intent the PR, diff, linked ticket, or tests
  do not support.
- Label which statements are facts from the diff, which are reasonable
  inferences, and which are missing information.
