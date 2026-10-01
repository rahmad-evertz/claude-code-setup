---
name: copy
description: Copy Claude's previous response to the system clipboard. Use when the user types /copy, or says "copy that", "copy your last response", or asks to put the previous answer on the clipboard.
---

# Copy last response

Run the helper and report what it prints:

```bash
python3 ~/.claude/skills/copy/copy_response.py
```

It reads the current session transcript, takes the final prose block of the
previous response, and puts it on the X11 clipboard using xclip. Raw markdown,
byte for byte as written. Thinking and tool output are never included.

Report the character count and whether verification passed. Do not paste the
copied text back into the reply, the user already has it on the clipboard.

If it reports that DISPLAY is unset or xclip is missing, say so plainly instead
of retrying.

To copy from a different session, pass the transcript path as an argument.
