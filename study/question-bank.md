# Question bank

Forty questions. Cover the answer, say it out loud, then open it.

Designed for **spaced repetition**: attempt all forty on day 1, then again on days 3, 7, 14 and 30. Mark the ones you get wrong and re-test only those. Ten minutes per pass.

If an answer surprises you, the chapter link is the fix.

---

## A · Mental model and economics

<details>
<summary><b>1. Why is "which agent is best?" the wrong question?</b></summary>

Because the model is the least durable variable in the system. Your specification quality, verification design and repository structure determine the outcome, and those survive every model upgrade.
</details>

<details>
<summary><b>2. What does an agent lack that a junior engineer has?</b></summary>

Memory between sessions, context about your codebase, visibility of what you can see, and — most importantly — calibrated uncertainty. It is equally confident when right and when wrong.
</details>

<details>
<summary><b>3. Why can't you use fluency as a signal of correctness?</b></summary>

Because generation quality and factual correctness are produced by the same process. Polished prose and plausible code are equally likely to be wrong, and the model has no mechanism to signal doubt reliably.
</details>

<details>
<summary><b>4. What does Amdahl's law predict about agent adoption?</b></summary>

That speeding up generation buys nothing if generation was not the bottleneck. If tests take 20 minutes or review is the constraint, faster code production makes the queue longer, not shorter.
</details>

<details>
<summary><b>5. When is delegation a bad trade?</b></summary>

When the task is small (specifying costs more than writing), when the design is the deliverable (you cannot specify what you have not thought through), or when verification cost approaches implementation cost (you added a translation layer, not leverage).
</details>

<details>
<summary><b>6. Why did the 2025 METR study matter, and what changed in 2026?</b></summary>

2025: a randomised trial found experienced developers were 19% slower with AI while believing it helped — direct evidence that felt speed is unreliable. 2026: the follow-up suggested a speedup (~18% for returning developers) but METR judged the data unreliable, because the heaviest AI users now refuse to participate without AI, biasing the estimate. The method lesson survives; the number does not.
</details>

---

## B · Context

<details>
<summary><b>7. Define context engineering in one sentence.</b></summary>

The smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome.
</details>

<details>
<summary><b>8. What are the first symptoms of context degradation?</b></summary>

It stops following an early instruction, re-suggests a rejected approach, becomes vague where it was specific, then starts touching files you did not mention. By the time you notice the last one, quality has been falling for a while.
</details>

<details>
<summary><b>9. Why does the two-correction rule exist?</b></summary>

Because failed attempts remain in the window and bias subsequent attempts. After two failures you are optimising against ghosts. A clean session with a sharper prompt beats a long session full of scar tissue.
</details>

<details>
<summary><b>10. What does compaction tend to lose?</b></summary>

Decisions and their reasons. It preserves what happened and drops why. Always name what must survive — modified files, interfaces, rejected approaches, the test command.
</details>

<details>
<summary><b>11. Why is a longer rules file followed less?</b></summary>

Because it is loaded every session and dilutes attention. Important instructions get lost among things the model can already infer. If a rule keeps being ignored, shorten the file before strengthening the rule.
</details>

<details>
<summary><b>12. What is the difference between pushing and pulling context?</b></summary>

Pushing preloads material you think is relevant; most of it is not, and it buries the part that is. Pulling gives a precise pointer ("the pattern is in `HotDogWidget.tsx`") and lets the agent fetch only what it needs. Pointers beat payloads.
</details>

---

## C · Specification and the loop

<details>
<summary><b>13. What are the two kinds of failure in the loop, and why distinguish them?</b></summary>

Execution errors (plan right, code wrong) and specification errors (plan wrong). They need different fixes: retry versus rewrite the spec. Confusing them produces the correction spiral — retrying code against a broken plan.
</details>

<details>
<summary><b>14. What four things does a usable spec contain?</b></summary>

Goal, files and interfaces, out of scope, and verification. The last two are the most often omitted and prevent the most damage.
</details>

<details>
<summary><b>15. When should you skip planning?</b></summary>

When you could describe the diff in one sentence. Typo fixes, log lines, renames, single-file changes following an obvious pattern.
</details>

<details>
<summary><b>16. Why must structural and behavioural changes be separate commits?</b></summary>

Because a diff that both moves code and changes behaviour cannot be reviewed — human or machine — for correctness. Separation makes each change verifiable and revertible independently.
</details>

<details>
<summary><b>17. What artefact does the Explore stage produce?</b></summary>

A short list of the files involved and the existing pattern to copy. Its exit condition is that you could now describe the change in a sentence.
</details>

<details>
<summary><b>18. If an agent fails twice in the same place, what do you do?</b></summary>

Stop. Treat it as a specification error. Clear the session and rewrite the plan with what you learned. Retrying the code cannot fix a wrong plan.
</details>

---

## D · Verification

<details>
<summary><b>19. What is the difference between a claim and evidence?</b></summary>

A claim costs the model nothing ("done"). Evidence costs it something — a command transcript, a test summary, a screenshot. Ask for artefacts, not assurance.
</details>

<details>
<summary><b>20. Why is "it compiles" near the bottom of the ladder?</b></summary>

