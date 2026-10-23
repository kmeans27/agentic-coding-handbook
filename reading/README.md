# The reading canon

Twenty-two sources. Annotated, time-boxed, and rated for how fast they will go stale.

**Every link was resolved on 2026-10-23.** Reading times are estimates at ~220 words per minute, rounded up — real times vary with how often you stop to think, which is the point.

---

## How to use this

Read in order of tier, not in order of publication. Tier 0 gives you the mental model; everything after it is detail.

| Rating | Meaning | Read it for |
|---|---|---|
| **Durable** | About mechanisms. Should hold for years. | Understanding |
| **Slow decay** | Tool-specific, patterns transfer. | Tactics |
| **Fast decay** | Version-pinned. | Ideas, not instructions |

The single most useful habit for this list: after each piece, write **one sentence** about what you would do differently. If you cannot, you did not read it — you scanned it.

---

## Tier 0 — the mental model (~1 h 30)

If you read nothing else, read these six.

| Source | Time | Durability | The idea worth taking |
|---|---|---|---|
| **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** · Anthropic, Dec 2024 | 20 min | **Durable** | Most "agents" should be workflows. Start with the simplest pattern that works; add autonomy only when it earns its cost. Agent = LLM using tools in a loop, and that loop is the last resort, not the first. |
| **[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** · Anthropic, Sep 2025 | 18 min | **Durable** | The goal is the *smallest set of high-signal tokens*, not the most complete prompt. Covers compaction, structured notes, sub-agents and just-in-time retrieval. |
| **[Agentic Coding Recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)** · Armin Ronacher, Jun 2025 | 13 min | **Durable** | The environment is the product: fast tools, boring languages, simple code, visible logs, parallelisable state. Explicitly written to age well. |
| **[Don't Build Multi-Agent Systems](https://cognition.ai/blog/dont-build-multi-agents)** · Cognition, Jun 2025 | 11 min | **Durable** | Two principles: *share full context*, and *actions carry implicit decisions*. Splitting a coupled task across agents creates incoherence that no orchestrator can reconcile. |
| **[Vibe Engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/)** · Simon Willison, Oct 2025 | 10 min | **Durable** | Names the professional version of vibe coding: you still own tests, review, security and correctness. The tool changed; the accountability did not. |
| **[Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)** · Kent Beck, Jun 2025 | 14 min | **Durable** | TDD as the control loop for an agent, plus the two failure signals to watch for: loops, and unrequested functionality. His actual system prompt is included. |

> **The one-hour version:** Building Effective Agents → Context Engineering → Armin. Skip the rest until you have used the ideas on real work.

---

## Tier 1 — operating depth (~1 h 50)

| Source | Time | Durability | The idea worth taking |
|---|---|---|---|
| **[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)** · Anthropic, living document | 40 min (skim 15) | **Slow decay** | The most complete public description of the *patterns*: give it a check it can run, explore before planning, keep the rules file short, clear after two corrections. Tool-specific examples, transferable mechanisms. |
| **[Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** · Anthropic, Sep 2025 | 15 min | **Durable** | Tool design is interface design: consolidate, namespace, return only what is needed, and write errors for a caller that cannot ask questions. |
| **[12-Factor Agents](https://github.com/humanlayer/12-factor-agents)** · HumanLayer | 45 min | **Slow decay** | The engineering checklist for production agents: own your prompts, own your context window, own your control flow, compact errors, small focused agents, stateless reducer. Unglamorous and useful. |
| **[How Anthropic Teams Use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code)** · Anthropic, Jul 2025 | 11 min | **Slow decay** | Team-level adoption patterns: onboarding to unfamiliar code, prototyping, documentation, and where people deliberately keep a human in the loop. |

---

## Tier 2 — hands-on (a weekend, or a fortnight of evenings)

These are systems you install and use, not essays. Read the README, then run it on a real task.

| Source | Time | Durability | What it is |
|---|---|---|---|
| **[Master Claude Code in a Weekend](https://github.com/luongnv89/claude-howto)** | **11–13 h** | **Fast decay** | The most structured free course available: 10 modules from slash commands to hooks, MCP, subagents and plugins, with a learning path and self-assessment. Genuinely good pedagogy. Ignore the version numbers; keep the concepts. |
| **[Superpowers](https://github.com/obra/superpowers)** · Jesse Vincent | 10 min, then live in it | **Slow decay** | A complete methodology expressed as composable skills: brainstorm → worktree → write plan → execute in small tasks → TDD → review → finish branch. The clearest public example of encoding process as skills. |
| **[Agent Skills](https://github.com/addyosmani/agent-skills)** · Addy Osmani | 13 min | **Slow decay** | Production-grade skills mapped to the lifecycle (`/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`). Best example of turning senior-engineer quality gates into something an agent follows. |
| **[Skills for Real Engineers](https://github.com/mattpocock/skills)** · Matt Pocock | 7 min | **Slow decay** | Deliberately anti-framework. Home of `/grill-me`, which interrogates your plan before implementation. Useful counterweight to process-heavy methodologies. |
| **[drill-me (plan stress-test)](https://github.com/rvanbaalen/skills/tree/main/plugins/drill-me)** · rvanbaalen | 5 min | **Slow decay** | The skill you asked about. Walks the design tree one branch at a time, asks one opinionated question per turn with a recommended answer, and reads the codebase instead of asking things it could find. |
| **[drill-me (tutor)](https://github.com/timini/drill-me)** · timini | 6 min | **Slow decay** | Same name, different tool: quizzes *you* on a codebase, paper or topic, with spaced repetition and a memory of what you got wrong. Good for ramping up on unfamiliar systems. |
| **[spec-kit](https://github.com/github/spec-kit)** · GitHub | 8 min | **Fast decay** | Spec-driven development with a formal toolchain. Useful even if you reject the ceremony — it shows what a specification needs to contain to be executable. |
| **[ECC](https://github.com/affaan-m/ECC)** · affaan-m | 60 min (optional) | **Fast decay** | A maximalist harness: skills, memory, instincts, security, research workflows. Steal ideas; do not adopt wholesale. This is the kind of config that changes weekly. |

> **Warning on Tier 2.** These repos are tool-specific and move fast. Read them for *structure* — how a spec is shaped, how a review is scoped, where a human gate sits. Copying their config verbatim will be stale within a release cycle, and you will not understand why it stopped working.

---

## Tier 3 — reality check (~1 h 20)

Read these *after* you are excited, not before. They are the antidote.

| Source | Time | Durability | Why it matters |
|---|---|---|---|
| **[Measuring the Impact of Early-2025 AI on Experienced OSS Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)** · METR, Jul 2025 | 20 min | **Durable as a method** | Randomised controlled trial, 16 experienced developers, 246 real tasks: AI made them **19% slower**, while they believed it helped. The number is dated; the lesson about felt vs measured speed is not. |
| **[We are Changing our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/)** · METR, Feb 2026 | 11 min | **Durable as a method** | The follow-up: returning developers now show roughly an 18% speedup (CI −38% to +9%), new developers ~4% — but METR judges the data unreliable because the heaviest AI users now drop out of the study. A masterclass in selection effects. |
| **[Exploring Gen AI](https://martinfowler.com/articles/exploring-gen-ai.html)** · Birgitta Böckeler / Martin Fowler | 8 min (index) | **Slow decay** | The most careful public thinking on coding assistants as *engineering* rather than magic. The index is the entry point; the individual essays are where the value is. |
| **[Andrej Karpathy — Software Is Changing (Again)](https://www.youtube.com/watch?v=LCEmiRjPEtQ)** · 2025 | 40 min video | **Slow decay** | "Software 3.0", partial autonomy, and why keeping a human on the loop is a design choice rather than a limitation. Good framing for the next five years. |

---

## Budget

| Path | Time | What you get |
|---|---|---|
| One hour | 60 min | Tier 0, first three |
| Core canon | ~4 h | Tiers 0, 1, 3 (minus the video) |
| Weekend | ~6–8 h | Core + two Tier 2 repos, used on a real task |
| Full course | ~18 h | Everything, including the 11–13 h walkthrough |

---

## What is deliberately excluded

This list is curated by subtraction, which is most of its value.

| Excluded | Why |
|---|---|
| Model leaderboards and benchmark tables | Stale in weeks; tell you nothing about your codebase |
| "N prompts that 10× your output" | Prompt alchemy. The environment dominates the wording |
| Vendor feature tours | Marketing with a changelog; read the docs when you need the feature |
| Productivity-thought-leadership threads | Confident, unfalsifiable, and usually selling something |
| Framework comparisons | The framework is not the variable. Your loop is |
| Anything without a named author | If nobody will stand behind it, you cannot check it |

One more exclusion worth stating: **this repository does not tell you which model to use.** That decision changes monthly and is the least interesting variable in the system.

---

## Verification log

| Date | What was checked | Result |
|---|---|---|
| 2026-10-23 | All 22 links resolve (HTTP 200) | Pass |
| 2026-10-23 | METR figures quoted from the primary posts, including the Feb 2026 correction | Pass |
| 2026-10-23 | Anthropic post dates read from page metadata | Pass |
| 2026-10-23 | Repository descriptions read from the GitHub API | Pass |

If a link rots, the fix is a pull request with a replacement and a date — not a silent deletion.

---

**Back to:** [README](../README.md) · **Next:** [14-day plan](../study/two-week-plan.md)
