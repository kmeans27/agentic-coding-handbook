# Lab 05 · Rules-file surgery

**Time:** 45 min · **Track:** paper or terminal · **Trains:** principle 6

> A rules file is not a description of your project. It is a list of things the
> agent would otherwise get wrong.

---

## The situation

`AGENTS.md` is 96 lines and 613 words. It contains:

- generic advice ("write clean code", "consider edge cases"),
- the same advice three times,
- a file map the agent can generate with `ls`,
- a domain tutorial that duplicates the docstrings,
- two rules that contradict each other,
- one rule that is simply false (`pytest` is not installed),
- and, buried in the middle, four lines that actually matter.

Everything in it is read on every task. The four useful lines are competing
with ninety-two lines of noise, and the false line actively causes failures.

Your job is to cut it to under 40 lines without losing a single rule that
prevents a real mistake.

---

## What you will produce

- A classification of every line: keep, move, or delete.
- A rules file under 40 lines.
- Evidence from three A/B tasks that it still works.
- A one-sentence heuristic for what belongs in a rules file.

---

## Steps

### 1. Count and read

```bash
wc -l AGENTS.md
wc -w AGENTS.md
```

Read it once, slowly. Mark every line that would cause a **specific, observable
mistake** if it were removed. Not "would be nice". A mistake you could point
at in a diff.

Most people mark 4–7 lines. The file has 96.

### 2. Find the contradictions

You are looking for pairs that cannot both be obeyed:

- "Always ask before running tests" vs "run the full suite before every
  commit".
- "Ask when in doubt" vs "be autonomous and do not interrupt".
- "Always write tests for new behaviour" vs "do not add tests for things that
  are obviously correct".
- "Do not modify tests" vs "(Exception: you may add tests freely.)"

Write them down. A contradiction does not just waste attention; it gives the
agent an excuse to pick whichever side is convenient.

### 3. Find the false rule

```bash
python3 -m pytest --version
```

There is no pytest. The rules file says to use it. An agent that follows the
file will either fail a command, waste a turn, or try to install a dependency —
which violates the "stdlib only" rule two sections above.

A false rule is worse than no rule, because it is followed.

### 4. Classify every line

Use four filters, in order:

| Filter | Question | Destination |
|---|---|---|
| **True?** | Is this factually correct for this repo? | If no: delete. |
| **Non-obvious?** | Could a competent engineer infer it from the code? | If yes: delete. |
| **Enforceable?** | Can a hook, CI check, or type system enforce it? | If yes: move to tooling. |
| **Specific?** | Does it prevent a mistake you have actually seen? | If no: delete. |

Only lines that pass all four stay. Most generic advice fails filter 1 or 4;
the file map fails filter 2; "do not commit `__pycache__`" fails filter 3
(`.gitignore`).

### 5. Write the new file

Target: under 40 lines, no duplicates, no contradictions, no false statements.
Keep the commands, because an agent cannot guess `make verify`. Keep the domain
invariants that have already caused bugs. Delete the rest.

Start your own version before opening
[`answer-key/AGENTS.pruned.md`](../answer-key/AGENTS.pruned.md).

### 6. A/B test it

Three tasks, two sessions each (old file, new file). Fresh copies.

| Task | Prompt | What to check |
|---|---|---|
| Money units | "Add a `late_fee_cents(days_late)` helper." | Returns integer cents, not float dollars. |
| Tests | "The fee test is too weak. Make it stronger." | Does it strengthen the assertion, or stop and ask, rather than delete it? |
| Commands | "Run the tests and report." | Runs `make verify` or `make test`; never `pytest`. |

Score each 0 or 1. The old file should lose at least the commands task — that
one is deterministic. The others depend on the model; record what happened
rather than forcing a result.

### 7. Prune again

After the A/B test, ask of every remaining line: "Did any run need this?" If
not, and it is not a known trap, cut it. The target is the smallest file that
still prevents the three failures above.

---

## Paper variant

Do steps 1–5 only. The classification table is the artefact. Then take a rules
file from a project you actually own and run the same four filters on it. Most
real rules files are 80% file maps and generic virtues.

---

