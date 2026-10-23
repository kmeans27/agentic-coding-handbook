# Glossary

Tool-agnostic where possible. Where a term is a product feature, the mechanism is described instead of the brand.

---

**Agent** — A model in a loop with tools: it decides an action, executes it, observes the result, and repeats until it decides it is done. Contrast with a workflow, where the steps are fixed in code.

**Agentic coding** — Using agents to make changes in a codebase, as opposed to using a model to answer questions about one.

**AGENTS.md / CLAUDE.md** — A small file loaded at the start of every session, containing project rules, commands and gotchas. A cache, not a diary. Keep it short.

**Augmented coding** — Kent Beck's term for the disciplined middle ground: you care about the code, its complexity and its tests, you just do not type most of it. Contrast with vibe coding.

**Blast radius** — How much can go wrong if the change is wrong. The main variable to control when deciding whether to delegate.

**Checkpoint / rewind** — A snapshot of files and conversation taken before changes, allowing rollback. Convenient, but not a substitute for git — it typically only tracks edits made through the tool's own file operations.

**Cognitive debt** — Understanding you will have to rebuild later. Accumulates when you merge code you did not fully read or understand.

**Compaction** — Replacing part of the conversation with a summary when the context fills. Lossy: it tends to keep events and lose decisions.

**Context engineering** — Finding the smallest set of high-signal tokens that maximises the likelihood of the desired outcome.

**Context rot** — Gradual degradation of output quality as the context fills, well before the hard limit. Manifests as ignored instructions, repetition, vagueness and scope creep.

**Context window** — The total text the model can attend to in one session: system prompt, tools, files read, command output, and conversation.

**Eval** — A repeatable test of model behaviour, usually a set of cases with expected outcomes. The agent equivalent of a test suite; without one, "it got better" is an opinion.

**Fan-out** — Running the same transformation across many independent units, one fresh invocation per unit. Requires a pilot on a few units first.

**Guardrail** — A deterministic constraint on what the agent may do: sandbox, permission rule, hook, lint rule. Not a suggestion in a prompt.

**Hallucination** — Confidently stated output that is not grounded in fact or in the code. Not a special failure mode: it is the same generation process producing a wrong answer.

**Hook** — A script run automatically at a defined point in the agent's cycle (before a tool call, after an edit, when a turn ends). Deterministic, unlike instructions.

**Just-in-time retrieval** — Giving the agent a pointer and letting it fetch what it needs, instead of preloading everything that might be relevant.

**MCP (Model Context Protocol)** — A standard for exposing tools and data to agents. Useful for structured, stateful integrations; often overkill when a CLI already exists.

**Orchestrator** — A component that splits work across agents and combines results. Powerful for independent work, fragile for coupled work.

**Plan mode** — A mode where the agent may read and reason but not modify. Useful for forcing exploration before implementation. The concept matters more than the name.

**Prompt injection** — Instructions hidden in content the agent reads (a web page, an issue, a file) that redirect its behaviour. Defend with privilege separation and by treating fetched content as data.

**Reward hacking / test tampering** — Making the check pass instead of making the code work: deleting assertions, adding skips, regenerating snapshots. A predictable consequence of optimising for "green".

**Sandbox** — OS-level isolation of filesystem and network. The only reliable way to let an agent act freely without giving it your whole machine.

**Skill** — A packaged procedure: a description of when to use it, the steps, and often scripts or references. Loaded on demand rather than every session, which keeps context clean.

**Spec** — A written statement of intent: goal, affected files and interfaces, out of scope, and how the result will be verified. The unit of delegation.

**Subagent** — A separate agent with its own context window, invoked for a scoped task and returning a summary. Good for investigation and review; bad for the work you are about to edit.

**Tool use** — The model emitting a structured call that external code executes. The mechanism that turns a chat model into an agent.

**Verification loop** — The cycle of running a check, reading the result, and iterating. The single most important thing to establish before delegating.

**Vibe coding** — Building by describing outcomes and accepting generated code without reviewing it. Fine for throwaway work; not a professional practice for maintained systems.

**Worktree** — A second checkout of the same repository on a different branch. The cheapest way to isolate parallel agent sessions.

---

**Back to:** [README](../README.md)
