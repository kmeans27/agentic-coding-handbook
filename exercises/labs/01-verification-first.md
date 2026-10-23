# Lab 01 · Verification before code

**Time:** 60–90 min · **Track:** terminal · **Trains:** principle 3, principle 1

> A green suite is a claim about your tests, not about your code.

---

## The situation

Members are being charged the wrong overdue fee. Support has a screenshot and
a complaint, not a reproduction.

You run the suite:

```bash
make test
# Ran 10 tests in 4.5s
# OK (skipped=1)
```

Everything passes. The bug is real and completely invisible to the tests. This
is the normal condition of a codebase, not an unusual one.

Your job is not to fix the fee. It is to make the bug **visible first**, then
fix it — and to notice that one of the existing tests is itself wrong.

---

## What you will produce

- A failing boundary test that encodes the written policy.
- A minimal implementation fix.
- A decision, with evidence, about which side of a docstring-vs-test conflict
  is authoritative.
- A one-paragraph note on why the existing assertions could not catch this.

---

## Steps

### 1. Read the contract, not the code

Open `library/loans.py`. The module docstring is the policy:

> The first three days *after* the due day are a grace period and cost nothing.
> From the fourth day late, the fee is 25 cents per day late.

Do not read the function yet. Write the truth table by hand for a loan due on
day 10:

| `today` | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|
| days late | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| expected cents | ? | ? | ? | ? | ? | ? | ? |

Fill it in before continuing. This table is the specification. If you skip
this step you will later accept whatever the agent produces, because you will
have nothing to compare it to.

### 2. Write the test, run it, watch it fail

Create `tests/test_fee_boundaries.py`. Assert the **whole table**, not one
example:

```python
import unittest

from library.loans import overdue_fee
from library.models import Loan


class FeeBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.loan = Loan(member_id="m1", book_id="b1", due_day=10)

    def test_whole_table(self):
        expected = {10: 0, 11: 0, 12: 0, 13: 0, 14: 25, 15: 50, 16: 75}
        actual = {today: overdue_fee(self.loan, today) for today in expected}
        self.assertEqual(actual, expected)
```

```bash
python3 -m unittest tests.test_fee_boundaries -v
```

It must fail. Record the actual values. If it passes, your table is wrong, not
the code.

### 3. Direct the agent — with the test as the target

Paste something close to this. Notice what it does and does not say:

```text
tests/test_fee_boundaries.py pins the fee policy from the module docstring
in library/loans.py. It currently fails.

Fix the implementation so that test passes. Do not modify the test.
Do not modify the docstring.

When done, run:
  python3 -m unittest tests.test_fee_boundaries -v
  make test-fast

Paste both outputs. If you believe the test is wrong, stop and say why
instead of changing it.
```

The prompt names the file, the symbol, the constraint, and the exit criterion.
It also gives the agent a legal way to disagree. That last clause is what
prevents silent test editing.

### 4. Verify the claim

Do not accept "fixed". Run the two commands yourself. Then read the diff:

```bash
git diff
```

You are looking for one changed arithmetic expression. If the diff touches the
test, the docstring, or anything unrelated, stop and ask why. A correct fix
here is small; a large diff means the agent rewrote something it did not
understand.

### 5. Resolve the second bug: when the test is wrong

The docstring says pages are **1-based**. The existing test paginates with
`page=0`.

```bash
grep -rn "paginate(" . --include=*.py
```

You will find exactly one caller: the test itself. Now decide, in writing:

- Is the docstring the contract, or is the test?
- Are there external callers who depend on 0-based pages?
- What is the smallest change that makes code and contract agree?

In this repository the docstring is the contract, there are no external
callers, and the test encoded an assumption rather than a requirement. Fix
both the function and the test, and add a second-page test so the boundary is
pinned from both sides.

### 6. Full suite

```bash
make test
```

All green, including the test you added. Commit.

---

## Acceptance criteria

