# 02 · The working loop

> **Principles 4 and 5** — Plan in proportion to risk. Small batches, reversible steps.

<img src="../assets/the-loop.svg" alt="Frame, explore, specify, execute, verify — with two feedback loops" width="100%">

---

## Six stages, each with an exit condition

The loop is only useful if each stage **produces something the next stage can check**. Otherwise it collapses into "chat until it looks right", which is the thing this handbook exists to replace.

| Stage | You are answering | Artefact | Exit condition |
|---|---|---|---|
| **Frame** | What problem, what constraints, what proves success? | Acceptance check | You can state how you will know it worked |
| **Explore** | What already exists? What pattern should this follow? | List of files + the pattern to copy | You could describe the change in a sentence |
| **Specify** | Exactly what changes, where, and what does not? | Written plan | The plan names files, interfaces, out-of-scope, and the test |
| **Execute** | Do the smallest next increment | A small diff | The local check passes |
| **Verify** | Is it actually correct? | Evidence | A fresh reader can see it pass |
| **Commit** | Is this one logical change? | Commit / PR | Revertible in one step |

The stage people skip is **Explore**, because reading feels like not working. It is the highest-return stage. An agent that has seen the existing pattern will copy it; an agent that has not will invent a second pattern, and now you have two.

---

## Two kinds of failure, two different fixes

This is the core insight of the loop, and the reason it is drawn as a loop with two returns.

**Execution error** — the plan was right, the code was wrong.
→ Fix: show the failure, retry, narrow the task.

**Specification error** — the plan was wrong.
→ Fix: **stop coding.** Rewrite the spec. Retrying the code cannot help.

The tell is repetition. If the agent fails twice in the same place, the defect is upstream. Humans do the same thing: when a task keeps failing, we usually try harder rather than asking whether we described it correctly.

> [!TIP]
> Before your third correction, ask: *"Am I fixing the code, or am I fixing the plan?"* If you cannot answer, you are fixing the plan.

---

## Plan in proportion to risk

Planning is not free — it costs time and tokens. The skill is calibration.

| Task | Plan? | Why |
|---|---|---|
| Typo, log line, rename | No | You could describe the diff in one sentence |
| Single-file, obvious pattern | No | Exploration is the plan |
| Multi-file change | Yes, brief | Interfaces and ordering matter |
| Unfamiliar code | Yes | You do not know what you do not know |
| Anything irreversible | Yes, and get it reviewed | Migration, schema, auth, payments |
| Requirements fuzzy | Yes — as an interview | You need to discover what you want |

Anthropic's own guidance is a good default: **if you could describe the diff in one sentence, skip the plan.**

For the fuzzy-requirements case, invert the direction: have the agent interview *you* until the decisions are resolved. Ask it to dig into edge cases, UI, failure modes and tradeoffs, then write the result to a spec file. A spec that survives being read by someone else is worth more than an hour of prompting.

---

## What a usable spec contains

A spec is not a wish. It is a contract with a verification clause.

```markdown
## Goal
One paragraph. What changes for the user.

## Files and interfaces
- `src/auth/session.ts` — add `refreshIfExpired()`
- `src/api/client.ts` — call it before each request
- Reuse the retry helper in `src/lib/retry.ts`

## Out of scope
- No changes to the login flow
- No new dependencies

## Verification
- New test: expired token triggers exactly one refresh
- Existing auth suite stays green
- Manual: log out, wait for expiry, confirm no redirect loop
```

The two sections people omit are the two that prevent the most damage: **Out of scope** and **Verification**. Without the first, the agent "helpfully" refactors adjacent code. Without the second, "done" is an opinion.

---

## Vague versus precise

The difference is rarely length. It is **specificity about the check**.

| Vague | Precise |
|---|---|
| "add tests for foo.py" | "write a test for `foo.py` covering the logged-out case. Avoid mocks — use the existing `make_test_user` fixture." |
| "make the dashboard look better" | "here is a screenshot of the target. Implement it, screenshot the result, list the differences, fix them." |
| "fix the login bug" | "users report login fails after session timeout. Check `src/auth/`, especially token refresh. Write a failing test first, then fix it." |
| "refactor this file" | "extract the validation logic into `validate.ts` without changing behaviour. Run the tests before and after; one commit, structural only." |

Note what the precise versions add: a **location**, a **constraint**, and a **check**. Not politeness, not role-play, not "think step by step".

---

## Small batches are not timidity

A long autonomous run compounds error. Each step is conditioned on all previous steps, so an early misunderstanding is not corrected — it is **built upon**, and every subsequent decision inherits it.

Small batches give you:

- **Cheap detection.** The diff is small enough that review is real.
- **Cheap reversion.** You lose minutes, not an afternoon.
- **Cheap context.** You can clear between batches without losing much.
- **Honest commits.** Each one is a single logical change.

Structural and behavioural changes should be **separate commits**. Mixing "rename the module" with "change the retry policy" produces a diff nobody can review, human or machine.

---

## Commit is a stage, not an afterthought

The loop ends with integration, and integration has its own discipline:

1. Tests pass — and you saw them pass.
2. The diff matches the plan. Anything extra is either justified or removed.
3. Structural and behavioural changes are not mixed.
4. The message explains *why*, not *what*.
5. You could revert this in one command.

Checkpoint and rewind features are convenience, **not** a substitute for version control. They only track edits made through the tool's own file operations — anything done via a shell command is invisible to them. Git is the source of truth.

---

## Practice

Take a task you completed recently and reconstruct it against the table above.

1. Which stages did you actually do? Which did you skip?
2. Where was the artefact missing — did you have a written acceptance check, or did you decide "done" by feel?
3. Rewrite the original request as a spec with the four sections. Notice which section is hardest to fill in. That is the part you did not understand.

---

**Next:** [03 · Context](03-context.md) — why the same prompt works at 9am and fails at 11am.