Because it tells you almost nothing about behaviour. It confirms syntax and types, not that the logic does what was asked.
</details>

<details>
<summary><b>21. Why does a fresh-context reviewer catch more?</b></summary>

It sees only the diff and the criteria, not the reasoning that produced them. It evaluates the artefact rather than the story, and does not inherit the writer's assumptions.
</details>

<details>
<summary><b>22. What is the over-engineering trap in review?</b></summary>

A reviewer asked to find problems will always find some, and chasing all of them produces defensive code, speculative abstractions and tests for impossible cases. Restrict findings to correctness and stated requirements.
</details>

<details>
<summary><b>23. Name three ways an agent can tamper with tests.</b></summary>

Deleting or commenting out a failing test; adding `skip`/`xfail`/broad exception handling; weakening an assertion or regenerating a snapshot to match wrong output.
</details>

<details>
<summary><b>24. When should you refuse to delegate?</b></summary>

When you cannot verify the result, or when verification would cost as much as implementation. Then reduce the blast radius until it is checkable, build the check first, or do it yourself.
</details>

<details>
<summary><b>25. What is the strongest practical verification for a UI change?</b></summary>

Screenshot the result and diff it against the target, listing the differences explicitly. Visual comparison catches what no unit test will; it is noisy for logic and excellent for layout and state.
</details>

---

## E · Environment and code design

<details>
<summary><b>26. Why is test speed a property of the codebase, not a convenience?</b></summary>

Because iterations per hour — not tokens per second — determine agent throughput. A 60-second inner loop gives roughly 60 attempts an hour; a 10-minute loop gives six.
</details>

<details>
<summary><b>27. Why should a dev server refuse to start twice?</b></summary>

Because agents cannot tell whether it is already running. They will start a second instance, bind the same port, and then debug a phantom. A pidfile is a five-minute fix that removes the whole class.
</details>

<details>
<summary><b>28. Why log emails, OTPs and webhooks in development?</b></summary>

So the agent can complete an entire user journey unattended. If a human must click a link for the loop to close, the loop cannot run without you.
</details>

<details>
<summary><b>29. When is a hook better than an instruction?</b></summary>

Whenever the rule must hold every time. Instructions are advisory; hooks, lint rules, types and CI are deterministic. Convert important prose rules into gates.
</details>

<details>
<summary><b>30. Why prefer a CLI to an MCP server?</b></summary>

Fewer moving parts, lower token cost (no tool definitions loaded every session), easier to debug, and composable in scripts. Use MCP when there is no CLI, or when you need a structured stateful integration.
</details>

<details>
<summary><b>31. Why is dependency churn more dangerous with agents?</b></summary>

Because upgrades are cheap, so they happen opportunistically — and they invalidate the comments that explained previous decisions. The codebase fills with confident, outdated reasoning that the next session trusts.
</details>

---

## F · Orchestration

<details>
<summary><b>32. What is the difference between parallelism and independence?</b></summary>

Parallelism is a throughput problem solved by isolating state. Independence is a judgement problem solved by isolating context. The first needs worktrees; the second needs a fresh reviewer.
</details>

<details>
<summary><b>33. What state must be isolated for parallel agents?</b></summary>

Files and git (worktrees), databases (per-worker), ports (dynamic), caches (per-worktree), and external credentials or rate limits. The filesystem is the easy one; the others cause the subtle failures.
</details>

<details>
<summary><b>34. Why do multi-agent decompositions fail on coupled work?</b></summary>

Because subtasks share context and actions carry implicit decisions. Each agent makes hundreds of small choices the others cannot see, producing individually reasonable but jointly incoherent results.
</details>

<details>
<summary><b>35. When is fan-out appropriate?</b></summary>

When each unit has independent verification: migrations, mechanical refactors, test generation, isolated research. Pilot on three units, fix the prompt, then loop — and verify the aggregate afterwards.
</details>

---

## G · Judgment and measurement

<details>
<summary><b>36. What is cognitive debt?</b></summary>

Understanding you will have to rebuild later. It accumulates when you merge diffs you did not fully read and can no longer explain why the code is shaped the way it is.
</details>

<details>
<summary><b>37. What is the ownership test?</b></summary>

Open a file you changed last month and explain what it does, why it is shaped that way, and what breaks if you change it — without the agent open.
</details>

<details>
<summary><b>38. Name two metrics that resist gaming.</b></summary>

Escaped defects and review rework. Both can only be improved by actually getting better, unlike output counts, which are improved by producing more output.
</details>

<details>
<summary><b>39. Why is self-reported speedup unreliable?</b></summary>

Because the 2025 METR participants reported being faster while measurably being 19% slower. The feeling of flow is driven by reduced friction, not reduced total time.
</details>

<details>
<summary><b>40. Why does Goodhart's law apply immediately here?</b></summary>

Because agentic work generates so much measurable activity — tokens, prompts, commits, PRs — that the temptation to optimise the measurement instead of the outcome is constant. Choose metrics that are hard to move without real improvement.
</details>

---

**Back to:** [README](../README.md) · [14-day plan](two-week-plan.md) · [Checklists](../appendix/checklists.md)
