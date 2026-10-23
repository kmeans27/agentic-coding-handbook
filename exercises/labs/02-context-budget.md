# Lab 02 · The context budget

**Time:** 45 min · **Track:** paper or terminal · **Trains:** principle 2

> Context is not free. Every line you supply is a line the agent must weigh.

---

## The situation

The same one-line bug, two ways of asking for a fix:

- **Run A** — paste the entire repository, the rules file, and the full test
  output into the prompt.
- **Run B** — name the file, the symbol, the contract, and the check.

Most people assume A is safer ("more context can't hurt") and B is faster but
riskier. Neither assumption survives measurement.

This lab is about producing the measurement, not about confirming a slogan. On
a four-file repository, the dump may well win. That is a legitimate finding —
and it tells you where the crossover is.

---

## What you will produce

- A filled comparison table from two runs of the same task.
- A one-sentence rule for when you will dump and when you will point.
- A reusable pointer prompt for a repository you actually work in.

---

## Steps

### 1. Build the payload for Run A

From a clean sandbox copy:

```bash
wc -c library/*.py tests/*.py AGENTS.md SPEC.md
make test 2>&1 | tail -20
```

Concatenate the four source files, `AGENTS.md`, and the test output. That is
your payload. Estimate its size in tokens as characters ÷ 4. Write the number
down; do not guess later.

Prompt:

```text
Here is my codebase. Fix the pagination bug.

<paste everything>
```

### 2. Run A

Use a fresh session — no memory of this repository. Record:

| Metric | Run A | Run B |
|---|---|---|
| Input tokens (estimate) | | |
| Files the agent opened itself | | |
| Assistant turns | | |
| Wall-clock time | | |
| Correct fix? | | |
| Unrelated edits in the diff? | | |

"Files opened itself" matters. A dump does not stop the agent from reading
more; it only front-loads the cost.

### 3. Build the pointer prompt for Run B

Fresh session. Same task. No dump:

```text
Goal: make pagination 1-based, as documented.

Where: library/loans.py, function `paginate`.
Contract: the module docstring in that file says page 1 is the first page.
Current behaviour: page index is multiplied directly by size.

Change: the implementation, plus the one test that calls `paginate` with
page=0. Run `grep -rn "paginate(" .` first and confirm there are no other
callers.

Check: `make test-fast` passes, and `paginate(range(1,26), 1, 10)` returns
[1..10].

Do not touch: the fee logic, the docstring, or any other test.
If the call-site search finds a caller outside tests, stop and report it.
```

Run it, record the same metrics.

### 4. Compare honestly

Answer these in writing:

1. Did Run A produce a larger diff? Open both diffs and count changed lines.
2. Did Run A read files that were irrelevant to the bug?
3. Was the token difference 2×, 10×, or 100×?
4. Did either run do something you did not ask for?
5. Which run would you rather review, and why?

### 5. Extrapolate

Estimate the same two prompts against a 10× larger repository (40 files) and a
100× one (400 files). You do not need to run it. The payload grows linearly;
the pointer stays roughly constant. At what size does the dump stop fitting in
a comfortable context window?

### 6. Write your rule

One sentence, in the form:

> I dump when ______, and I point when ______.

It must be falsifiable. "I always point" is not a rule, it is a slogan.

---

## Paper variant

If you cannot run an agent:

1. Write both prompts in full.
2. Highlight every line of Run A that is **payload** (code, logs, restated
   facts already in the repo) versus **pointer** (a location, a contract, a
   check).
3. Estimate the token counts.
4. Predict which run reads more irrelevant files, and which produces the
   larger diff.
5. Rewrite your own last agent prompt in pointer form. That is the artefact.

---

## Acceptance criteria

- [ ] Both runs used a fresh session and the same task.
- [ ] The table is filled with real numbers, not impressions.
- [ ] Both diffs were read, not just the test result.
- [ ] Your rule names a condition for dumping, not just a preference.
- [ ] You can explain what the dump bought, if anything.

---

## Debrief

1. What did the dump actually buy? Name a specific thing, or say "nothing".
2. What did it cost? Tokens are the obvious answer; name one non-obvious cost.
3. Why is "more context is always better" false *even when the extra context is
   accurate*?

---

<details>
<summary><strong>Solution, model answer, and grading</strong></summary>

### What usually happens

On this repository, the honest result is often close:

| Metric | Run A (dump) | Run B (pointer) |
|---|---|---|
| Input tokens | ~3,000–5,000 | ~150–250 |
| Files opened itself | 0–1 | 1–2 |
| Turns | 1 | 1–2 |
| Correct fix | usually | usually |
| Unrelated edits | more likely | rare |

Both can be correct. The dump is not stupid on a four-file repo — it is simply
paying 20× for insurance it does not need. The point is that you now know the
price. At 40 files the insurance premium becomes a real constraint; at 400 it
does not fit.

If your Run A was faster and cleaner: good. Record the crossover rather than
forcing the conclusion. The rule is "measure", not "always point".

### Why the dump can be worse even when accurate

Three mechanisms:

1. **Attention is finite.** Long inputs dilute the weight of any single line.
   The relevant docstring is one sentence among thousands. Retrieval-style
   benchmarks consistently show recall degrading with input length; treat that
   as a reason to keep inputs lean, not as a precise law.
2. **The agent cannot tell signal from noise.** A dump includes dead code,
   stale comments, and the bug itself, all presented with equal authority. A
   pointer tells it which contract is binding.
3. **It hides what you know.** Writing "the docstring says 1-based" forces you
   to check the docstring. Pasting everything lets you skip the part where you
   understand the task — and that understanding is the actual product.

The dump also has a real advantage: it removes the risk that your pointer
omits something the agent needed. That is why the rule is conditional.

### A good pointer prompt

```text
Goal: <one sentence, observable outcome>
Where: <file:symbol>
Contract: <the authoritative source: docstring, spec section, test name>
Change: <what must differ, not how to implement it>
Check: <exact command + expected result>
Do not touch: <files, tests, docs>
If <condition>: stop and report instead of guessing.
```

Six lines. Every line is a pointer or a constraint. None of it is a restatement
of code the agent can read itself.

### A good rule

Acceptable:

> I dump when the repository is small enough that the whole thing fits under a
> few thousand tokens and I do not yet know where the relevant code lives. I
> point once I can name the file and symbol.

Not acceptable:

> I always point, because context is a budget.

The second is a slogan: it does not tell you what to do on an unfamiliar
codebase, where pointing is impossible until you have explored.

### Grading

| Score | Submission |
|---|---|
| **3** | Real numbers for both runs; diffs compared; a conditional rule; explains a non-obvious cost of dumping. |
| **2** | Numbers recorded, rule written, but comparison limited to tokens and correctness. |
| **1** | One run only, or the conclusion was written before the measurement. |
| **0** | No artefact, or a rule that cannot be falsified. |

### Common failures

- **Different tasks.** Run A says "fix the bug", Run B says "make it 1-based
  and update the test". That is not a context experiment; it is two tasks.
- **Same session.** The second run remembers the first, so the pointer is
  doing no work. Start fresh.
- **Judging by the answer text.** Read the diff. An agent can produce a
  confident, correct-sounding summary of a wrong change.
- **Ignoring tool calls.** A small prompt that triggers twelve file reads is
  not a small context. Count what was read, not what you typed.

</details>
