# The sandbox

A small library-loans codebase. It is **deliberately imperfect**:

- three real bugs that the test suite does not catch,
- one skipped test hiding a bug,
- a test that encodes a bug,
- a slow integration suite,
- a 96-line rules file that mostly says nothing.

That is the point. Every lab in `../labs/` operates on this repository, and each one asks you to fix a specific kind of failure that agents produce in real codebases.

---

## Commands

```bash
cd exercises/sandbox

make test        # everything (~5s, includes the slow suite)
make test-fast   # unit tests only (fast)
make test-slow   # the deliberately slow integration tests
make lint
make verify      # what you should run before committing
```

No dependencies. Python 3.10+ standard library only.

---

## Ground rules for using the sandbox

1. **Work on a copy.** `cp -r sandbox /tmp/lab01` before each lab. Do not let one lab's fixes contaminate the next.
2. **Initialise git first.** The labs assume you can diff and revert:
   ```bash
   cd /tmp/lab01 && git init -q && git add -A && git commit -qm baseline
   ```
3. **Do not read `../answer-key/` until you have attempted the lab.** The value is in the attempt, not the answer.
4. **Run the agent, not just yourself.** These labs are about *directing* an agent. If you solve it by hand, you have practised the wrong skill.

---

## What is wrong with it

Do not read this list before Lab 01. It is here so that you can check your own diagnosis afterwards.

<details>
<summary>Spoilers</summary>

1. **Overdue fee is off by one, twice.** The stated policy is "first three days late are free, 25c/day after". The implementation charges from day 3 and overcharges by one day thereafter.
2. **`borrow()` never calls `can_borrow()`.** Suspended members can borrow. The test that would catch it is skipped with "flaky on CI" — which is the tell.
3. **Pagination is 0-based but documented as 1-based.** The test asserts page 0, encoding the bug.
4. **Weak assertions.** `assertGreater(fee, 0)` passes for almost any wrong implementation.
5. **Slow suite.** Three tests sleep 1.5s each.

</details>
