# Review findings: the reservations diff

Two real defects, three pieces of noise. A good review names both defects,
assigns severity, and does **not** pad the report with the noise.

---

## Finding 1 — Blocker: reservations bypass eligibility

**Where:** `library/loans.py`, `reserve_book`

```python
def reserve_book(member, book, reservations):
    reservation = {"member_id": member.id, "book_id": book.id}
    reservations.append(reservation)
    return reservation
```

**Why it is wrong:** every other path that grants a member access to a book
goes through `policy.can_borrow`. This one does not. A suspended member can
reserve. So can a member who is already at their loan limit. The docstring
says "reserve the next available copy", which is a promise the function does
not keep — there is no availability check either.

**Trigger:**

```python
member = Member(id="m1", name="S", tier="basic", suspended=True)
reservations = []
reserve_book(member, Book(id="b1", title="Dune"), reservations)
# returns a reservation instead of raising
```

**Expected:** `ValueError`, consistent with `borrow`. **Actual:** reservation
created.

**Why the tests miss it:** there is no reservation test at all. This is the
class of bug that review exists for; a green suite says nothing about code
that no test exercises.

**Difficulty:** easy to see once you ask "what authorises this action?" Hard
to see if you read the diff as a list of additions rather than as a change to
the system's invariants.

---

## Finding 2 — Major: `overdue_days` is one day short

**Where:** `library/loans.py`, `overdue_days`

```python
-    return max(0, today - loan.due_day)
+    return max(0, today - loan.due_day - 1)
```

**Why it is wrong:** the module docstring defines the due day as inclusive:
being due *on* day N is not late, and day N+1 is one day late. Subtracting one
makes day N+1 return zero and every subsequent day short by one. The fee
function then undercharges by 25c per loan.

**Trigger:** loan due day 10, returned day 14. Expected 25c. Actual 0c.

**Why the tests miss it:** `test_overdue_costs_money` asserts only
`assertGreater(fee, 0)` at day 20. Day 20 still produces a positive number, so
the test passes. A boundary test (see Lab 01) catches it immediately.

**Difficulty:** medium. The line is buried among import and docstring changes,
and it looks like a deliberate adjustment. The only defence is to read changed
arithmetic against the written contract.

---

## Not findings

These are in the diff. Do not report them as defects.

| Change | Why it is not a finding |
|---|---|
| Import order swapped | No behavioural effect. Style. |
| Module docstring gained a paragraph | Accurate. "Public behaviour is intended to be unchanged" is a claim, not evidence — which is exactly why you check the code, but the sentence itself is not a bug. |
| `format_fee` added, unused | Dead code is a minor cleanup note, not a defect. It uses integer arithmetic correctly. Reporting it as a money bug is a false positive. |
| Reservation stored as a `dict` | Matches how the surrounding code passes records around. A dataclass would be nicer; not a correctness issue. |

---

## How to score yourself

| Points | Criterion |
|---|---|
| 2 | Found the missing eligibility check, with a concrete trigger |
| 2 | Found the off-by-one, with a concrete trigger |
| 1 | Severity is proportionate (blocker vs major, not both "critical") |
| 1 | Zero false positives from the noise table |
| −1 each | Invented issues, or "consider adding tests" as a finding |
| −2 | Reported the style changes as bugs |

**8–10:** you can review agent output. **5–7:** you find bugs but cannot
filter. **0–4:** you are pattern-matching on the diff, not reading the system.

The most common failure is not missing a bug. It is reporting the rename and
the docstring while missing the arithmetic, because style is easier to see
than semantics.
