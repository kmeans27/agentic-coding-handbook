# Lab 07 · Parallel isolation

**Time:** 60 min · **Track:** terminal · **Trains:** principle 9

> Two agents in one checkout is not parallelism. It is a race condition with a
> natural-language interface.

---

## The situation

You have two independent features:

- **A — renewals:** add `renew(loan, member, today)` and a renewal counter.
- **B — reservations:** add `reserve_book(member, book, reservations)`.

Both touch `library/loans.py`. Both touch `library/models.py`. You want them
done at the same time.

The naive approach is two terminal sessions in the same directory. It appears
to work for the first few minutes, which is the dangerous part.

This lab makes the collision happen, then fixes it with worktrees, then asks
what worktrees do **not** isolate.

---

## What you will produce

- Evidence of the collision, or a reasoned account of why your harness
  serialised the work.
- Two worktrees with separate branches and separate agent sessions.
- A merge sequence with the conflict resolved.
- A list of shared state that a worktree does not fix.
- An honest speedup number, including the merge cost.

---

## Steps

### 1. Prepare two task briefs

Write each as a pointer prompt, not an essay:

```text
TASK A
Goal: add loan renewals.
Where: library/loans.py, library/models.py.
Contract: SPEC-A.md, copied into the worktree from
$HANDBOOK/exercises/answer-key/renewals-spec.md.
Check: new tests in tests/test_renewals_a.py; make test-fast passes.
Do not touch: tests other than the new file.
```

```text
TASK B
Goal: add book reservations.
Where: library/loans.py.
Contract: a suspended member cannot reserve, and a member at their loan limit
cannot reserve. Reservations are dicts with member_id and book_id.
Check: new tests in tests/test_reservations_b.py; make test-fast passes.
Do not touch: tests other than the new file.
```

Task B's brief is already better than the review diff in Lab 08. That is
deliberate: the lab is about isolation, not about planting bugs.

### 2. Version 1 — one checkout, two sessions

Start from a clean copy (the baseline commit from Setup is already there):

```bash
rm -rf /tmp/lab07 && cp -r /tmp/lab-sandbox /tmp/lab07
cd /tmp/lab07
git log --oneline        # one commit: baseline
```

Open two agent sessions in the **same directory**. Start both tasks at roughly
the same time. Do not stagger them; the point is the overlap.

Record what happens:

```bash
git status
git diff --stat
git log --oneline
make test
```

Look for:

- both features' changes in one diff,
- one agent's edit disappearing after the other writes the file,
- a commit that contains part of both features,
- `index.lock` errors,
- tests failing for reasons neither task introduced,
- an agent running `git checkout -- .` and erasing the other's work.

If your harness serialises tool calls across sessions (some do), you may not
get a hard collision. That is a finding, not a failure: your "parallelism" was
an illusion, and the wall-clock time will show it. Record that.

### 3. Version 2 — two worktrees

Reset to a clean repository, then:

```bash
git worktree add ../wt-renewals -b feature/renewals
git worktree add ../wt-reservations -b feature/reservations
git worktree list
```

Each directory has its own working tree, index, and `HEAD`. They share the
object database and refs, which is what makes merging cheap.

Run one agent in each directory, on its own branch. Same two briefs.

Confirm isolation:

```bash
cd ../wt-renewals && git status --short --branch
cd ../wt-reservations && git status --short --branch
```

Different branches, different changes, no interference. Neither agent can see
the other's uncommitted work — which is the point, and also the cost: they
cannot coordinate.

### 4. Merge, one at a time

```bash
cd /tmp/labNN                 # the primary checkout
git merge --no-ff feature/renewals
make test

git merge --no-ff feature/reservations
# expect a conflict in library/loans.py if both added functions at the same anchor
```

Resolve the conflict by hand. Do not ask an agent to resolve a conflict between
two changes it did not see in full; you are the only participant with both
contexts.

After each merge: `make test`. A merge that is textually clean can still be
semantically broken — both features add a function, both compile, and the
combined behaviour is wrong.

### 5. List what worktrees do not isolate

Worktrees isolate files, index, and `HEAD`. They do not isolate:

| Shared resource | Symptom |
|---|---|
| A development database | Both agents migrate or truncate the same tables |
| A fixed port | Second server fails to bind, or silently talks to the first |
| A package cache / lockfile | One install rewrites what the other is using |
| `.env` or credentials | One agent changes config for both |
| A build output directory outside the worktree | Stale artefacts, flaky results |
| A remote branch | Both push to the same name; one is rejected or overwrites |

For each, write the isolation mechanism you would use: a per-worktree database
name, a port derived from the worktree, a separate cache directory, a branch
per task, a container per session.

The general rule: **isolate the filesystem, the runtime state, and the
namespace.** Worktrees handle the first. You handle the other two.

### 6. Measure the speedup honestly

Time each version from first prompt to two merged, green features.

| Version | Wall clock | Rework (minutes) | Merge conflicts |
|---|---|---|---|
| One checkout | | | |
| Two worktrees | | | |

