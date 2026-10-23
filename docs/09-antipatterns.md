# 09 · Antipatterns

Twelve failure modes. Each one is a mechanism you already met in an earlier chapter, showing up in practice.

---

### 1. The kitchen-sink session

**Symptom** — One session, three unrelated tasks, mounting confusion, "why did it edit that?"
**Cause** — Context accumulates irrelevant material and never gets cleared.
**Fix** — One task per session. Clear between tasks. If you are re-explaining background, it belongs in a file.

---

### 2. The correction spiral

**Symptom** — "No, not like that." × 5. Each attempt slightly worse.
**Cause** — Failed attempts stay in context and bias the next attempt. You are now optimising against ghosts.
**Fix** — After two failed corrections: clear, and rewrite the request incorporating what you learned. A clean session with a better prompt beats a polluted one with a better threat.

---

### 3. The encyclopaedia rules file

**Symptom** — The agent ignores rules that are clearly written in the file.
**Cause** — The file is too long. Important instructions are diluted by things the model already knows or can read from the code.
**Fix** — Delete every line that fails *"would removing this cause a mistake?"*. Convert anything that must always hold into a hook, lint rule, or test.

---

### 4. Trust, then verify

**Symptom** — A plausible implementation that misses the edge cases; discovered in review or production.
**Cause** — No check existed, so "looks done" was the only stopping condition.
**Fix** — Define the acceptance check *before* delegating. Ask for evidence, not assurance. If you cannot verify it, do not delegate it.

---

### 5. Infinite exploration

**Symptom** — "Investigate the codebase" → 200 files read, no answer, context exhausted.
**Cause** — Unbounded research question with no budget.
**Fix** — Scope the question ("how does token refresh work in `src/auth`?"), or delegate it to a subagent that returns a summary. Never let exploration into the context you will edit from.

---

### 6. Test tampering

**Symptom** — Green tests, broken behaviour. The diff includes deleted assertions.
**Cause** — The goal given was "make the tests pass", and that was the cheapest path.
**Fix** — Review test diffs as carefully as source. Require that a bug fix starts with a failing test you have watched fail. Treat snapshot regeneration as suspicious by default.

---

### 7. Spec drift

**Symptom** — The change is correct, plus a refactor you did not ask for, plus a new dependency.
**Cause** — No stated boundary, and models are trained to be helpful.
**Fix** — Put **Out of scope** in every spec. Review the diff against the plan, not against your general hopes. Revert unrelated changes rather than accepting them.

---

### 8. Review theatre

**Symptom** — A review happened; nothing was caught; the incident was in the reviewed code.
**Cause** — The reviewer shared the writer's context, or was asked for "any feedback", or was an agent that had already decided the work was good.
**Fix** — Fresh context. Give the plan and the diff only. Ask for correctness gaps against stated requirements, not opinions. Have the reviewer try to *refute* the change.

---

### 9. Parallel collision

**Symptom** — Unexplained lost edits, duplicated work, a "model failure" that is actually a race.
**Cause** — Two sessions in the same checkout, or sharing a database, port or cache.
**Fix** — One worktree per task. Per-worktree database and ports. Never two writers on one branch.

---

### 10. Prompt alchemy

**Symptom** — Endless tweaking of wording, magic phrases, saved prompt collections, benchmark-chasing.
**Cause** — Optimising the cheapest lever instead of the highest-leverage one.
**Fix** — Fix the environment: faster tests, a real check, a shorter rules file, a clearer spec. A mediocre prompt against a good check beats a perfect prompt against nothing.

---

### 11. Modernisation drift

**Symptom** — Unrelated upgrades inside feature work; comments that no longer match reality.
**Cause** — Upgrades are cheap for agents, so they happen opportunistically.
**Fix** — Upgrades are their own commit, with the changelog read. Update or delete the comments that justified the old behaviour. Never let "while I was in there" touch dependencies.

---

### 12. Cognitive debt

**Symptom** — You ship quickly and understand less each month. You cannot debug your own system.
**Cause** — Reviewing for plausibility rather than comprehension; never reading the full diff.
**Fix** — Read every diff. Explain each significant change in your own words before merging. Keep one thing you build without the agent. See [chapter 08](08-judgment.md).

---

## The meta-antipattern

All twelve share one root:

> **Treating a finite, degrading resource as if it were infinite — and treating a claim as if it were evidence.**

Context is finite. Your attention is finite. Verification capacity is finite. An agent's confidence is not correlated with its correctness. Every fix above is a way of respecting one of those facts.

If you remember nothing else from this repository: **make the check real, and keep the loop small.**

---

**Next:** [Reading canon](../reading/README.md) — the sources behind all of this, annotated and dated.
