# Lab 06 · Make the loop fast

**Time:** 45 min · **Track:** terminal · **Trains:** principle 7 · **Assumes:** Lab 01

> A test suite you avoid running is a test suite that does not exist.

---

## The situation

Measured on the sandbox, median of five runs:

| Command | Time | Theoretical runs/hour |
|---|---|---|
| `make test` | 4.56 s | 789 |
| `make test-fast` | 0.035 s | ~100,000 |

The fast path is already there. The problem is that it does not include the
test you wrote in Lab 01, so the fast path cannot catch the fee bug. Running it
feels productive and verifies the wrong thing.

There is also a trap waiting: the slow tests are slow because of a `sleep`, and
the easiest way to make the number better is to delete them. That improves the
metric and destroys the coverage. This lab is about getting the number down
**without** losing detection.

---

## What you will produce

- Before/after medians, with the method stated.
- A two-tier loop: fast default, full before push.
- Proof that the fast tier still catches a real regression.
- A judgement on whether to optimise the slow tests or isolate them.

---

## Steps

### 1. Measure, do not estimate

```bash
python3 - <<'PY'
import subprocess, time, statistics
for target in ("test-fast", "test"):
    vals = []
    for _ in range(5):
        t = time.perf_counter()
        subprocess.run(["make", target], capture_output=True)
        vals.append(time.perf_counter() - t)
    print(target, "median %.3fs" % statistics.median(vals))
PY
```

Five runs, median. One run is noise: the first `make` pays for process startup
and `__pycache__` may be cold.

Record the numbers. You will need them at the end.

### 2. Find where the time goes

```bash
python3 -m unittest tests.test_integration -v
```

Three tests, each about 1.5 s, all from `setUp`:

```python
def setUp(self):
    time.sleep(1.5)
```

That is a stand-in for booting a service. In a real suite it might be a
database, a container, or a fixture that rebuilds the world for every test.

Most slow suites are slow for one of four reasons: repeated setup, real I/O,
sleeps/polling, or too much scope per test. Name the cause before optimising.

### 3. Notice the gap

```bash
make test-fast
```

It passes. Now reintroduce the fee bug and run it again:

```bash
git apply -R "$HANDBOOK/exercises/answer-key/fix-fee.patch"
make test-fast
```

If it still passes, your fast tier is decorative. Lab 01's boundary test lives
in `tests/test_fee_boundaries.py`, which `test-fast` does not run. Fix the
Makefile:

```make
test-fast:
	python3 -m unittest tests.test_loans tests.test_policy tests.test_fee_boundaries -q
```

Now the same command must fail. If it does not, you have found the actual
problem: speed was never the bottleneck, detection was.

Restore the fix:

```bash
git apply "$HANDBOOK/exercises/answer-key/fix-fee.patch"
```

### 4. Design two tiers

| Tier | When | Contents | Budget |
|---|---|---|---|
| **Fast** | Every edit; the agent runs it after every change | Unit tests for the code you are touching | < 1 s |
| **Full** | Before push, and in CI | Everything, including integration | Minutes are fine |

`make verify` should be the fast tier plus lint. `make test` stays the full
tier. Do not weaken `make test` to make it fast; add a tier.

The rule is not "all tests must be fast". It is "the tests that gate each edit
must be fast, and the slow tests must still gate the merge".

### 5. Optimise the slow tier honestly

The sleep is per test. The service only needs to boot once per class:

```diff
-    def setUp(self):
+    @classmethod
+    def setUpClass(cls):
         time.sleep(1.5)
```

Measure again. It should drop from ~4.5 s to ~1.6 s.

This is a real trade: tests in the class now share state. Here they only create
local objects, so it is safe. In a suite with a shared database it would not
be. State the assumption when you make the change; do not copy the pattern
blind.

If the slow tests cannot be made faster without risking shared state, leave
them slow and move them to the full tier. That is a valid answer. A slow test
that runs before push is worth more than a fast test that no longer tests
anything.

### 6. Measure the loop, not the suite

Time yourself on one small change:

1. Edit a line.
2. Run the fast tier.
3. Read the failure.
4. Fix it.

Do that three times and average. The suite is 0.035 s; the loop is dominated by
your reading and the agent's turn. Cutting the suite from 4.5 s to 0.035 s
matters because it removes a fixed cost from every one of those turns — not
because 0.035 s is an impressive number.

