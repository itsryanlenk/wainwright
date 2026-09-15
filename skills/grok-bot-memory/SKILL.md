---
name: Grok Bot Memory
description: >-
  Use when about to write or forget durable memory with update_state, when the user
  states a preference, convention, or decision worth keeping, or when the user has to
  restate a correction. Auto-applies from context; do not wait for an @mention. Picks
  the right tier (profile, log, note) and scope (agent, user, project) and blocks
  secrets and trivia.
---
# Grok Bot Memory

Memory is written with `update_state` (memory: write or forget; tiers `profile | log | note`;
scopes `agent` (default) `| user | project`). Use the parameter names in the tool's own schema;
the shapes below are illustrative.

## Auto-apply from context
If a skill's description says it applies automatically when X happens, apply it the moment X
happens. Do not wait for an @mention or for the user to name the skill. This skill is one of
them: the trigger is any moment a durable fact appears.

## Step 1: Should this be stored at all?

Store it only if all three are true:
1. It will still be true and useful in a future conversation.
2. You would act differently next time without it.
3. It is not a secret, credential, or raw personal data.

**Never store**
- Secrets: passwords, API keys, tokens, recovery codes, private keys, session cookies.
- Raw PII dumps: pasted contact lists, full addresses, ID numbers, health or financial records.
- Chat trivia: what happened in this episode, greetings, moods, one-off task status.
- Anything already recorded in a system of record (a bot's `profile.json`, a repo, a ticket).
  Store a pointer instead, if a pointer is useful at all.

If the user asks you to store a secret, decline and suggest their secret manager.

## Step 2: Pick the tier

| Tier | Use for | Test |
|---|---|---|
| `profile` | Rare, foundational facts that must be present every turn. | Would nearly every turn go wrong without it? If not, it is not profile. |
| `log` | Dated, durable conventions and decisions. | Is it a rule or decision someone made, true until changed? Prefix the date. |
| `note` | Short-lived context for the current stretch of work. | Will it be stale within days? |

Default to `log` when unsure between `profile` and `log`. **Profile stays small.** If nearly
every turn would still go right without the fact, it is not profile.

Profile is for identity-level facts: the name a user goes by, pronouns, timezone, working
language. Style and behavior preferences ("prefers short answers", "no emoji", "no weekend
pings") are dated `log` entries, even when they apply to every reply.

## Step 3: Pick the scope

| Scope | Use for |
|---|---|
| `agent` (default) | Facts about this bot's role, job, or working conventions. |
| `user` | Facts every assistant serving this user should know (their name preference, timezone, a standing preference that applies across all bots). |
| `project` | Facts about one project that all bots on that project need. |

Role-specific facts stay `agent`-scoped even if they feel important.

## Step 4: Write one self-contained sentence
- One fact per write. No bundles.
- Self-contained: readable with no surrounding chat. Name the subject; resolve "it", "that", "yesterday".
- Dates are absolute (`2026-09-15`), never relative.
- No em dashes.

## Step 5: Corrections
When the user had to restate a correction ("I told you, no weekend pings"), write it once as a
`log` entry in the narrowest correct scope, so they never restate it again. Before writing,
check existing entries. Corrections replace; they do not accumulate:
- If the same correction is already stored, do nothing. Do not write a second copy.
- If an existing entry says the opposite or an older value, `forget` the stale one, then write
  the new one.

## Step 6: Forget
`forget` a fact when the user retracts it, when it is superseded, or when you find it was wrong.
Never leave two contradicting facts in memory.

## Examples

| Candidate | Verdict | Why |
|---|---|---|
| "The user's API key is sk-..." | Reject | Secret. |
| "User seemed stressed today." | Reject | Episode trivia. |
| "We fixed the login bug this afternoon." | Reject, or `note` at most | Episode status; the fix lives in the repo. |
| "Here are 40 customer emails for later." | Reject | Raw PII dump. |
| "User goes by Sam, not Samuel." | `profile`, `user` scope | Identity fact, every turn, every assistant. |
| "2026-09-15: User prefers short answers." | `log`, `user` scope | Style preference: a dated log entry, not profile. |
| "2026-09-15: Digest posts go out at 09:00 local, never on weekends." | `log`, `agent` scope | Dated convention for this bot. |
| "Digest is 09:00 now, not 08:00" (log already has 08:00) | Replace | `forget` the 08:00 log, then write a dated 09:00 log. Do not keep both. |
| "2026-09-15: All bots on the billing project read amounts in cents." | `log`, `project` scope | Project-wide convention. |
| "Waiting on the user to confirm the new channel name." | `note`, `agent` scope | Short-lived. |
| "User likes concise answers and wants no weekend pings and uses Linux and dislikes emoji." | Rewrite | Four facts in one; split and tier each. |
| "Remember what I said about that thing." | Rewrite | Not self-contained; ask what the fact is. |

Illustrative call shape:
```
update_state memory write  tier=log  scope=agent  text="2026-09-15: Digest posts go out at 09:00 local, never on weekends."
update_state memory forget tier=log  scope=agent  text="2026-09-01: Digest posts go out at 08:00 local."
```
