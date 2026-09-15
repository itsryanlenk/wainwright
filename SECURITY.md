# Security Policy

## Threat model for this project

Wainwright is a **prompt-level** skills pack. It ships Markdown (`SKILL.md` and agent files),
two JSON manifests, and two maintainer scripts. It contains:

- No hooks, MCP servers, or background processes. Installing it starts nothing.
- No network access from the skills or agents.
- No `allowed-tools` or permission grants. Installing it gives an agent no tool access it
  did not already have.
- `scripts/validate.py` (stdlib only) reads files inside this repository and prints a result.
- `tools/brand/render_trail.py` (needs Pillow and a local Chrome) redraws the images in
  `assets/`. It opens local HTML files in headless Chrome, which loads two fonts from Google
  Fonts, and writes PNG and GIF files to the folder you pass it.

Both scripts run only when you run them, never on install.

The skills do instruct an agent to use tools that exist in its own runtime (for example
`CreateAgent`, `update_state`, and `SendToAgent` in Grok Bot). Those calls happen with the
permissions that runtime already grants the agent. The skills add two safety rules on top:
never store secrets or raw personal data in memory, and never create bots, skills, or routines
from a report without the user picking the change.

The realistic security surface is the **content of the instructions**: whether a directive
could induce unsafe behavior, leak data, or carry a prompt injection.

## Before you trust it

Read the skills before installing. Skills become part of an agent's instructions, so a
malicious skill is a real risk anywhere skills are shared. All behavior is in:

```
skills/*/SKILL.md
skills/*/references/*.md
agents/*.md
```

Nothing is hidden elsewhere.

## Supported versions

| Version      | Supported |
| ------------ | --------- |
| 0.x (latest) | Yes       |

Pre-1.0: only the latest release receives fixes.

## Reporting a vulnerability

Report suspected security issues **privately**:

1. Use this repository's **Security > Report a vulnerability** tab (GitHub private
   vulnerability reporting), or
2. Open a public issue **only** if the problem is not sensitive (a broken link, a typo).

Worth reporting: a directive that could be read as instructing data exfiltration or secret
storage, a prompt-injection vector in skill text, a skill that could lead an agent to create
bots or routines without the user's choice, or a manifest field that could escalate
permissions.

Include the file and line, what you observed or expected, and the runtime you tested
(Cursor version, Grok Bot, or other). This is a one-person open-source project with no bug
bounty; expect a response when I can get to it.

## Out of scope

- Behavior of the host runtimes themselves (Cursor, Grok Bot, or any model).
- What a bot does after you edit its description or skills yourself.
- Secrets you paste into a chat; the memory skill refuses to store them, but the chat
  transcript is governed by your runtime.