## Acceptance criteria

- [ ] Every line classified, with a reason.
- [ ] All four contradictions identified.
- [ ] The false `pytest` rule removed and the failure demonstrated.
- [ ] Final file is under 40 lines and contains the commands.
- [ ] Three A/B tasks run, with results recorded.
- [ ] A heuristic in one sentence.

---

## Debrief

1. Which is worse: a missing rule or a false rule? Why?
2. The file map duplicated information the agent can get from `ls`. What did
   that duplication cost?
3. Why do rules files tend to grow, and what stops them?

---

<details>
<summary><strong>Solution, model answer, and grading</strong></summary>

### The pruned file

See [`answer-key/AGENTS.pruned.md`](../answer-key/AGENTS.pruned.md). Thirty
lines. It keeps:

| Kept rule | Why it survives |
|---|---|
| Python 3.10+, stdlib only | Environment fact. Prevents dependency additions that would break the sandbox. |
| Money is integer cents | A real bug class. The code has a fee calculation; floats would be silent and wrong. |
| Day numbers are ints, not `datetime` | Non-obvious domain convention. An agent's default is `datetime`. |
| Pages are 1-based | Currently load-bearing: the implementation contradicts it. Remove once the code and docstring agree. |
| Policy lives in `policy.py` | Architectural constraint. Not inferable from a 40-line module. |
| `make verify`, `make test` | Commands cannot be guessed. Highest-value lines in the file. |
| There is no pytest | A negative fact. Prevents a deterministic failure. |
| Never weaken a test to pass | Process rule, not enforceable by a linter. Directly prevents the Lab 04 failure. |

Everything else goes. The file map is `ls`. The domain tutorial is the
docstring. "Write clean code" is a wish.

### Why the false rule matters most

A missing rule produces an unprompted choice. A false rule produces a
*confident wrong action*: the agent runs `pytest`, gets `No module named
pytest`, and then has three bad options — install it (violating stdlib-only),
give up, or guess another command. You have spent a turn and, worse, taught it
that the file is unreliable.

The same applies to the non-existent `docs/` and `scripts/` directories. They
are not harmful on their own, but they teach the agent that the file describes
an imagined repository. Once one line is known to be false, every line is
suspect.

### The four filters, applied

| Line | Verdict | Reason |
|---|---|---|
| "Write clean, readable code" | Delete | Not specific; no observable mistake. |
| File map | Delete | Inferable with `ls`; goes stale. |
| "Always ask before running tests" | Delete | Contradicts the workflow rule and blocks autonomy. |
| "Use pytest" | Delete | False. |
| "No third-party dependencies" | Keep | True, non-obvious, enforceable in review, prevents a real failure. |
| "Run `make verify`" | Keep | Not inferable; exact command. |
| "Do not commit `__pycache__`" | Move | `.gitignore` does it deterministically. |
| "Money in cents" | Keep | Domain invariant; floats are the default mistake. |

### The heuristic

> If removing a line would not cause a specific mistake you could point to in a
> diff, the line is costing attention and buying nothing.

Corollary: rules files should shrink as the codebase becomes more
self-describing. A rule that compensates for a bad interface is a signal to fix
the interface, not to add another paragraph.

### Grading

| Score | Submission |
|---|---|
| **3** | <40 lines; all contradictions and the false rule found; A/B results recorded honestly; heuristic is specific; every remaining line justified. |
| **2** | Good prune, but a contradiction or the A/B test is missing. |
| **1** | Cut by length rather than by filter; lost the commands or a domain invariant. |
| **0** | Rewrote the file with different generic advice, or deleted it entirely without replacing the commands. |

### Common failures

- **Keeping "write tests" but deleting the test-integrity rule.** The generic
  one is agreeable; the specific one prevents the failure.
- **Pruning until the file is empty.** The commands and domain invariants are
  the point. A short file that omits `make verify` is worse than a long one
  that includes it.
- **Judging by length alone.** 39 lines of noise is not an improvement on 96
  lines with four useful rules. The filters come first; the line count is a
  consequence.
- **A/B testing with different prompts.** The only variable should be the rules
  file.

</details>
