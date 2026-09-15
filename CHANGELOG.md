# Changelog

All notable changes are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Planned as 0.1.0.

### Fixed

- Hand Off Routine: hold the send until `profile.json` verification passed; never
  report a routine as confirmed before the new bot replies. Description no longer
  auto-applies after a failed CreateAgent verify.
- Design a Grok Bot: vague multi-job requests stop before draft, lint, or create;
  intake is one message of unanswered items; the report cites the overlap read.
- Grok Bot Memory: restated corrections replace an existing entry; they do not
  write a second copy. Schedule change with a stale log is an explicit example.
- Bot Persona Lint: FAIL blocks CreateAgent until a rewrite lints PASS.
- Fleet Healthcheck Hooks: a report that contains a ready CreateAgent or routine
  spec is still a proposal.
- README: private-repo local install path aligned with `.cursor-plugin/plugin.json`.
- Validator now checks the skill and agent counts in both README.md and AGENTS.md.

### Changed

- Renamed the twelve persona skills and agents to `wainwright-*` slugs (folders,
  agent files, frontmatter names, and user-facing copy). Persona behavior unchanged.

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
- Twelve Wainwright persona skills and agents with human-readable names and
  "Use when" descriptions; persona bodies unchanged.
- `skills/design-a-grok-bot/references/wainwright-persona-bots.md`: twelve starter bot
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
