# Prompt patterns

Ten templates, chosen because they survive model changes. None of them rely on magic phrasing, role-play, or "think step by step". They work because they change the **information** and the **check**, not the tone.

Adapt the wording. Keep the structure.

---

## 1 · The interview (turning fuzzy intent into a spec)

**When:** the requirement is clear in your head but not in words. Larger features.

```text
I want to build <one line>.

Interview me in detail before writing any code. Ask about technical
approach, edge cases, failure modes, UI/UX, and tradeoffs. Do not ask
questions you could answer by reading the codebase — read it instead.

One question at a time. For each, give me your recommended answer and
why. Keep going until the decisions are resolved, then write the full
spec to SPEC.md with: goal, files and interfaces, out of scope, and
how we will verify it.
```

**Why it works:** it converts your implicit knowledge into an artefact, and it surfaces the questions you did not think to ask. Start the implementation in a **new session** afterwards.

---

## 2 · The failing test first (bug fix)

**When:** anything is broken and you can describe the symptom.

```text
Bug: <what the user sees>.
Reproduce it with a failing test in <test file>. Do not fix anything yet.
Run it. Show me the failure output.

Only then implement the smallest fix. Run the test again and show the
passing output. Then run the full suite.
```

**Why it works:** it forces reproduction before explanation, and gives you two pieces of evidence — the red and the green. It also prevents "fixing" the symptom in a way that never addressed the cause.

---

## 3 · The behaviour-preserving refactor

**When:** structure is bad, behaviour is fine.

```text
Refactor <target> without changing behaviour.

Constraints:
- No new dependencies.
- Do not change public interfaces or output.
- One commit, structural only.

Before: run the full suite and record the result.
After: run it again and show both summaries.
If any test changes, stop and explain why before continuing.
```

**Why it works:** "without changing behaviour" is only meaningful if there is a check that can detect the change. The before/after evidence is the whole pattern.

---

## 4 · The fan-out migration

**When:** the same mechanical change across dozens or hundreds of files.

```text
Step 1 — list the files that need <change>. Write them to files.txt.
Step 2 — show me the exact transformation for three of them as a diff.
        Wait for my approval.
Step 3 — <after approval> apply the same transformation to each file in
        files.txt using the script below, one invocation per file.
```

```bash
for f in $(cat files.txt); do
  agent -p "Apply <transformation> to $f. Change nothing else.
            Return OK or FAIL with a one-line reason." \
        --allowedTools "Edit" --permission-mode dontAsk
done
```

**Why it works:** the pilot of three is where the prompt gets fixed. Skipping it is how you get 200 confident, wrong diffs. Verify the aggregate afterwards — full suite plus a sampled diff review.

---

## 5 · The adversarial review

**When:** before merging anything non-trivial.

```text
You are reviewing a change you did not write. The plan is in PLAN.md;
the diff is in the working tree.

Try to refute it. Report only gaps that affect correctness or a stated
requirement. For each: file, line, what breaks, how to reproduce.

Do not report style, naming, or speculative future needs. If you find
nothing that affects correctness, say so plainly.
```

**Why it works:** "try to refute" is a different task from "review". The explicit exclusion list prevents the over-engineering spiral.

---

## 6 · The onboarding read

**When:** you are new to a codebase, or returning after a break.

```text
I am new to this repository. Do not modify anything.

Answer, with file references:
1. How does a request flow from entry point to database?
2. Where are the three most important invariants enforced?
3. What is the pattern I should copy to add a new <thing>?
4. What is the most surprising or fragile part of this code?
5. What would you read first if you had one hour?
```

**Why it works:** it produces a map you can verify, rather than a summary you have to trust. Question 4 is the one that surfaces the real risk.

---

## 7 · The visual match

**When:** the target is a design, not a description.

```text
[paste target screenshot or reference path]

Implement this. Then:
1. Screenshot the result at the same viewport.
2. List every visible difference from the target — spacing, colour,
   typography, alignment, states.
3. Fix them and screenshot again.
```

**Why it works:** "make it look better" has no stopping condition. A diff against a reference does.

---

## 8 · The legacy test net

**When:** untested code you need to change safely.

```text
Do not change src/legacy/*.py yet.

Write characterisation tests that capture current behaviour, including
the odd parts. Run them against the current code — they should pass
without modification.

List any behaviour you could not pin down, and any place where the
current behaviour looks like a bug. Do not fix those. Just report them.
```

**Why it works:** it builds the safety net before the change, and it separates "this is weird" from "this is wrong" — a distinction that matters when you do not yet know the domain.

---

## 9 · The production investigation

**When:** symptom in production, cause unknown.

```text
Symptom: <what users see>. Started: <when>. Scope: <who/what>.
Here is the evidence: <logs, metrics, trace, error>.

Do not change code yet. Produce:
1. Three hypotheses, ranked, each with the evidence for and against.
2. The cheapest observation that would distinguish between them.
3. What you would check first if you could only check one thing.
```

**Why it works:** it separates hypothesis generation from action. Debugging fails when the agent starts editing before it understands — and it keeps your context clean of speculative patches.

---

## 10 · The second opinion

**When:** you have made a design decision and want a challenge, not agreement.

```text
Here is my decision and my reasoning: <paste>.

Argue the strongest case against it. Assume I am wrong and find the
failure mode I have not considered. If, after arguing, you still think
the decision is sound, say which part of my reasoning is load-bearing.
```

**Why it works:** models are agreeable by default. Asking for the counter-case is the cheapest way to get a real critique — and the "load-bearing" clause stops it from inventing objections.

---

## The anti-patterns of prompting

| Avoid | Because |
|---|---|
| "Think step by step" | Modern models do this internally; it adds nothing and can hurt |
| Role-play ("you are a 10x engineer") | Adds tokens, not information |
| Threats and bribes | No reliable effect; wastes context |
| Giant context dumps | Buries the signal (see [chapter 03](../docs/03-context.md)) |
| Asking "are you sure?" | Invites a confident yes. Ask for a command output instead |
| Six tasks in one message | Guarantees at least one is done badly |

---

**Back to:** [README](../README.md) · [Checklists](checklists.md)
