# Lab 03 · Spec error or execution error?

**Time:** 60 min · **Track:** paper or terminal · **Trains:** principle 1

> When the code is wrong, retrying the code cannot help. When the spec is
> wrong, retrying the code is the only thing that makes it worse.

---

## The situation

`SPEC.md` asks for loan renewals:

> Members should be able to renew a loan so they can keep a book for longer.
> Add a `renew(loan, today)` function to the library package. It should extend
> the loan and handle overdue fees sensibly.

An agent will implement this. The tests will pass. The code will look
reasonable. It will also be wrong, in the sense that it will not do what you
meant — and you will not be able to point to the line where it went wrong,
because no line is wrong. The request was.

This is the most expensive failure mode in agentic coding, because it produces
no error. The only detector is a written expectation.

---

## What you will produce

- An inventory of at least five decisions the request left open.
- A rewritten spec that pins them.
- Two implementations to compare, from two fresh sessions.
- A one-line diagnostic you can use on the next ambiguous task.

---

## Steps

### 1. Answer the request yourself, on paper

Before prompting, write down what *you* would build. At minimum:

1. How many renewals are allowed?
2. How many days does a renewal add?
3. Does it extend from the due date or from today?
4. Can an overdue loan be renewed?
5. Can a suspended member renew?
6. Can a returned loan be renewed?
7. What happens at the limit — error or silent no-op?
8. Does the renewal counter live on the loan?
9. Does renewing reset the grace period or waive fees?
10. What is the function signature?

If you cannot answer all ten, you have found the problem. Most people can
answer four.

### 2. Let the agent implement the ambiguous spec

Fresh session. Prompt:

```text
Implement the feature in SPEC.md. Add tests. Run make test.
```

Do not add detail. Do not answer questions it did not ask. If it asks you
something, that is data: note the question, answer it, and remember that the
spec did not contain the answer.

### 3. Inventory the decisions

Open the diff. For every choice the implementation had to make, write:

| Decision | What the code does | Was it specified? |
|---|---|---|

You are not looking for bugs. You are looking for **silent choices**. A silent
choice is not a defect; it is a decision that was made by the model instead of
by you.

Pay particular attention to the signature. The request says
`renew(loan, today)`. Suspension is a property of `Member`. With that
signature, the suspension rule **cannot be implemented**, because the function
never sees the member. That is not an execution error — no amount of retrying
will fix it. The interface is the spec, and the spec is impossible.

### 4. Check whether the tests encode the decisions

Read `tests/test_renewals.py` (or whatever it created).

- Do the tests assert the renewal limit, or only the happy path?
- Is there a test for the overdue case at all?
- If a test exists for suspension, how did it get the member into `renew`?

If the tests only cover the happy path, they are not encoding the spec — they
are encoding the implementation. That is the second failure: tests that would
pass for any of the ten possible answers.

### 5. Diagnose the error type

Use this test:

> Can you write a failing test that the current code violates, **and** justify
> that test from the request as written?

- **Yes** → execution error. The spec was sufficient; the code diverged. Retry
  with the failing test as the target.
- **No** → specification error. The code is consistent with an underspecified
  request. Retrying produces a different arbitrary answer, not a better one.

Write down which one this is, and the evidence.

### 6. Rewrite the spec

Write your own version first. Then compare with
[`answer-key/renewals-spec.md`](../answer-key/renewals-spec.md). It is one valid
answer, not the only one — what matters is that every decision is **binding**
and **testable**.

A spec is not done when it describes the feature. It is done when two
implementers would produce the same observable behaviour.

### 7. Run it again, fresh

New session, new copy of the sandbox, new spec. No reference to the first run.

```text
Implement the feature in SPEC.md exactly. Where the spec is silent, stop and
ask rather than choosing. Add tests for every acceptance criterion.
```

Compare the two implementations on the ten decisions. At least one should
differ. That difference is the cost of the ambiguity, made visible.

If the agent still asks a question, the spec still has a hole. That is a
useful result, not a failure: you found it in five minutes instead of in
review.

