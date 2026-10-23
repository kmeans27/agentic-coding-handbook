<div align="center">

# Exercises

**Nine labs. One deliberately broken repository. Real failure modes, not prompts about prompts.**

</div>

---

## What this is

The [handbook](../README.md) explains the mechanisms. This track makes you
operate them until they are habits.

Every lab is built on the same small Python codebase — [`sandbox/`](sandbox/) —
which contains real bugs the tests do not catch, a skipped test hiding a
suspension bug, an ambiguous feature request, a slow suite, and a rules file
that is 90% noise. None of that is decoration. Each lab asks you to fix one
specific failure that agents produce in real repositories, and each one has a
solution you can compare against.

There are no toy prompts and no trivia. If you finish a lab, you have an
artefact: a boundary test, a pruned rules file, a spec, a review report, a
faster loop.

---

## Two tracks

| Track | Needs | Labs |
|---|---|---|
| **Paper** | A text editor and the files in this repo. No execution. | 02, 03, 05, 08 |
| **Terminal** | Python 3.10+, `git`, and an agent you can run. | 01, 04, 06, 07, 09 |

The paper labs are deliberately usable during a break when you cannot code.
They train the parts that matter most anyway: specifying, pruning, and
reviewing. Do them in order; the terminal labs assume the artefacts they
produce.

---

## Setup (once)

```bash
# from the repository root
export HANDBOOK="$PWD"          # terminal labs use this for the answer key
cp -r exercises/sandbox /tmp/lab-sandbox
cd /tmp/lab-sandbox
git init -q
git config user.email "you@example.com"   # only if git has no identity
git config user.name "Your Name"
git add -A && git commit -qm "baseline"
make test                                  # 10 tests, ~4.5s, 1 skipped
```

Then, for each lab, start from a clean copy:

```bash
rm -rf /tmp/labNN && cp -r /tmp/lab-sandbox /tmp/labNN && cd /tmp/labNN
```

The terminal labs refer to `$HANDBOOK/exercises/answer-key/`. If you opened a
new shell, re-export `HANDBOOK` before starting.

Do not work inside the handbook repository. Do not carry fixes from one lab
into the next; several labs depend on the bug still being there.

---

## How a lab works

Every lab has the same shape:

1. **The situation** — what is broken, and why it is realistic.
2. **Guided steps** — numbered, with prompts you can paste. The prompts are
   examples of *direction*, not magic words.
3. **Acceptance criteria** — how you know you are done. These are checkable,
   not vibes.
4. **Debrief** — two or three questions. Write the answers down; the writing
   is the exercise.
5. **Solution** — inside a collapsed `<details>` block, with a grading rubric
   and the common ways people fail.

Attempt the lab before opening the solution. Not because spoilers are naughty,
but because the diagnostic value is in your first attempt. The solution is for
calibration, not for reading instead of doing.

---

## The labs

| # | Lab | Time | Track | Trains |
|---|---|---|---|---|
| 01 | [Verification before code](labs/01-verification-first.md) | 75 min | Terminal | Principle 3. Write the check before the change; decide when a test is wrong. |
| 02 | [Context budget](labs/02-context-budget.md) | 45 min | Both | Principle 2. Pointers beat payloads; measure instead of assuming. |
| 03 | [Spec error or execution error?](labs/03-spec-vs-execution.md) | 60 min | Both | Principle 1. Find the decisions a request left open. |
| 04 | [Test tampering](labs/04-test-tampering.md) | 45 min | Terminal | Principle 3. Notice when "make it green" buys green with coverage. |
| 05 | [Rules-file surgery](labs/05-rules-file.md) | 45 min | Both | Principle 6. Keep only rules that prevent a real mistake. |
| 06 | [Make the loop fast](labs/06-fast-loop.md) | 45 min | Terminal | Principle 7. Cut feedback time without cutting detection. |
| 07 | [Parallel isolation](labs/07-parallel-isolation.md) | 60 min | Terminal | Principle 9. Two agents, one checkout, one race condition. |
| 08 | [Adversarial review](labs/08-adversarial-review.md) | 45 min | Both | Principle 10. Find the real bugs; do not report the noise. |
| 09 | [Capstone](labs/09-capstone.md) | 150 min | Terminal | All of it, on one feature, end to end. |

**Total:** about 9–10 hours. Split across three sittings:
01–03, then 04–06, then 07–09. Do not do them all in one day; the debrief
questions need time to settle.

---

## Self-grading

Each lab is scored **0–3**:

| Score | Meaning |
|---|---|
| **0** | Did not attempt, or skipped the acceptance criteria. |
| **1** | Produced the artefact, but it would not survive review: assertions too weak, the bug is still reachable, the spec still has holes. |
| **2** | Artefact is correct and the stated checks pass. One debrief answer is thin. |
| **3** | Correct, checked, and you can explain *why* the failure happened and what would have prevented it. You would ship this. |

Out of 27:

- **22–27** — you can direct an agent without losing the plot.
- **15–21** — the mechanics are there; the gaps are in verification and review.
- **8–14** — you are still accepting claims as evidence. Re-read
  [Verification](../docs/04-verification.md), then redo 01 and 08.
- **0–7** — do the [14-day plan](../study/two-week-plan.md) first. The labs
  assume the vocabulary.

A score is diagnostic, not a grade. The useful output of a 1 is the sentence
"here is what I accepted without checking", not the number.

---

## The one rule that matters

**Run the agent, not just yourself.**

You can fix all three bugs by hand in twenty minutes. That teaches you Python,
which you already know. The skill under test is *directing*: writing the check
first, giving a pointer instead of a dump, noticing when the agent quietly
weakened a test, reviewing a diff you did not write.

If you solve a terminal lab by hand, you have practised the wrong thing. If
you must, do it twice: once by hand to learn the domain, then from a clean copy
with the agent, watching what it does.

---

## Answer key

Concrete artefacts live in [`answer-key/`](answer-key/):

| File | Used by |
|---|---|
| `fix-fee.patch`, `fix-suspension.patch`, `fix-pagination.patch` | 01, 04, 09 |
| `prepare-suspension-test.patch` | 04 |
| `test_fee_boundaries.py` | 01, 06, 08 |
| `AGENTS.pruned.md` | 05 |
| `renewals-spec.md` | 03, 09 |
| `renewals-reference.patch`, `test_renewals.py` | 09 |
| `review-diff.patch`, `review-findings.md` | 08 |

All patches are `git apply`-able from the sandbox root. The reference
implementation is one valid answer to the spec, not the only one.

---

## After the labs

You will have a boundary test, a spec template, a pruned rules file, a review
prompt, and three loop measurements. That is the kit described on
[day 14 of the plan](../study/two-week-plan.md). Keep it; use it on the next
real task rather than starting from a blank prompt.
