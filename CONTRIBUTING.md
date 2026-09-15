# Contributing to Wainwright

The bar for a change: does it make a designed bot tighter, a memory write more correct, or a
persona more accurate? Longer is not better.

## Ways to contribute

- Report a misfire. A skill that triggered wrongly, or a designer that produced a sloppy
  bot, is the most useful signal. Open an issue with the prompt and the output.
- Sharpen a skill. Fix a rule that backfires, add a missing good-vs-bad example.
- Add a skill. Only for a recurring job the current skills do not cover.

## Rules for skill changes

1. **Description says when.** `description` starts with "Use when" and states whether the
   skill auto-applies from context.
2. **Body is a generic recipe.** No personal names, emails, repo names, or channel names.
   Use `<placeholders>`.
3. **Examples show both sides.** Every rule worth writing down gets a good and a bad example.
4. **No em dashes.** Use a period, comma, or colon.
5. **Candor personas stay grounded.** Persona changes follow the rules in the upstream
   [Candor](https://github.com/itsryanlenk/candor) project.

## Verify before you open a PR

Run this and paste the `RESULT` line into the PR description:

```
python scripts/validate.py
```

If you changed a Grok Bot skill, also paste one before/after example of a bot description or
memory write that the change affects.

## Pull request process

1. Branch from `main`; one skill or one concern per PR.
2. Re-read every changed file end to end.
3. Say what behavior changed and why.

## Code of conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
