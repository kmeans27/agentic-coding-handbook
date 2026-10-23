# Lab 09 · Capstone

**Time:** 2–3 hours · **Track:** terminal · **Trains:** all of it · **Assumes:** Labs 01, 03, 04, 06

> The method is not the prompt. It is the sequence: specify, check, build,
> verify, review, measure.

---

## The task

Ship loan renewals, end to end, on a clean copy of the sandbox.

No new instructions beyond the spec you write. No hints beyond the reference
artefacts. You have already met every failure mode this feature can produce:

- an ambiguous request (Lab 03),
- a signature that cannot express the policy (Lab 03),
- tests that encode the implementation (Lab 03),
- a temptation to edit tests (Lab 04),
- a slow loop (Lab 06),
- a review that must separate bugs from noise (Lab 08).

The capstone is whether you run the sequence without being told to.

---

## What you will produce

1. A committed spec.
2. A committed set of acceptance tests that failed before the implementation.
3. An implementation, in a worktree, that passes them.
4. A verification record with real command output.
5. A fresh-context review report.
6. A measurement table and a five-line decision log.

---

## Steps

### 1. Spec (20 min)

Start from [`answer-key/renewals-spec.md`](../answer-key/renewals-spec.md) —
but write your own version first, then compare. Yours must pin:

- the signature and why it takes a `Member`,
- the maximum number of renewals,
- what the extension is measured from,
- the overdue, suspended, and returned cases,
- the failure type and the no-mutation guarantee,
- what is out of scope.

Commit it as `SPEC-renewals.md` **before** writing code. A spec written after
the implementation is a description, not a specification.

### 2. Acceptance tests first (30 min)

Write `tests/test_renewals.py` from the spec. Cover, at minimum:

| Case | Expected |
|---|---|
| Renew before due | due day + 14, counter 1 |
| Second renewal | due day + 28, counter 2 |
| Third renewal | `RenewalError`, no mutation |
| Overdue loan | `RenewalError`, no mutation |
| Suspended member | `RenewalError` |
| Returned loan | `RenewalError` |

Run them. Every one must fail, and for the right reason — not `ImportError`
alone. If the module does not exist yet, that is fine; write the tests against
the intended interface and let the import failure be the first failure. Then
add a stub if you need to see the assertions fail individually.

Commit the failing tests. Yes, commit red. The history is evidence that the
tests came first.

### 3. Isolate and implement (45 min)

```bash
git worktree add ../wt-renewals -b feature/renewals
cd ../wt-renewals
```

Prompt:

```text
Implement SPEC-renewals.md. The acceptance tests are in tests/test_renewals.py
and currently fail.

Constraints:
- Do not modify tests or the spec.
- Do not add dependencies.
- Keep the diff under 60 lines.
- Run `make test-fast` after each change and paste the output.

If the spec is silent on a decision, stop and ask. Do not choose silently.
```

Watch for:

- silent decisions (Lab 03),
- test edits (Lab 04),
- unrelated refactors,
- a diff that grows past the constraint.

If it asks a question, answer it **in the spec**, not in chat. The next agent
will not see the chat.

### 4. Verify (20 min)

The ladder, in order:

```bash
make test-fast          # unit tests, including the new ones
make test               # full suite, slow tests included
```

Then a manual trace — do not skip this:

```bash
python3 - <<'PY'
from library.loans import renew
from library.models import Book, Loan, Member

m = Member("m1", "Ada", tier="plus")
l = Loan("m1", "b1", due_day=14)
print(renew(l, m, today=10).due_day)   # expect 28
print(l.renewals)                      # expect 1
PY
```

The tests and the trace answer different questions. Tests say "the cases I
thought of pass". The trace says "the thing runs". Both are cheap; do both.

Record the commands and their output in a file. "It passed" is a claim; the
output is evidence.

### 5. Fresh-context review (30 min)

New session. No memory of writing the code. Give it only the diff and the spec:

```text
Review this diff against SPEC-renewals.md.

For each finding: file:line, trigger, expected, actual, severity.
Report only behaviour-changing defects. Put uncertainty in a separate
questions list. Do not report style, naming, or dead code.
```

Then run the tests yourself and compare:

| Found by | Count | Which |
|---|---|---|
| Tests | | |
| Review | | |
| Both | | |
| Neither (found later) | | |

A healthy result is not "review found nothing". It is "review found the
uncovered case". If review found only style, your prompt or your reviewer is
not adversarial enough. If it found nothing at all, try a second reviewer with
the instruction to look specifically at preconditions and boundaries.

### 6. Fix, rerun, merge (20 min)

Fix the real findings, add a regression test for each, rerun both tiers, then:

```bash
cd ..
git merge --no-ff feature/renewals
make test
```

Merge only when the full suite is green and no test was modified to get there.

### 7. Measure (15 min)