- [ ] A boundary test existed and **failed** before the implementation changed.
- [ ] `make test` is green.
- [ ] The implementation diff is one line for the fee bug.
- [ ] The pagination decision is justified by the docstring and a call-site
      search, not by "the test was failing".
- [ ] You can state why `assertGreater(fee, 0)` cannot catch this class of bug.

---

## Debrief

Write the answers down.

1. The suite was green while the fee was wrong. What exactly did the green
   suite prove?
2. You changed a test in step 5. Lab 04 is about *not* changing tests. What is
   the difference between the two situations?
3. If you had let the agent "make the failing tests pass" without the
   no-edit clause, what are the three most likely things it would have done?
   Which of them would still have looked like success?

---

<details>
<summary><strong>Solution, model answer, and grading</strong></summary>

### The table

| `today` | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|
| days late | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| expected cents | 0 | 0 | 0 | 0 | 25 | 50 | 75 |

The implementation returns `0, 0, 0, 25, 50, 75, 100`. It starts charging one
day early and charges one day too much from then on. Two errors in one
expression:

```python
return max(0, days - GRACE_DAYS + 1) * DAILY_FEE_CENTS   # wrong
return max(0, days - GRACE_DAYS) * DAILY_FEE_CENTS       # right
```

The reference patch is [`answer-key/fix-fee.patch`](../answer-key/fix-fee.patch),
and the full boundary test is
[`answer-key/test_fee_boundaries.py`](../answer-key/test_fee_boundaries.py).

### Why a table test

A single example would have to land on day 13 or 14 to catch this. The existing
test checks day 10 (not late) and day 20 (very late) — both outside the broken
boundary. A table checks the transition, which is where the bug lives.

This is the general rule: **bugs cluster at boundaries, so tests should too.**
Off-by-one errors are invisible in the middle of a range.

`assertGreater(fee, 0)` is nearly worthless because it asserts a direction, not
a value. It passes for 1 cent, 25 cents, or 10,000 cents. It cannot distinguish
"correct" from "wrong by a factor of ten".

### The pagination conflict

The correct resolution is:

1. The docstring is the stated contract.
2. `grep` shows one caller, and it is a test.
3. Therefore the test is wrong, and both the function and the test change.

```diff
-    start = page * size
+    start = (page - 1) * size
```

```diff
-        self.assertEqual(paginate(items, page=0, size=10), list(range(1, 11)))
+        self.assertEqual(paginate(items, page=1, size=10), list(range(1, 11)))
+        self.assertEqual(paginate(items, page=2, size=10), list(range(11, 21)))
```

This is **not** test tampering. The distinction is not "did you edit a test".
It is:

- Tampering: you weaken a test so a wrong implementation passes.
- Correction: you change a test because the test contradicts an authoritative,
  externally checkable contract.

Tampering has no evidence. Correction has a docstring, a call-site search, and
a replacement assertion that is at least as strong as the original.

The worst outcome is the one that looks tidiest: changing the docstring to say
pages are 0-based. That is rewriting the specification to match the bug. It
makes the suite green and the product wrong. If you did this, score 1.

### Grading

| Score | Submission |
|---|---|
| **3** | Boundary test failed first; one-line fix; pagination justified by contract + call sites; a second-page test added; debrief explains that green means "tests pass", not "behaviour is correct". |
| **2** | Test and fix correct, but pagination resolved by whichever was easier, or no second-page test. |
| **1** | Test written after the fix (no failure recorded), or docstring changed to match the bug, or only one of the two boundaries asserted. |
| **0** | Fixed by hand without a test, or accepted the agent's "done" without running anything. |

### Common failures

- **Writing the test with the buggy values.** If the test passes immediately,
  you copied the implementation instead of the policy. The table is derived
  from prose, not from running the code.
- **Asking for "the fix" and the test in one prompt.** The agent writes a test
  that asserts whatever it implemented. Split the steps: test first, failure
  observed, then fix.
- **Weak replacement.** `assertEqual(fee, 25)` at day 14 alone misses the
  grace boundary. Keep the table.
- **Ignoring the skipped test.** You will meet it properly in Lab 04.

</details>
