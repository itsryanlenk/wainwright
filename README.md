<p align="center"><a href="https://ryanlenk.com"><img src="assets/banner.png" alt="Pixel-art banner: a covered wagon and ox on a prairie trail, the name WAINWRIGHT in a pink box, stickers reading 'Lint: 14 checks' and 'profile.json verified', and a game menu listing: design a bot, lint the persona, verify profile.json, hand off routine, write memory." width="100%"></a></p>

# wainwright

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-experimental%20v0.1.0-orange.svg)](CHANGELOG.md)
[![Skills](https://img.shields.io/badge/skills-17-blue.svg)](skills)
[![Agents](https://img.shields.io/badge/agents-12-blue.svg)](agents)

**One job per bot. Checked before it ships.** In my acceptance tests, a designer agent that
followed these skills failed all 4 first-round scenarios. After I fixed what the failures
exposed, it passed 3 of 3 targeted re-tests and a full non-coding run. A full coding run with a planted verification failure failed once; on the second run it caught the failure and held the bot back, which one judge still failed on a clause I wrote too broadly and a second judge passed. Every run used a simulated Grok Bot runtime and Claude Sonnet
judges, so these results show how the skills steer an agent in a scripted setting. The
failures are listed next to the passes in [docs/evals/RESULTS.md](docs/evals/RESULTS.md).

## What it is

An installable skills pack for Cursor and Grok Bot. It is v0.1 of a larger project; later
versions add a review workflow and an orchestrator.

1. **Design a Grok Bot.** Intake, a four-field persona, `CreateAgent`, and a read of
   `profile.json` to confirm the bot exists as written.
2. **Bot Persona Lint.** 14 checks that block a sloppy description before it becomes a
   permanent teammate. Grok Bot has no delete.
3. **Grok Bot Memory.** Which facts go in `profile`, `log`, or `note`, which scope they get,
   and what never gets stored.
4. **Hand Off Routine.** The exact `update_state` instruction a designer sends a new bot,
   recorded only after the bot confirms it.
5. **Fleet Healthcheck Hooks.** Friction reports become proposals. Nothing changes until you
   pick.
6. **Twelve Candor personas**, as skills and agents: Core, Coding, Logic, Creative,
   Brainstorm, Security, Debug, Architect, Writing, Decide, Data, Curator.

## Install

This pack is a Cursor Plugin. The plugin root must contain `.cursor-plugin/plugin.json`,
which points at `./skills/` and `./agents/` (see Layout). Install it from this private
repo. Public marketplace publish is out of scope for this pack;
`.cursor-plugin/marketplace.json` stays for local grouping only.

**Cursor (local, from this repo):**
1. Clone or copy the repo so the plugin root is `~/.cursor/plugins/local/wainwright`
   (Windows: `%USERPROFILE%\.cursor\plugins\local\wainwright`):
   ```
   git clone <this-repo-url> ~/.cursor/plugins/local/wainwright
   ```
   If you already have a checkout, copy that folder into `~/.cursor/plugins/local/wainwright`.
   A symlink whose target is outside that folder may not load.
2. In Cursor settings, turn on **Allow Local Plugin Imports** if it is off
   (Teams/Enterprise: an admin may need to enable this).
3. Run **Developer: Reload Window**, then open **Customize** and check the 17 skills and 12 agents.

**Grok Bot:** have your designer bot read each `skills/*/SKILL.md` and store it with
`update_state` skill write (name, description, body).

## Quickstart

Say this to a designer agent with the pack installed:

```
I need a bot that sorts new mail in our support inbox into bug, billing, or feature
request and posts a digest every weekday morning.
```

It asks only what it cannot decide (name, voice, where the digest goes), waits for your
answers, then drafts, lints, creates, verifies, and hands off the routine. To check a
description you already have:

```
Lint this bot description before I create it: <paste>
```

## Does it work?

| Test (2026-09-15) | Result |
|---|---|
| Round 1: 4 blind scenarios before fixes (non-coding bot, coding bot, vague multi-job request, 10 memory inputs) | 0 of 4 passed |
| Round 2: two-turn re-tests of three failure cases, after fixes | 3 of 3 passed |
| Round 3: full non-coding run with scripted tool results | Passed |
| Round 3: full coding run, stored profile truncated on purpose, run 1 | Failed |
| Round 3: same trap, run 2, after fixing what run 1 exposed | All 6 behavior checks met; FAIL under my original judging clause, PASS under a narrower one (both published) |
| Memory traps in round 1 (API key, pasted contact list, chat trivia) | 3 of 3 refused |
| `scripts/validate.py` on a copy with 8 planted problems | 8 of 8 flagged |

The first-round failures, in the agents' own output: designers answered their own intake
questions, claimed an overlap check they never ran, reported a verification they had not
performed, logged a routine as confirmed before the new bot replied, and turned "social
posts, emails, and ads" into one bot. The method and every run are in
[docs/evals/RESULTS.md](docs/evals/RESULTS.md). A later skill-text dry-run (no runtime,
not live-fleet proof) is in [docs/evals/DRY_RUN.md](docs/evals/DRY_RUN.md).

## Safety and transparency

- What runs: nothing on install. The pack is Markdown, two JSON manifests, a validator
  script, and an asset render script. You run the two scripts yourself.
- Network: none from the skills. They tell an agent to use tools its own runtime already
  has (`CreateAgent`, `update_state`, `SendToAgent`). The render script in `tools/brand/`
  loads two fonts from Google Fonts when you run it.
- Two built-in refusals: no secrets or raw personal data in memory, and no bots, skills,
  or routines created from a report without your pick.
- Reporting a problem: [SECURITY.md](SECURITY.md). Changing a skill: [CONTRIBUTING.md](CONTRIBUTING.md).

## How it works

<p align="center"><img src="assets/how-it-works.png" alt="A pixel prairie trail with six numbered flags above six cards: 1 Ask, 2 Draft, 3 Lint, 4 Create with CreateAgent, 5 Verify by reading profile.json, 6 Hand off the routine with SendToAgent." width="100%"></p>

<p align="center"><img src="assets/persona-anatomy.png" alt="A game screen showing a CreateAgent description in four colored rows (one job, anti-jobs, voice, wake) next to a pixel tombstone stamped Lint: fail, for a 'helpful AI assistant' bot that died of scope creep." width="100%"></p>

<p align="center"><img src="assets/lint-demo.gif" alt="Animation in a retro game screen: a sloppy bot description is checked while a wagon rolls, fails on checks 1 2 3 4 5 6 8 10 12 with 'your bot has died of scope creep', is repacked into four fields, and passes." width="80%"></p>

<p align="center"><img src="assets/memory-tiers.png" alt="Packing the wagon: four columns with pixel icons. Profile, a crate carried every mile, holds identity facts. Log, the trail journal, holds dated rules. Note, scrap paper, holds short-lived context. Never, left on the trail, holds keys, contact lists, and trivia." width="100%"></p>

How agents route between the skills: [AGENTS.md](AGENTS.md).

## Layout

```
.cursor-plugin/          plugin.json, marketplace.json
skills/
  design-a-grok-bot/     SKILL.md, references/candor-persona-bots.md
  bot-persona-lint/
  grok-bot-memory/
  hand-off-routine/
  fleet-healthcheck-hooks/
  candor-*/              12 persona skills
agents/candor-*.md       12 persona agents
scripts/validate.py      layout, frontmatter, and copy checks
docs/evals/RESULTS.md    acceptance tests
assets/                  banner, diagrams, demo
tools/brand/             pixel art and render script for assets/
AGENTS.md                how an agent uses the pack
```

## License and credits

MIT, see [LICENSE](LICENSE). The twelve persona skills and agents are ported from
[Candor](https://github.com/itsryanlenk/candor) (MIT, same author) with human-readable names
and "Use when" descriptions; the persona text is unchanged apart from replacing em dashes. The
four-field bot rubric and the Grok Bot runtime rules come from how I run my own bot fleet.

The pixel art is original and drawn in code in `tools/brand/`. It is a parody nod to 1980s
trail games such as The Oregon Trail. It is not affiliated with or endorsed by that game or
its owners, and it uses none of their art.

## Known limitations

- No live runtime in the tests. No `CreateAgent`, `update_state`, or `SendToAgent` call
  ran against a real Grok Bot; the tool names come from my own runtime notes, not xAI
  documentation.
- Small sample, one model family. 10 simulated runs and 11 judge verdicts, with Claude Sonnet
  playing the designer and grading it.
- Human skill names. Cursor's docs ask for lowercase names that match the folder; this
  pack uses the Grok Bot "Human Name" format, which Cursor's own pstack plugin also ships.