| Metric | Value |
|---|---|
| Spec decisions pinned | |
| Acceptance tests written | |
| Tests that failed first | |
| Assistant turns | |
| Wall-clock time | |
| Rework (minutes spent undoing or redoing) | |
| Review findings (real / false) | |
| Diff size (lines) | |
| Loop time (`make test-fast`) | |

Then five lines:

```text
The decision I almost left implicit:
What I got wrong on the first attempt:
What review caught that tests did not:
What I would change about my loop:
One sentence I will reuse next time:
```

---

## Hard mode (optional)

Add one interaction the spec does not cover: a member with an overdue loan
cannot reserve a new book. Write the spec amendment first, then the test, then
the code. This is the same loop with a smaller feature; if the first pass took
you under two hours, do this one.

---

## Grading — 10 points

| Area | Points | Criteria |
|---|---|---|
| **Spec** | 2 | Every decision binding; signature justified; out-of-scope stated; committed before code. |
| **Tests** | 2 | Written first and observed failing; boundaries covered (limit, grace, no-mutation); no weak assertions. |
| **Implementation** | 2 | Matches the spec; small diff; no test or spec edits; no dependencies. |
| **Verification** | 1 | Both tiers run; manual trace recorded; output pasted, not summarised. |
| **Review** | 2 | Fresh context; real findings with triggers; zero noise; regression test per finding. |
| **Measurement** | 1 | Numbers recorded; decision log names one concrete change. |

**9–10:** you can run this loop on a real repository.
**7–8:** the loop is there; one of spec, tests, or review is still decorative.
**5–6:** you can build, but you cannot yet prove.
**0–4:** the agent drove.

---

## Debrief

1. Which step cost the most, and was it the step you expected?
2. If the review had found nothing, would you have shipped? What would that
   have meant?
3. What would you cut if the task had to be done in 30 minutes? What would you
   never cut?

---

<details>
<summary><strong>Reference solution and what a strong run looks like</strong></summary>

### Reference artefacts

- Spec: [`answer-key/renewals-spec.md`](../answer-key/renewals-spec.md)
- Tests: [`answer-key/test_renewals.py`](../answer-key/test_renewals.py)
- Implementation: [`answer-key/renewals-reference.patch`](../answer-key/renewals-reference.patch)

The reference is one valid implementation. It adds `renewals: int = 0` to
`Loan`, `MAX_RENEWALS = 2`, `RenewalError`, and `renew()`, and it passes the six
acceptance tests plus the existing suite.

To see it:

```bash
rm -rf /tmp/reference && cp -r exercises/sandbox /tmp/reference
cd /tmp/reference
git init -q && git add -A && git commit -qm baseline
git apply "$HANDBOOK/exercises/answer-key/renewals-reference.patch"
cp "$HANDBOOK/exercises/answer-key/test_renewals.py" tests/
make test
```

### What a strong submission contains

- A spec where the signature is justified, not just stated. The sentence
  "`renew(loan, today)` cannot express suspension" is the intellectual core of
  the feature.
- Acceptance tests that a second implementer could satisfy without reading the
  first implementation.
- A no-mutation assertion on every failure case. This is the case most people
  forget: raising an error after half-mutating the loan.
- A diff in the 30–60 line range. The feature is small; a 200-line diff means
  refactoring that the spec did not ask for.
- A review finding that the tests missed, or an explicit, evidenced statement
  that review found nothing because the tests covered every branch. The second
  is rare and should be argued, not assumed.
- Numbers. Not "it felt fast".

### What a weak submission looks like

| Symptom | Underlying failure | Score impact |
|---|---|---|
| Spec written after the code | Description, not specification | Spec 1/2 |
| Tests written against the implementation | Tests encode bugs | Tests 1/2 |
| Tests pass but no failure was ever observed | No evidence they test anything | Tests 1/2 |
| Signature still `renew(loan, today)` | Suspension silently unimplemented | Spec 0–1 |
| Test file edited during implementation | The objective was green, not correct | Impl 1/2 |
| Review report lists import order | Precision collapse | Review 1/2 |
| No timing, no rework count | Measurement absent | Measurement 0/1 |

### Calibration

A strong run on this capstone takes 2–2.5 hours, not 45 minutes. Most of the
time is in the spec and the review, not the code. That ratio is the lesson: the
implementation is the cheap part now.

If you finished in under an hour with a good score, you probably skipped the
failing-first step or the fresh-context review. Check the evidence before
believing the score.

### The one thing to keep

The sequence:

```text
spec (binding decisions)
  → acceptance tests (fail first)
    → implementation (small, constrained)
      → verification (tests + trace)
        → review (fresh context, behaviour only)
          → measure (numbers + one change)
```

Every lab in this track is one cell of that table. The capstone is the whole
table, run without a checklist in front of you. When you can do that on a real
repository, the exercises are finished.

</details>
