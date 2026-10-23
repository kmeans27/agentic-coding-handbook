# Project rules

Python 3.10+, standard library only.

## Invariants

- Money is integer cents. Never floats.
- Day numbers are integers relative to an arbitrary epoch. Never `datetime`.
- Pages are 1-based. Page 1 is the first page.
- The authoritative policy is the module docstring in `library/policy.py`
  and `library/loans.py`. Read it before changing behaviour.

## Layout

- `library/policy.py` — eligibility rules. Put policy here, not in `loans.py`.
- `library/loans.py` — loan lifecycle, fees, pagination.
- `tests/` — `unittest`, no third-party runner.

## Commands

- `make verify` — lint plus fast unit tests. Run before every commit.
- `make test` — full suite, including the slow integration tests. Run before push.
- There is no `pytest` in this project. Do not invoke it.

## Test integrity

- Never delete, skip, or weaken a test to make the suite pass.
- If a test looks wrong, stop and explain why. Do not edit it without agreement.
- New behaviour needs a test that fails before the change.
