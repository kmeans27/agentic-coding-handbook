# Project rules

## Style and conventions

- Write clean, readable, maintainable code.
- Use meaningful variable names.
- Be thorough and consider edge cases.
- Follow best practices at all times.
- Add comments where the code is not self-explanatory.
- Keep functions small and focused on a single responsibility.
- Prefer clarity over cleverness.
- Write clean, readable, maintainable code. (Yes, this is repeated. It is still true.)
- Always write tests for new behaviour.
- Never break the build.
- Think before you act.

## Testing

- Use pytest: `pytest -q`.
- Run the full test suite before every commit.
- Always ask the user before running tests, in case they are already running.
- If a test fails, fix the code, not the test.
- Do not add tests for things that are obviously correct.

## Build and environment

- Python 3.10+.
- No third-party dependencies. Standard library only.
- Money is stored as integer cents. Never use floats for money.
- Dates are represented as integer day numbers relative to an arbitrary epoch, not as `datetime` objects.

## File map

- `library/models.py` — dataclasses: `Member`, `Book`, `Loan`.
- `library/policy.py` — borrowing limits and the `can_borrow` check.
- `library/loans.py` — loan lifecycle, overdue fees, pagination.
- `tests/test_loans.py` — unit tests for fees, borrowing and pagination.
- `tests/test_policy.py` — unit tests for limits and suspension.
- `tests/test_integration.py` — slower lifecycle tests.
- `Makefile` — `test`, `test-fast`, `test-slow`, `lint`, `verify`.
- `SPEC.md` — the current feature request.
- `docs/` — architecture documentation. (This directory does not exist yet.)
- `scripts/` — maintenance scripts. (This directory does not exist yet.)

## Domain notes

The library lends books to members. Members have a tier: basic or plus.
Basic members can hold three loans, plus members ten. A suspended member
cannot borrow. Loans are due after fourteen days. There is a three-day grace
period before overdue fees start. Fees are twenty-five cents per day late.

This is a small domain and you should be able to hold it in your head.

## Architecture

The code is organised into a policy layer and a lifecycle layer. The policy
layer owns the rules; the lifecycle layer owns the transitions. Do not mix
them. If you find yourself adding policy logic to `loans.py`, stop and put it
in `policy.py` instead. This separation is important for maintainability and
was chosen after a long discussion. It keeps the code testable and makes the
rules discoverable.

## Workflow

- Run `make verify` before committing.
- Commit messages should be descriptive.
- Do not commit `__pycache__`.
- If you are unsure about a requirement, ask.
- Reference the issue number in the commit message.

## Things to avoid

- Do not rewrite the whole file when a small edit will do.
- Do not introduce new patterns when an existing one will work.
- Do not add dependencies.
- Do not use floats for money.
- Do not use `datetime` for day numbers.
- Do not modify `tests/` unless the task requires it.
  (Exception: you may add tests freely. But do not modify existing tests.)
- Do not delete tests.
- Do not skip tests.
- Do not silence errors with bare `except`.
- Do not use global mutable state.
- Do not optimise prematurely.
- Do not over-engineer.

## When in doubt

Ask the user. It is better to ask than to guess. But also try to be
autonomous and not interrupt unnecessarily. Use your judgement.

## Final reminder

Write clean, readable, maintainable code. Be thorough. Consider edge cases.
Follow best practices. Keep functions small. Prefer clarity over cleverness.
Always write tests. Never break the build. Think before you act.
