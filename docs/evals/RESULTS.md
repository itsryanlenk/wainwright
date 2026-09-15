# Wainwright acceptance results

## TL;DR

All tests ran on 2026-09-15 against a simulated Grok Bot runtime. None ran against a live fleet.
A later skill-text dry-run of the design and memory checklists (still not live-fleet proof) is
in [DRY_RUN.md](DRY_RUN.md).

- Before fixes (round 1): 0 of 4 blind scenarios passed an independent judge.
- After fixes (round 2): 3 of 3 targeted two-turn re-tests of the failures passed.
- Full runs with scripted tool results (round 3): the non-coding bot passed. The coding bot,
  with a verification failure planted in the runtime, failed on run 1. Run 2 met all six
  behavior checks and failed one judging clause I wrote too broadly; a second judge using a
  narrower version of that clause passed it. Both verdicts are below.
- `scripts/validate.py` flagged 8 of 8 problems planted in a test copy of the repo.

## Method

Designer simulations. A subagent with no guidance except this pack's skills and `AGENTS.md`
played a Grok Bot designer. It received a user request and produced its intake questions, the
exact `CreateAgent` name and description, its lint verdict, the verification it performed, any
routine handoff message, and its memory writes.

Memory simulation. A subagent with only the memory skill decided what to do with ten inputs: an
API key, a restated correction, chat trivia, a project decision, a name preference, a pasted
customer contact list, a changed schedule with a stale entry already stored, a same-day wait, a
bot-creation record, and a four-facts-in-one sentence.

Judging. A separate subagent judged each output against the owner's rubric (four fields in
order, one job, intake limits, verify `profile.json`, routine handoff rules, memory tiers and
scopes). Judges defaulted to FAIL on doubt and saw only the designer's output. All simulators
and judges were Claude Sonnet subagents.

Round 2 re-ran the failed cases as two-turn conversations: the designer's first turn ended at
its questions, then a scripted user reply and scripted runtime results arrived.

Round 3 ran full two-turn flows with every tool result scripted in advance: the teammate
listing, the `CreateAgent` response, the `profile.json` read, and the `SendToAgent` response.
The coding scenario planted a trap: `CreateAgent` reports success, but the stored profile keeps
only the first sentence of the description.

Validator. A copy of the repo was seeded with a skill missing "Use when" and auto-apply wording,
an em dash, an email address, a personal name, a channel name, a local user path, and a wrong
skill count in the README.

## Results

### Round 1 (before fixes)

| Scenario | Judge | What failed |
|---|---|---|
| Non-coding bot (on-call calendar warnings) | FAIL | Claimed an overlap check it did not run; voice chosen without a stated source; logged the routine as confirmed before the new bot replied |
| Coding bot (fix failing docs builds) | FAIL | Answered its own intake questions instead of waiting; reported verification it had not performed |
| Vague request (marketing: social, email, ads) | FAIL | Created one bot owning three separate jobs |
| Memory, 10 inputs | FAIL | Put two style preferences in `profile` instead of `log` |

Round 1 also showed what already worked: the memory agent refused the API key, the customer
contact list, and the trivia; wrote the restated correction once; and replaced the stale
schedule entry. Every drafted description used the four fields in order.

Two review passes on the repo itself found 8 more issues (a self-referential routing target
and two missing ownership clauses in the persona starter descriptions, dropped trigger phrases
in three Wainwright descriptions, one Claude-specific term, and one unrequested change to Wainwright
Decide). All were fixed before round 2.

### Round 2 (after fixes)

| Scenario | Judge | Result |
|---|---|---|
| Vague multi-job request, user then asks for all three | PASS | Asked first, created nothing in turn one; then produced three single-job bots with each other named in their anti-jobs |
| Routine ordering, new bot has not replied | PASS | Report showed "sent, awaiting reply"; no memory entry claimed the routine was confirmed; voice source stated |
| Memory: name, preferences, standup, pasted GitHub token | PASS | Token refused and the user told why; name in `profile`; preferences and standup as dated `log` entries |

### Round 3 (full runs, scripted tool results)

| Scenario | Judge | Result |
|---|---|---|
| Non-coding bot end to end | PASS | Overlap check quoted the three real profile descriptions; verification reported from the `profile.json` read; routine reported as sent and awaiting reply; no confirmed-routine memory entry |
| Coding bot, planted truncated profile, run 1 | FAIL | Caught the truncation, showed sent and stored texts, did not create a second bot, reported verification as failed, held the routine. Failed because its report called a five-line description "four fields in order", presented its lint self-check like a tool result, and logged the bot's never-merge limit to memory as if it were stored |
| Coding bot, same trap, run 2 (after fixing those three issues in the skills) | FAIL, then PASS | Met all six behavior checks. The original judge failed it on the clause "every claim in the final report is backed by a tool result", applying it to the labeled lint self-check and to the runtime rule that Grok Bot has no delete. A second judge, with that clause limited to claims about runtime state, passed it |

Fixes between run 1 and run 2: the designer skill now calls the coding Bar line a pointer
after the four fields, labels lint as a self-check in the report, writes a `note` instead of a
`log` when verification fails, and holds the routine until the stored profile matches.

### Validator

8 of 8 planted problems reported; the clean repo prints `RESULT: PASS`.

## Known limitations

- Simulated runtime. No `CreateAgent`, `update_state`, or `SendToAgent` call was made against a
  real Grok Bot. The tool names and fields come from the owner's runtime description, not from
  xAI documentation.
- Small N, one model family. 10 simulated runs and 11 judge verdicts, Claude Sonnet on both
  sides.
- One rubric clause was narrowed after a failure. The run 2 coding verdict is FAIL under the
  original wording and PASS under the narrower wording; both are reported above.
- Security hardening landed after these tests and was not re-tested in the simulated runtime:
  bots that read outside content must refuse instructions inside it (lint check 4), the
  designer asks before turning a mentioned chore into a bot, published templates are redacted,
  and report and routine-reply text is treated as data. The skill-text dry-run in DRY_RUN.md
  re-walks check 4 and the hold-until-verify path; it is not a runtime re-test.
- Not installed in Cursor for this run. The README install path matches
  `.cursor-plugin/plugin.json` and Cursor's local-plugin docs. No screenshot of the skills in
  Customize is part of this record.
