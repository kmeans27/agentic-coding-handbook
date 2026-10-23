# 08 · Judgment

> **Principles 11 and 12** — Stay the engineer. Measure outcomes, not activity.

---

## Cognitive debt

Technical debt is code you will have to fix later. **Cognitive debt is understanding you will have to rebuild later** — and it is the occupational hazard of agentic coding.

It accumulates quietly:

- You merge a diff you did not fully read.
- You cannot explain why an abstraction exists.
- You fix a bug by asking the agent to "look into it" and accepting the result.
- You know the tests pass but not what they cover.
- You could not reproduce the change without the tool.

None of these are emergencies. All of them compound. Six months later you have a codebase you are nominally responsible for and cannot reason about — and the agent cannot reason about it either, because the model of it lives only in the code, and the code has become something nobody designed.

> **The test:** open a file you changed last month. Can you explain what it does, why it is shaped that way, and what would break if you changed it? Without the agent open.

If the answer is no, you have borrowed against your future.

---

## Why this is a performance problem, not a purity problem

There is a tempting response: "who cares, the agent can read it later". Three reasons that fails:

1. **You cannot review what you do not understand.** Review is the control that makes delegation safe. Without it you are not directing, you are approving.
2. **You cannot debug what you did not design.** Production failures arrive with sparse signals. The agent's advantage is weakest exactly when the pressure is highest.
3. **You cannot make good architectural decisions from a position of ignorance.** The next design builds on the current one. If your understanding decays, your judgement decays, and the codebase drifts in ways no test catches.

The uncomfortable part: **the better the agent gets, the more tempting this becomes.** A junior engineer who does not understand the code notices immediately, because they cannot get anything done. A senior engineer with an agent can keep shipping for a long time on a shrinking foundation. The feedback is delayed, not absent.

---

## What to protect

| Muscle | How it atrophies | How to keep it |
|---|---|---|
| Reading unfamiliar code | Never reading; only prompting | Review every diff; read one module a week |
| Debugging from first principles | "Just fix it" | Debug one incident per month with no agent |
| Design taste | Accepting the first plausible structure | Review the design *before* implementation |
| Naming | Letting the agent name things | Rename deliberately; names are design |
| Estimating | Never feeling the friction | Do a small task by hand occasionally |
| Writing | Never writing prose | Write the spec yourself, not just the prompt |

A practical rule that costs almost nothing: **read the full diff, every time.** Not skim — read. It is the single habit most correlated with staying competent.

The second: **keep one thing you build without the agent.** A tool, a library, a subsystem. Not as ideology — as calibration. It keeps your sense of what "hard" actually feels like.

---

## Measurement

The metrics that matter are the ones your organisation already cares about, measured honestly.

| Good metric | What it tells you | Watch out for |
|---|---|---|
| **Cycle time** (idea → merged) | Whether throughput actually improved | Gaming by merging smaller, less useful changes |
| **Review rework** (findings per PR) | Whether quality at generation improved | Reviewers adapting their standards |
| **Escaped defects** | Whether verification is working | Lag — appears weeks later |
| **Revert rate** | Whether changes are too large or too unverified | Teams that never revert because they patch forward |
| **Time to first feedback** | Whether the loop is fast | Optimising the metric instead of the loop |

| Vanity metric | Why it lies |
|---|---|
| Lines of code | Rewards volume, punishes deletion |
| Tokens spent | Measures input, not output |
| Prompts written | Measures effort, not effect |
| "AI-assisted %" | Measures adoption, not value |
| Self-reported speedup | Systematically optimistic — see below |

Track **two** numbers for a month: cycle time and review rework. That is enough to know whether any of this is working. More metrics usually means you are avoiding the question.

---

## The evidence is messier than the marketing

Worth knowing precisely, because it is the most misquoted study in the field.

**2025 — the randomised trial.** METR recruited 16 experienced open-source developers working on repositories they had contributed to for years (246 real tasks). Tasks were randomly assigned to AI-allowed or AI-disallowed. Result: with AI, tasks took **19% longer**. The developers believed the tools were helping.

**2026 — the follow-up.** METR ran a larger study from August 2025 with newer tools. Their estimate for the returning developers was a **speedup of about 18%** (confidence interval −38% to +9%); for newly recruited developers, about **4%** (CI −15% to +9%). But they concluded the data was **not a reliable signal**, because developers who benefit most now refuse to work without AI and therefore drop out of the study — which biases the estimate toward "no effect". They are redesigning the experiment.

What survives both results:

1. **Felt speed ≠ measured speed.** The 2025 developers were confidently wrong about their own productivity.
2. **Averages hide the distribution.** The effect depends on task type, codebase and person. You are not the mean.
3. **The measurement is getting harder**, not because AI is magic but because the counterfactual is disappearing.

The honest position: for many engineers on many tasks, current tools probably help. For some tasks they slow you down, and you will not feel it. The only defence is your own measurement.

---

## Goodhart's law applies immediately

Once a metric becomes a target, it stops measuring.

- Reward cycle time → people merge smaller, less valuable changes.
- Reward PR count → people split work artificially.
- Reward "AI usage" → people use AI for things it is bad at.

Choose metrics that are **hard to game without actually improving** — escaped defects and rework are better than output counts, because the only way to move them is to get better.

---

## What to be good at

If implementation gets cheaper, the scarce skills become:

1. **Decomposition** — cutting work into pieces with independent verification.
2. **Specification** — describing intent precisely enough to be checked.
3. **Verification design** — knowing what evidence would actually convince you.
4. **Systems thinking** — seeing the coupling the agent cannot see.
5. **Domain knowledge** — knowing what the business actually needs.
6. **Review and taste** — recognising "technically correct but wrong".
7. **Saying no** — to scope, to plausible-but-unnecessary code, to the demo.

Notice that all seven are old skills. The tools changed the price, not the list.

---

## Practice

Three audits, one page total:

1. **Ownership audit.** Pick the five largest changes you shipped in the last quarter. For each: can you explain it without the tool? Score 1–5. Anything below 4 is a debt payment due.
2. **Metric audit.** What do you currently use to decide whether this is working? If the answer is "it feels faster", pick two real metrics today and write down their current values.
3. **Skill audit.** Which of the seven skills above are you actually practising? Which have you outsourced entirely?

---

**Next:** [09 · Antipatterns](09-antipatterns.md) — the twelve ways this goes wrong, with fixes.
