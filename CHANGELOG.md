# Changelog

All notable changes are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Planned as 0.1.0.

### Fixed

- README Install and DRY_RUN no longer call this pack a private repo. Install is
  from this public GitHub repo via the local plugin path; marketplace listing
  stays out of scope.
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

- Wainwright Onboard: hiring language (roles, undo-proof hire, sidebar-Delete),
  plain pitch, defaults, one widget, progress checklist, and a required
  `SendToAgent` Teammate Focus Onboard after each verified `CreateAgent`.
- Wainwright Manager: seamless onboard plus mandatory focus handoff.
- Design a Grok Bot: after verify, Manager or designer sends Teammate Focus
  Onboard. `CreateAgent` is a hire the designer cannot undo; the human can
  sidebar-Delete.
- README: short Grok Bot setup section (Manager first, pick menu, each hire
  focuses on first open). Marketplace stays out of scope.
- Renamed the twelve persona skills and agents to `wainwright-*` slugs (folders,
  agent files, frontmatter names, and user-facing copy). Persona behavior unchanged.
- Regenerated `assets/` PNG and GIF files from `tools/brand/` so rasters match
  the Wainwright templates (social preview sticker included).

### Added

- Teammate Focus Onboard: first user message restates one job and anti-jobs; at
  most three focus questions; prefer narrower; update profile, memory, and
  routine; tell the human they can sidebar-Delete. Auto-applies once when
  Manager hands off.
- Wainwright Onboard: first-wake pick menu, local plugin confirm, create only
  user-picked teammates; paused routines and one fleet checkup are optional.
- Wainwright Manager agent: four-field orchestrator persona for onboard and fleet
  orchestration (not the Core / Straight Shooter stance).
- README: Grok Bot setup section pointing at Manager, the pick menu, and per-hire
  focus.
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
- `docs/evals/RESULTS.md`: live Grok Bot canary (2026-09-15) on a real fleet, next to
  the simulated Claude Sonnet acceptance tests.
- README install copy names local plugin, Grok Bot skill write / workflows, and the
  Manager onboard pick menu. Marketplace listing stays out of scope.

### Security

- Bots that read email, PRs, issues, reports, or other bots' messages must refuse instructions
  written inside that content (Bot Persona Lint check 4 and all starter descriptions).
- The designer asks before creating a bot for a chore the user only mentioned.
- Public templates are redacted to placeholders and shown to the user before publishing.
- Report lines and routine confirmation replies are treated as data, never instructions.
- CI token is read-only and actions are pinned to commit SHAs.
- The asset render script HTML-escapes the name and tagline.
