# 06 · Code design

> **Principles 8 and 13** — Design for legibility. Prefer boring, stable technology.

---

## The codebase is part of the prompt

An agent does not experience your architecture as a diagram. It experiences it as a sequence of file reads, grep results and error messages. Everything that makes that sequence noisy — indirection, magic, inconsistency — is a tax paid on every single task.

The useful reframe:

> **Every agent session is an implicit readability review of your codebase.**

If the agent keeps getting lost, the codebase is lost. Fixing it helps humans too, which is why this advice survived from before agents existed.

---

## What "agent-legible" means

| Property | Why the agent cares | What it looks like |
|---|---|---|
| **Local** | It reads one file, not eight | Permission check in the handler, not the middleware config |
| **Explicit** | Nothing is inferred from convention | `validateOrder(order)` not `__call__` magic |
| **Consistent** | One pattern to copy, not five | Every endpoint shaped the same way |
| **Boring** | Predictable idioms, stable docs | `if`/`else` over metaprogramming |
| **Named for search** | `grep` is its main navigation tool | `calculateShippingCost` not `calc` |
| **Small** | Fits in a window with room to spare | 200-line files over 2,000 |

A useful test: *if I only had grep and file reads, could I find every place that handles refunds in under a minute?* If not, the agent cannot either.

---

## Prefer functions to hierarchies

The practical guidance, mostly from Armin Ronacher's field notes:

- **Long, descriptive function names** over clever abstractions.
- **Avoid inheritance**; prefer composition and plain data.
- **Avoid metaprogramming** — decorators that rewrite signatures, ORMs that generate SQL you cannot see, frameworks that own control flow.
- **Plain SQL** over ORM gymnastics. Agents write excellent SQL, and they can match it against the SQL in your logs. An ORM hides both.
- **The dumbest thing that works** is usually the most maintainable thing an agent will produce.

None of this is new advice. It is what "simple code" always meant. Agents just make the cost visible and immediate.

---

## Keep invariants where they can be seen

This is the highest-stakes version of locality.

If authorisation is enforced by a decorator defined three files away, an agent adding a new route will plausibly forget it — not because it is careless, but because the rule was not visible at the point of change.

Rules that must never be missed should be:

1. **At the call site**, or
2. **Enforced by the type system**, or
3. **Enforced by a test that enumerates all routes**.

A config file listing protected paths is the worst option: it is invisible at the point of change and it silently drifts.

> [!WARNING]
> Any invariant enforced "somewhere else" is an invariant the next agent will break. Move it local, or make it structural.

---

## Stability beats novelty

Agents are trained on the world's code, and the world's code is mostly old. The further you move from well-trodden idioms, the more the model is guessing.

| Prefer | Avoid |
|---|---|
| Mature, slow-moving ecosystems | Frameworks with breaking changes every quarter |
| Backwards-compatible runtimes | Bleeding-edge language features |
| A small number of dependencies | A dependency for every utility |
| Explicit version pinning | Floating ranges |
| Boring, documented patterns | Clever patterns from a blog post |

The dependency point deserves emphasis. **Write the 30 lines yourself.** A dependency is not just a supply-chain risk; it is a second source of truth about how something works, and the agent has to reconcile both. Every dependency you remove is context you get back.

---

## Be more conservative about upgrades, not less

This is counter-intuitive, because agents make upgrades *cheap*. That is exactly the trap.

When an agent leaves a comment explaining why it chose an approach, that comment is a breadcrumb. If you then upgrade the library and the reason no longer holds, the comment becomes a lie that the next session will trust. Do this a few times and your codebase is full of confident, outdated reasoning — the worst possible input.

Practical rules:

- Upgrade deliberately, in its own commit, with the changelog read.
- When behaviour changes, update or delete the comments that justified the old behaviour.
- Do not let an agent "modernise" code as a side effect of an unrelated task.
- Treat generated migration guides with suspicion; they are written for the average codebase, not yours.

---

## Refactor at the threshold, not on a schedule

Agents work well up to a complexity ceiling, then fall off a cliff. The ceiling is not lines of code — it is **the total amount of stuff that has to be considered at once** to make a safe change.

Signals you are near it:

- The agent starts making changes in files you did not mention.
- It re-implements something that already exists.
- You have to explain the same architectural rule in every session.
- Reviews get longer while diffs stay the same size.

The fix is not a bigger context window. It is extraction: a component library, a shared helper, a narrower interface. Do it slightly **before** it hurts — after the pain is obvious, the refactor is much larger.

Too early is waste. Too late is a rewrite. This is a judgement call, and it is one of the reasons the job is still a job.

---

## Tests are instructions

For an agent, a test is the most reliable description of intended behaviour that exists. More reliable than a doc, because it fails when it is wrong.

That has design consequences:

- **Test names should read as requirements.** `rejects_expired_token` is a spec line.
- **Test failures should be informative.** A failure message that says "expected true, got false" teaches nothing.
- **Fixtures should be obvious.** A magic fixture that injects five things violates locality as badly as production code does.
- **One behaviour per test.** A test asserting six things cannot tell the agent which one broke.

---

## Anti-patterns that specifically hurt agents

| Pattern | Why it hurts |
|---|---|
| Base class with 12 optional hooks | The agent must read all subclasses to know what runs |
| Dynamic dispatch by string | `grep` finds the string, not the behaviour |
| Implicit global state | Tests pass individually, fail together; agent cannot see why |
| Generated code checked in without a header | Agent edits the generated file, changes vanish |
| Deep directory symmetry for its own sake | Navigation cost with no information |
| "Utils" modules | Where meaning goes to die |

---

## Practice

Pick the module you have touched most in the last month and run this audit from memory:

1. Can you find every entry point with `grep` alone? Write down the query you would use.
2. Name one invariant that lives away from where it is needed. Move it (or plan to).
3. Name one dependency you could delete in under an hour.
4. Name one place where two patterns coexist. Which one is correct? How would an agent know?

---

**Next:** [07 · Orchestration](07-orchestration.md) — running more than one thing at once without creating a mess.
