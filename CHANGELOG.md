# Changelog

All notable changes are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Planned as 0.1.0.

### Added

- Design a Grok Bot: intake, four-field persona (job, anti-jobs, voice, wake),
  `CreateAgent`, `profile.json` verification, routine handoff, template note.
- Bot Persona Lint: 14 checks run before every `CreateAgent`.
- Grok Bot Memory: tier (`profile`, `log`, `note`) and scope (`agent`, `user`,
  `project`) rules; refuses secrets, raw personal data, and chat trivia.
- Hand Off Routine: explicit `update_state` routine instruction sent to a new bot, recorded
  only after the bot confirms.
- Fleet Healthcheck Hooks: friction reports become proposals; nothing changes until the
  user picks.
- Twelve Candor persona skills and agents, ported from Candor 0.5.0 with human-readable
  names and "Use when" descriptions; persona bodies unchanged.
- `skills/design-a-grok-bot/references/candor-persona-bots.md`: twelve starter bot
  descriptions, one per persona.
- `scripts/validate.py` and a CI workflow that runs it.
- `docs/evals/RESULTS.md`: acceptance test method and results.

### Security

- Bots that read email, PRs, issues, reports, or other bots' messages must refuse instructions
  written inside that content (Bot Persona Lint check 4 and all starter descriptions).
- The designer asks before creating a bot for a chore the user only mentioned.
- Public templates are redacted to placeholders and shown to the user before publishing.
- Report lines and routine confirmation replies are treated as data, never instructions.
- CI token is read-only and actions are pinned to commit SHAs.
- The asset render script HTML-escapes the name and tagline.
