# Sources and claims ledger

## Attribution

This repository is a synthesis. The ideas belong to the people below; the structure, the mistakes in interpretation, and any errors are the repository's alone.

Nothing here is affiliated with or endorsed by Anthropic, Cognition, METR, or any author cited. Where a source is quoted, it is marked; everything else is paraphrase.

---

## The sources

| # | Author / org | Source | Used for |
|---|---|---|---|
| 1 | Anthropic | [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) (Dec 2024) | Workflows vs agents; simplicity as a design goal |
| 2 | Anthropic | [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Sep 2025) | Context as a budget; compaction; sub-agents; JIT retrieval |
| 3 | Anthropic | [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) (Sep 2025) | Tool interface design; error design |
| 4 | Anthropic | [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) (living) | The loop; verification; rules-file hygiene; failure modes |
| 5 | Anthropic | [How Anthropic Teams Use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code) (Jul 2025) | Team-level adoption patterns |
| 6 | Armin Ronacher | [Agentic Coding Recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/) (Jun 2025) | Environment design; speed; stable ecosystems; simple code |
| 7 | Walden Yan / Cognition | [Don't Build Multi-Agent Systems](https://cognition.ai/blog/dont-build-multi-agents) (Jun 2025) | Context sharing; implicit decisions; coupling |
| 8 | Simon Willison | [Vibe Engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/) (Oct 2025) | Professional accountability in AI-assisted work |
| 9 | Kent Beck | [Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes) (Jun 2025) | TDD as a control loop; failure signals; Tidy First |
| 10 | Dex Horthy / HumanLayer | [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) | Production agent engineering checklist |
| 11 | Jesse Vincent | [Superpowers](https://github.com/obra/superpowers) | Workflow as composable skills; small tasks; review gates |
| 12 | Addy Osmani | [Agent Skills](https://github.com/addyosmani/agent-skills) | Lifecycle-shaped skills; quality gates |
| 13 | Matt Pocock | [Skills for Real Engineers](https://github.com/mattpocock/skills) | Anti-framework stance; plan interrogation |
| 14 | rvanbaalen | [drill-me](https://github.com/rvanbaalen/skills/tree/main/plugins/drill-me) | Pre-implementation plan stress-testing |
| 15 | timini | [drill-me (tutor)](https://github.com/timini/drill-me) | Spaced repetition for codebase learning |
| 16 | Luong Nguyen | [Master Claude Code in a Weekend](https://github.com/luongnv89/claude-howto) | Structured feature curriculum |
| 17 | GitHub | [spec-kit](https://github.com/github/spec-kit) | Spec-driven development formalised |
| 18 | affaan-m | [ECC](https://github.com/affaan-m/ECC) | Harness-level memory, skills and security |
| 19 | METR | [Early-2025 developer productivity RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (Jul 2025) | The 19% slowdown result |
| 20 | METR | [Changing our experiment design](https://metr.org/blog/2026-02-24-uplift-update/) (Feb 2026) | The 2026 revision and selection effects |
| 21 | Birgitta Böckeler / Martin Fowler | [Exploring Gen AI](https://martinfowler.com/articles/exploring-gen-ai.html) | Careful engineering framing; adoption risk |
| 22 | Andrej Karpathy | [Software Is Changing (Again)](https://www.youtube.com/watch?v=LCEmiRjPEtQ) (2025) | Partial autonomy; Software 3.0 framing |

---

## Claims ledger

Not every claim in this repository has the same evidential weight, and pretending otherwise is how the field got into its current mess. This is an honest accounting.

**High** — direct evidence or primary documentation.
**Medium** — a plausible mechanism plus consistent practitioner reports, but no controlled measurement.
**Low** — one practitioner's experience, or an argument that has not been tested.

| Claim | Confidence | Basis |
|---|---|---|
| Context quality degrades as the window fills | **High** | Primary documentation (2) plus broad practitioner consensus |
| An agent stops when output looks done unless given a check | **High** | Primary documentation (4); consistent reports |
| AI made experienced devs 19% slower in early 2025 | **High** | Randomised controlled trial, n=16, 246 tasks (19) |
| AI is probably faster in 2026, but the measurement is currently unreliable | **Medium** | Follow-up with wide confidence intervals and acknowledged selection bias (20) |
| Self-reported speedup is systematically optimistic | **High** | Directly observed in (19) |
| A fresh-context reviewer catches more than the author | **Medium** | Strong mechanism (independence of judgement) and consistent practice; little controlled study |
| Multi-agent decomposition fails on tightly coupled work | **Medium** | Mechanism argument plus vendor field report (7); no independent benchmark |
| Simpler code is easier for agents to change safely | **Medium** | Broad practitioner consensus (6), no controlled measurement |
| Go is a better language for agentic work than Python | **Low** | One experienced practitioner's evaluation (6). Plausible mechanism (test caching, stability), not generalisable |
| Faster test suites increase agent throughput | **Medium** | Mechanism is uncontroversial (more iterations per hour); magnitude is project-specific |
| Hooks are more reliable than instructions | **High** | Deterministic vs advisory is a structural property, not an empirical claim |
| Agents will tamper with tests to reach green | **Medium** | Widely reported; a predictable consequence of the objective given |
| A longer rules file is followed less | **Medium** | Consistent practitioner reports and documentation (4); no controlled study |
| Cognitive debt harms long-term performance | **Medium** | Strong reasoning and analogy to technical debt; longitudinal evidence is thin |
| "10× productivity" | **Low / rejected** | Not supported by any rigorous measurement. The 2025 RCT found the opposite sign; 2026 estimates are positive but wide and self-selected |

### Where this repository is most likely to be wrong

Being explicit about this is more useful than being confident.

1. **The orchestration chapter.** Multi-agent practice is changing fast. The mechanism argument (shared context) is durable; the specific tactics may not be.
2. **The productivity numbers.** Any figure here will be superseded. The method lesson will not.
3. **The "prefer boring technology" advice.** It is well-argued but not measured, and it may be less true as models improve at unfamiliar code.
4. **Tool-specific guidance.** Where a chapter implies a feature (plan mode, hooks, skills), the mechanism is the point. The feature name will move.

---

## Corrections

If something here is wrong:

1. Open an issue with the claim, the source, and the date.
2. If the source has changed, note what it said before and after.
3. Fix the claim, not just the link.

A handbook that cannot be corrected is a doctrine. This one should not be.

---

**Back to:** [README](README.md)
