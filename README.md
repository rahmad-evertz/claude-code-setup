# Claude Code setup

Global rules and custom skills for [Claude Code](https://claude.com/claude-code).

`CLAUDE.md` loads into every session. `skills/` load on demand, when the task
matches a skill's description or when invoked by name.

## Install

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
cp -r skills/* ~/.claude/skills/
```

Skills are picked up immediately. `CLAUDE.md` applies from the next session,
since instruction files are read at startup.

## Rules

`CLAUDE.md` is one file, 13 sections. What it constrains:

| Section | Covers |
| --- | --- |
| Characters | No em dashes, en dashes, or emojis, anywhere |
| Voice | Plainspoken and technical, confident where evidence supports it |
| Never write | Stock openers, closing offers, filler praise, buzzwords |
| Response shape | Answer first, caveats after, bullets only where they help |
| Communication | Smallest reasonable assumption, stated. Ask only when it changes the work |
| Engineering workflow | Read before changing, narrow diffs, reuse existing patterns |
| Implementation standards | Validate at boundaries, handle failures deliberately, no premature optimisation |
| Comments and docstrings | Why not what, nothing on obvious code, no boilerplate |
| Testing and verification | Never claim a build, test, or fix succeeded unless verified |
| Follow the project | A project's own CLAUDE.md wins on conflict |
| Git | Never commit or push unasked, one-line imperative messages, no AI attribution |
| Documentation | Concise and factual, no throat-clearing |
| Before sending, strip | Final self-check list |

## Skills

| Skill | Trigger | What it does |
| --- | --- | --- |
| `copy` | `/copy`, "copy that" | Puts the previous response on the system clipboard, read straight from the session transcript |
| `explain-pr` | "explain this PR" | Plain-language walkthrough for someone learning the codebase. Seven-section overview, then per-file detail |
| `investigation-log` | A multi-step investigation | Maintains `INVESTIGATION.md` with findings, hypotheses, failed checks, and open questions |
| `ticket-clarifier` | Being handed a ticket | Prioritised checklist of questions to answer before writing code, P0 to P2, with owners |

## Requirements and limits

- `copy` is Linux and X11 only. It needs `xclip` installed and `DISPLAY` set.
  It will not work over SSH or on Wayland without changes. It detaches xclip
  with `setsid` so the clipboard survives the shell exiting, which X11 needs
  because the selection is owned by a live process.
- `explain-pr` uses the `gh` CLI and expects it to be authenticated.
- `ticket-clarifier` reads Jira tickets through an MCP connector when one is
  configured. Without one, paste the ticket text.
- `investigation-log` relies on a pointer line in the Engineering workflow
  section of `CLAUDE.md` to fire reliably. Installing the skill without
  `CLAUDE.md` means it only triggers when its description matches, which is
  less dependable for behaviour meant to run across a whole session.