### 8. Commit the spec, not just the code

The durable artefact from this lab is the spec. Keep it next to the code. The
next feature starts from it, and the next agent reads it instead of guessing.

---

## Paper variant

Do steps 1, 3 and 6 without running anything. For step 3, read the reference
implementation in
[`answer-key/renewals-reference.patch`](../answer-key/renewals-reference.patch)
and list its choices as if a teammate had written it. Then write the spec that
would have forced those choices.

The exercise is the inventory, not the code.

---

## Acceptance criteria

- [ ] At least five open decisions listed, with what the implementation chose.
- [ ] The signature problem identified: `renew(loan, today)` cannot express
      suspension.
- [ ] A rewritten spec with binding, testable answers.
- [ ] A second, fresh run that follows the spec without questions.
- [ ] A written diagnosis: spec error or execution error, with evidence.

---

## Debrief

1. How many of the ten decisions did the original request answer? How many did
   the implementation answer silently?
2. The first implementation passed its own tests. What did those tests actually
   verify?
3. Why does re-running the same prompt tend to produce a *different* wrong
   answer rather than a correction?

---

<details>
<summary><strong>Solution, model answer, and grading</strong></summary>

### The decisions the request left open

The reference spec pins all ten. A typical first implementation chooses
something like: unlimited renewals, extend from today, allow overdue, no
suspension check (it cannot see the member), no counter, silent no-op at the
limit. Every one of those is defensible. None of them is what the spec says,
because the spec says nothing.

The decisive one is the signature:

```python
renew(loan, today)              # cannot implement the suspension rule
renew(loan, member, today)      # can
```

An interface that cannot express the policy is a specification defect. The
agent cannot fix it by trying harder; it can only invent an answer or ask.

### The diagnosis

| Symptom | Execution error | Specification error |
|---|---|---|
| Tests | Fail | Pass |
| Diff | Contradicts a written expectation | Consistent with an unwritten one |
| Error message | Exists | Does not exist |
| Retry | Can converge | Produces a different arbitrary answer |
| Detector | The test | Review against intent |

The heuristic:

> If you cannot write a failing test that is justified by the request itself,
> the request is the defect.

This is why "the tests pass" is not evidence of correctness. The tests were
written against the same underspecified request, usually by the same agent, in
the same session. They inherit the ambiguity.

### The tell

The most reliable signal of a spec error is **fluency**. The agent asks nothing,
produces a complete implementation, writes tests that pass, and summarises
confidently. That is not evidence that the task was clear. It is evidence that
the model filled the gaps silently — which it is designed to do.

The absence of questions is not clarity. It is unmeasured ambiguity.

### A good spec

The reference is
[`answer-key/renewals-spec.md`](../answer-key/renewals-spec.md). What makes it
work:

- A table of binding decisions, each with a value.
- An explicit note that the original signature was wrong, and why.
- Acceptance tests written as observable behaviour.
- An out-of-scope section, so the agent does not add reservations.
- A verification section with exact commands.

Two implementers reading it would produce the same observable behaviour. That
is the bar.

### Grading

| Score | Submission |
|---|---|
| **3** | ≥5 decisions inventoried with evidence; signature defect found; spec is binding and testable; second run follows it without questions; diagnosis is correct and justified. |
| **2** | Inventory and spec are good, but the signature problem or the second run is missing. |
| **1** | A spec was written but still contains adjectives ("sensible", "reasonable") instead of values; or the first implementation was treated as the reference. |
| **0** | "It works" accepted because the tests passed; no inventory. |

### Common failures

- **Treating the first implementation as the answer.** It is one sample from a
  distribution of guesses. The second run is how you see the distribution.
- **Writing a longer spec instead of a more specific one.** Length is not
  precision. "Renewals should be user-friendly" is longer and worth less than
  "maximum 2".
- **Asking the agent to "make it robust".** That delegates the decisions back
  to the model, which is where they came from.
- **Forgetting the interface.** Most spec defects are signature defects. If the
  function cannot see the data the rule needs, no implementation can be
  correct.

</details>
