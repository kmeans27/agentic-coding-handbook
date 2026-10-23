# Lab 08 · Adversarial review

**Time:** 45 min · **Track:** paper or terminal · **Trains:** principle 10 · **Assumes:** Lab 01

> A reviewer that reports everything is as useless as one that reports nothing.

---

## The situation

A teammate — or an agent — has submitted a branch that adds reservations. The
diff also reorganises a module, reorders imports, and adds a helper.

There are two real defects. There are also four changes that look like defects
if you are pattern-matching: a rename-shaped import block, a new docstring
paragraph, an unused function, and a data structure choice you might not make.

Your job is to find the two, and to leave the four alone.

The branch is built on top of your Lab 01 fixes, so the baseline is green. That
matters: a red baseline lets you find bugs by running tests. A green one makes
you read.

---

## What you will produce

- A review report with severity, location, and a concrete trigger per finding.
- A false-positive count.
- A test that proves the defect the existing suite does not catch.
- A one-sentence review instruction you will reuse.

---

## Steps

### 1. Build the branch

From a clean sandbox copy:

```bash
git apply "$HANDBOOK/exercises/answer-key/fix-fee.patch"
git apply "$HANDBOOK/exercises/answer-key/fix-pagination.patch"
git apply "$HANDBOOK/exercises/answer-key/prepare-suspension-test.patch"
git apply "$HANDBOOK/exercises/answer-key/fix-suspension.patch"
cp "$HANDBOOK/exercises/answer-key/test_fee_boundaries.py" tests/

git add -A && git commit -qm "baseline: lab 01 fixes"
make test     # must be green, including the boundary tests

git checkout -b feature/reservations
git apply "$HANDBOOK/exercises/answer-key/review-diff.patch"
git diff
```

Read the diff on its own before you run anything.

### 2. Review without executing

Fresh agent session. Do not tell it what the bugs are. Prompt:

```text
Review the current git diff for correctness.

For each finding, give:
- file:line
- the input or state that triggers it
- the observable wrong output
- severity (blocker / major / minor)

Report only defects that change behaviour. Do not report style, naming,
import order, dead code, or missing tests unless the missing test hides a
concrete defect you can describe.

If you are unsure whether something is a defect, put it in a separate
"questions" list rather than mixing it with findings.
```

The last instruction is the important one. It gives the reviewer a place to put
uncertainty without polluting the findings.

### 3. Write your own report first

Before reading the agent's output, write your own. For each finding:

```text
Finding: <one sentence>
Where: library/loans.py:NN
Trigger: <input or state>
Expected: <observable behaviour>
Actual: <observable behaviour>
Severity: <blocker|major|minor>
```

If you cannot fill in Trigger, Expected, and Actual, you have a suspicion, not a
finding. Put it in your own questions list.

### 4. Compare and score

| | You | Agent | Reference |
|---|---|---|---|
| Missing eligibility check | | | ✓ |
| Off-by-one in `overdue_days` | | | ✓ |
| Import order | | | noise |
| Docstring paragraph | | | noise |
| Unused `format_fee` | | | noise |
| Reservation as `dict` | | | noise |

Score:

- +2 for each real bug found with a trigger.
- +1 if severity is proportionate.
- −1 per invented finding.
- −2 if style noise is reported as a defect.

### 5. Run the tests — now

```bash
make test
```

You will see failures in `test_fee_boundaries.py`. That confirms the
off-by-one. It tells you nothing about the reservation bug, because no test
covers reservations.

This asymmetry is the lesson:

- Tests are good at **regressions in tested behaviour**.
- Review is good at **uncovered preconditions and new surface area**.
- Neither replaces the other.

### 6. Prove the uncovered bug

Write a test that fails on the branch:

```python
def test_suspended_member_cannot_reserve(self):
    member = Member(id="m1", name="S", tier="basic", suspended=True)
    with self.assertRaises(ValueError):
        reserve_book(member, Book(id="b1", title="Dune"), [])
```

Run it. It fails. Now fix `reserve_book` to check `can_borrow` — and notice
that you have just converted a review finding into a regression test. That is
the correct lifecycle for a finding: review finds it once, a test keeps it
found.

### 7. Write the reusable instruction

One or two sentences you can paste into any review prompt. It should encode the
two failure modes you just saw: accepting a plausible line, and reporting
noise.