Expect less than 2×. Setup, merge, conflict resolution, and review are serial.
If the tasks are small, the coordination cost can exceed the gain — which is a
legitimate result. Parallelism is for independent work with a real duration,
not for two twenty-minute edits.

---

## Acceptance criteria

- [ ] You ran both versions, or explained precisely why your harness prevented
      the collision.
- [ ] Two worktrees, two branches, two sessions.
- [ ] A merge sequence with `make test` after every merge.
- [ ] The conflict is resolved by hand, with a reason.
- [ ] At least four non-filesystem shared resources listed with mitigations.
- [ ] Speedup reported including rework and merge time.

---

## Debrief

1. Why is a clean textual merge not evidence that the combined change is
   correct?
2. Which of the two features would you merge first, and what does the answer
   depend on?
3. When is parallelism *not* worth it, even with perfect isolation?

---

<details>
<summary><strong>Solution, model answer, and grading</strong></summary>

### The commands

```bash
# once, from a clean repo
git worktree add ../wt-renewals -b feature/renewals
git worktree add ../wt-reservations -b feature/reservations

# in each worktree, a separate agent session
cd ../wt-renewals      && <agent>
cd ../wt-reservations  && <agent>

# merge serially in the primary checkout
git merge --no-ff feature/renewals
make test
git merge --no-ff feature/reservations
make test

# clean up
git worktree remove ../wt-renewals
git worktree remove ../wt-reservations
```

`git worktree list` is the ground truth. If a worktree is missing from that
output, it is just a directory, and you are back to a shared checkout.

### What the collision looks like

The most common version is not an error. It is a **silent overwrite**: agent A
writes `loans.py`, agent B writes `loans.py` from its own stale read, and A's
function is gone. The tests still pass because B's tests do not reference A's
function. You discover it at merge time, or in production.

The second most common is a **mixed commit**: one agent runs `git add -A` and
commits both features plus a half-finished edit. The commit message describes
one feature. The diff contains two.

The third is **destructive recovery**: an agent hits a confusing test failure,
runs `git checkout -- .` or `git reset --hard`, and erases the other session's
uncommitted work. There is no undo for that.

Worktrees prevent all three by giving each session its own index and working
tree. They do not prevent the fourth: shared runtime state.

### Merge order

Merge the change that alters shared interfaces first, then rebase the other
onto it. Here both add functions to `loans.py` and a field to `models.py`;
neither changes an existing signature, so order is mostly arbitrary. Choose the
smaller, better-tested change first, so the second merge is resolved against a
known-good baseline.

If both features changed the same signature, the order would be determined by
which one is harder to rebase — merge that one first.

### Why a clean merge can still be broken

Git merges text. It does not know that:

- both features compute eligibility differently, and one silently shadows the
  other,
- both add a field named `renewals` for different purposes,
- A's test passes only because B's change altered a shared default,
- the combined feature exceeds a limit that neither change alone exceeded.

The only detector is running the **full** suite after each merge, plus a review
of the combined diff. A textual conflict is the easy case because it forces you
to look. A clean merge is the dangerous case.

### What worktrees do not isolate

| Resource | Mitigation |
|---|---|
| Database | One schema/database per worktree, named after the branch |
| Ports | Derive from an env var; never hard-code 3000 |
| Caches | `XDG_CACHE_HOME` or a project-local cache per worktree |
| `.env` | Per-worktree file, generated from a template; never committed |
| Build output | Inside the worktree, or keyed by branch |
| Remote branches | One branch per task; never push to the same name |
| Credentials | A shared read-only source, not a mutable file |

The pattern is: **anything with a name that two processes can collide on must
be namespaced.**

### The speedup

For two 20-minute tasks, two worktrees typically finish in 25–35 minutes of
wall clock, not 20, because you still review both diffs and resolve the merge
yourself. That is a 1.2–1.6× gain, not 2×.

The gain becomes real when the tasks are long and independent: a migration and
a UI change, a test-suite build-out and a dependency upgrade. It is negative
when the tasks touch the same three files, because the merge cost exceeds the
overlap.

### Grading

| Score | Submission |
|---|---|
| **3** | Both versions run; collision or serialisation documented; worktrees correct; merge tested; non-filesystem state listed with mitigations; honest speedup. |
| **2** | Worktrees work and merge is clean, but no collision evidence or no state analysis. |
| **1** | Two directories created by copying instead of worktrees, or one branch used for both. |
| **0** | "I would just use two terminals" with no experiment. |

### Common failures

- **Copying the directory instead of `git worktree`.** Two copies are two
  repositories. Merging them is manual, and the object database is duplicated.
- **One branch in both worktrees.** Git refuses to check out the same branch
  twice, which is a feature. Use distinct branches.
- **Running the agent in the primary checkout for one task.** Then one side is
  isolated and the other is not; you have half a fix.
- **Merging both at once.** `git merge feature/a feature/b` is an octopus merge;
  if it conflicts, you get one combined conflict and no per-feature test point.
  Merge one at a time.
- **Forgetting cleanup.** Stale worktrees accumulate. `git worktree prune`
  after removing directories by hand.

</details>
