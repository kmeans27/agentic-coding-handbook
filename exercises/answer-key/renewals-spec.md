# Feature: loan renewals

A member may extend an open loan without returning the book. This document is
the specification. Where it disagrees with the current code, this document
wins.

## Interface

```python
renew(loan: Loan, member: Member, today: int) -> Loan
```

The request originally proposed `renew(loan, today)`. That signature cannot
express the suspension rule, because suspension lives on `Member`. The
signature above is the corrected one.

## Decisions

These are the questions the original request left open. Each answer is binding.

| # | Decision | Value |
|---|---|---|
| 1 | Maximum renewals per loan | 2 |
| 2 | Extension length | 14 days (`DEFAULT_LOAN_DAYS`) |
| 3 | Extend from | The loan's current `due_day`, not from `today` |
| 4 | Overdue loans | Cannot be renewed |
| 5 | Suspended members | Cannot renew |
| 6 | Returned loans | Cannot be renewed |
| 7 | Renewal counter | `Loan.renewals`, starts at 0, increments by 1 |
| 8 | Failure mode | Raise `RenewalError` (subclass of `ValueError`) |
| 9 | On failure | No mutation: `due_day` and `renewals` are unchanged |
| 10 | On success | Mutate the loan in place and return it |

A renewal is not a return. It does not touch `returned_day`, does not create a
second loan, and does not waive fees. Because overdue loans cannot be renewed,
there is no fee conflict to resolve.

## Acceptance tests

1. `renew(loan due 14, member, today=10)` → `due_day == 28`, `renewals == 1`.
2. A second renewal → `due_day == 42`, `renewals == 2`.
3. A third renewal raises `RenewalError` and leaves `due_day == 42`.
4. `renew(..., today=15)` on a loan due 14 raises `RenewalError` and leaves the
   due day unchanged.
5. A suspended member raises `RenewalError`.
6. A returned loan raises `RenewalError`.

## Out of scope

Reservations, holds, and notifications. Do not add them.

## Verification

```bash
make test      # full suite, all pre-existing tests still green
make verify    # lint and fast tests
```

The diff must not modify existing tests. Add a new `tests/test_renewals.py`.