### 7. Prove the tier still detects

With the fast tier green, break something on purpose:

```bash
git apply -R "$HANDBOOK/exercises/answer-key/fix-fee.patch"
make verify        # must fail
git apply "$HANDBOOK/exercises/answer-key/fix-fee.patch"
make verify        # must pass
```

This is the only evidence that matters. A fast suite that cannot fail is a
no-op with good latency.

---

## Acceptance criteria

- [ ] Medians from at least five runs, before and after.
- [ ] `make verify` is sub-second and includes the boundary test.
- [ ] Reintroducing the fee bug makes `make verify` fail.
- [ ] The slow tests still run somewhere (full tier or CI).
- [ ] You can name the cause of the original slowness.
- [ ] A written policy: what runs when.

---

## Debrief

1. `make test-fast` was fast before this lab. Why was that not enough?
2. Deleting `test_integration.py` would make `make test` fast too. What would
   you lose, and how would you know?
3. Why is "the suite is fast" a weaker claim than "the suite fails when the bug
   is present"?

---

<details>
<summary><strong>Solution, model answer, and grading</strong></summary>

### The numbers

| State | `make test` | `make verify` | Note |
|---|---|---|---|
| Baseline | 4.56 s | 0.035 s | Fast tier misses the boundary test |
| Fast tier fixed | 4.56 s | ~0.04 s | Detection restored |
| `setUpClass` | ~1.6 s | ~0.04 s | Setup amortised over three tests |
| Tests deleted | 0.04 s | 0.04 s | Faster, and worthless |

The third row is an optimisation. The fourth is a metric improvement. They look
identical on a dashboard.

### The Makefile change

```diff
 test-fast:
-	python3 -m unittest tests.test_loans tests.test_policy -q
+	python3 -m unittest tests.test_loans tests.test_policy tests.test_fee_boundaries -q
```

That is the most important line in the lab. Everything else is tuning.

### The integration change

```diff
-    def setUp(self):
+    @classmethod
+    def setUpClass(cls):
         time.sleep(1.5)
```

`setUpClass` runs once per class; `setUp` runs before every test. Three tests
at 1.5 s each become one 1.5 s boot plus three fast tests.

The trade is shared state. Here each test builds its own `Member` and list, so
nothing leaks. In a suite that mutates a shared database, this change would
introduce order dependence — the classic symptom is tests that pass alone and
fail together.

### The loop policy

| Event | Command | Budget |
|---|---|---|
| After a small edit | `make verify` | < 1 s |
| Before asking for review | `make test` | < 10 s here |
| Before push / in CI | `make test` + lint | Minutes acceptable |
| Nightly | full suite + slow integration | Hours acceptable |

Two tiers is usually enough. Three is fine. Zero (only the full suite) means
the agent waits four seconds for every trivial edit, and eventually you stop
asking it to run tests at all.

### Why the baseline fast tier was useless

It ran the tests that existed before Lab 01, not the test that encodes the
contract. This is a general failure: the fast tier is configured once and never
updated when new tests are added. Prefer discovery with a marker:

```bash
python3 -m unittest discover -s tests -t . -p "test_*.py" -q   # everything
```

and, in a real project, a marker or naming convention for slow tests, so new
fast tests are included automatically rather than by hand.

### Grading

| Score | Submission |
|---|---|
| **3** | Real medians; fast tier includes the boundary test; regression proof both ways; slow tests preserved; state trade-off named. |
| **2** | Numbers and tiers, but no regression proof, or the boundary test is still outside the fast tier. |
| **1** | Made the suite fast by deleting or skipping slow tests. |
| **0** | Did not measure; "it feels faster". |

### Common failures

- **Deleting the slow tests.** The number improves and the coverage does not.
  This is the trap the lab is built around.
- **Moving the bug-catching test into the slow tier.** Then the fast tier is
  green while the code is broken. Detection belongs where the edits happen.
- **Optimising lint.** Lint is already milliseconds. Profile before tuning.
- **One measurement.** The first run is always slower. Use a median.
- **Forgetting CI.** A fast local loop plus a full CI run is the design. A fast
  local loop with no CI is a coverage hole with good latency.

</details>