Example shape:

> Report only behaviour-changing defects, each with a concrete trigger and the
> wrong output. Put uncertainty in a separate questions list. Do not report
> style, naming, or dead code.

---

## Paper variant

Do steps 1–3, then read
[`answer-key/review-findings.md`](../answer-key/review-findings.md) and score
yourself. You do not need to run the tests to find the off-by-one; the module
docstring is in the diff context. You do need it to confirm.

---

## Acceptance criteria

- [ ] Both real defects found with a trigger and an expected/actual pair.
- [ ] No style noise reported as a defect.
- [ ] A false-positive count, stated honestly.
- [ ] A test that proves the uncovered defect.
- [ ] A reusable review instruction.

---

## Debrief

1. Which defect was easier to find, and why?
2. The diff says "public behaviour is intended to be unchanged". Why is that
   sentence not evidence?
3. What does a review catch that a test cannot, and vice versa?

---

<details>
<summary><strong>Solution, model answer, and grading</strong></summary>

### The two findings

**1 — Blocker: `reserve_book` bypasses eligibility.**

```python
def reserve_book(member, book, reservations):
    reservation = {"member_id": member.id, "book_id": book.id}
    reservations.append(reservation)
    return reservation
```

Trigger: `Member(suspended=True)`. Expected: `ValueError`, like `borrow`.
Actual: reservation created. The function also promises "next available copy"
without checking availability, but availability is not modelled in this
codebase; treat that as an overpromising docstring, not a separate defect.

Why tests miss it: there is no reservation test. A green suite is silent about
code it never executes.

**2 — Major: `overdue_days` subtracts a day.**

```diff
-    return max(0, today - loan.due_day)
+    return max(0, today - loan.due_day - 1)
```

Trigger: due 10, today 14. Expected 25c. Actual 0c. The docstring defines the
due day as inclusive, so day 11 is one day late; subtracting one makes it zero.

Why tests miss it *in the original repo*: the only fee assertion is
`assertGreater(fee, 0)` at day 20. Why they catch it here: Lab 01 added the
boundary table.

### The noise

| Change | Why it is not a finding |
|---|---|
| Imports reordered | No behaviour. |
| Docstring paragraph | Accurate, if unverifiable. |
| `format_fee` unused | Dead code; a cleanup note at most. It uses integer arithmetic. |
| `dict` reservation | Consistent with the codebase; not a correctness issue. |

A review that lists these has a recall of 2/2 and a precision of 2/6. It reads
as thorough and is nearly useless, because the author now has to triage four
non-issues.

### The asymmetry

| Detector | Strength | Blind spot |
|---|---|---|
| Tests | Deterministic, repeatable, cheap to rerun | Only what someone thought to test |
| Review | Finds uncovered preconditions, design errors, missing cases | Inconsistent, attention-limited, no regression protection |

The correct loop is: review finds it, a test keeps it found. A finding without
a test is a conversation; a test without a review is a coverage bet.

### The "behaviour unchanged" claim

The docstring says the reorganisation intends no behaviour change. That is a
statement of intent by the author. It is not a proof, and it is exactly the
kind of claim that should make you check the arithmetic. The phrase is useful
only as a hint about where to look: "nothing changed" plus a changed line means
the author either believes the line is equivalent or did not notice it.

### Grading

| Score | Submission |
|---|---|
| **3** | Both findings with triggers and severities; zero noise reported; test added for the uncovered defect; reusable instruction is specific. |
| **2** | Both findings, but one lacks a trigger, or one noise item reported as minor. |
| **1** | Only the test-caught bug found, or the report is a list of "consider…" suggestions. |
| **0** | Reported the import order and missed the arithmetic. |

### Common failures

- **Finding the test failure and stopping.** Running `make test` gives you one
  bug for free and hides the other. Review before executing, or you will
  confuse the two skills.
- **Reporting dead code as a blocker.** `format_fee` is unused. That is a
  cleanup, not a defect. Severity inflation destroys trust in the report.
- **"Consider adding tests."** That is not a finding; it is a wish. Name the
  behaviour that is untested and the input that would break it.
- **Reviewing the summary instead of the diff.** The summary says reservations
  are checked. The diff says they are not. Only one of them is evidence.

</details>
