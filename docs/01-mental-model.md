# 01 · The mental model

> **Principle 1** — Specification and verification are the bottleneck now, not typing.

---

## The question people ask is wrong

The usual question is *"which agent is best?"* or *"what's the prompt for this?"*

Those are the wrong level of abstraction. They are questions about a vendor and a sentence. The engineers who get a large, durable advantage out of these tools are not winning on prompts. They are winning because they **specify better, verify better, and structure their codebase so that being wrong is cheap.**

A model upgrade will erase your prompt advantage in a weekend. It will not erase your ability to describe what you want or to prove that you got it.

---

## What actually changed

| | Before | Now |
|---|---|---|
| Constraint | Typing speed, recall of APIs, willingness to do tedious work | Clarity of intent, quality of verification, tolerance for review |
| Failure mode | You wrote the bug | You approved the bug |
| Unit of work | A function, a file | A task with an acceptance check |
| Main skill | Implementation | Decomposition and judgment |
| Main risk | Not knowing how | Not knowing what you shipped |
| Effort curve | Costly to start, steep to improve | Cheap to start, expensive to trust |

The last row is the one that hurts. When writing code is expensive, you naturally think before you start. When it is nearly free, the temptation is to start immediately and let the loop sort it out. That works for small things and quietly fails for large ones.

---

## The best working model: a brilliant junior with amnesia

An agent is a fast, tireless, extremely well-read engineer who:

- has **no memory** between sessions,
- has **not read your codebase** unless you make it,
- **cannot see what you see** unless you show it,
- is **uniformly confident** — equally sure when right and when wrong,
- **cannot tell** when it has misunderstood you,
- and **stops when the output looks like an answer**, not when it is correct.

This model predicts almost everything that goes wrong. If a new colleague with no context could not do the task from your instructions, neither can the agent.

It also predicts what helps: written context, examples to copy, explicit constraints, a way to check the result, and small enough tasks that misunderstanding is visible early.

Where the model breaks: an agent does not get bored, does not resent repetition, and will happily attempt things a junior would flag as unwise. **It has no professional fear.** That is your job.

---

## There are three scarce resources, and only one of them is the model

| Resource | Why it is scarce | How it gets wasted |
|---|---|---|
| **Context** | Finite, and quality degrades as it fills | Irrelevant files, verbose logs, failed attempts |
| **Your attention** | You are the reviewer, and you have a day job | Watching the agent instead of thinking ahead |
| **Verification capacity** | Every change must be checked by *something* | Changes too large or too vague to check |

Amdahl's law applies to your workflow: speeding up the part that was never the bottleneck buys you nothing. If tests take 20 minutes, no amount of generation speed helps. If review is the constraint, generating more code makes you slower.

This is the single most useful diagnostic question in this entire handbook:

> **Where does the work actually wait?**

Fix that. Not the prompt.

---

## The confidence problem

An agent's output has no error bars. A correct answer and a hallucinated one arrive in the same tone. Human collaborators leak uncertainty — they hedge, they ask, they say "I think". Agents mostly do not.

Consequences:

1. **You cannot use fluency as a signal.** Polished prose and confident code are equally likely to be wrong.
2. **You must design the check before you trust the answer.** Not after. Before.
3. **You must ask for evidence, not assurance.** "Run the test and paste the output" beats "are you sure?"

> [!IMPORTANT]
> The failure state is not "the agent made a mistake". It is "the agent made a mistake and you could not tell." Everything in [chapter 04](04-verification.md) exists to prevent the second one.

---

## What did not change

A useful antidote to the hype: list the things that are still exactly as hard as they were.

- **Knowing what to build.** The agent will build the wrong thing with excellent craftsmanship.
- **Decomposition.** A task too big to describe is too big to delegate.
- **Coupling and design.** Agents produce locally reasonable code that is globally incoherent, faster than humans do.
- **Correctness under concurrency, failure and time.** Tests pass; production disagrees.
- **Naming.** A codebase full of `handleData` is harder for a model to navigate too.
- **The cost of being wrong.** It is still paid in incidents, not in tokens.

The tools moved the *cost of production*. They did not move the *cost of being wrong*, except by increasing the volume of code exposed to it.

---

## When not to delegate

Principle 14 deserves its own short list, because the most common high-performer mistake is over-delegation.

Do it yourself when:

| Situation | Why |
|---|---|
| The design **is** the deliverable | You cannot specify what you have not yet thought |
| Security-critical logic you cannot fully verify | Unverifiable + high blast radius |
| A one-off script under ~50 lines | Specifying costs more than writing |
| Code you need to learn | The learning is the point; delegation removes it |
| Debugging a subtle production issue | The signal is sparse and the loop is slow; your intuition is the asset |
| Anything where verification ≈ implementation cost | You did not save work, you added a translation layer |

Delegation is a trade: you exchange **typing** for **specifying, reviewing and trusting**. That trade is excellent when the task is large, mechanical, verifiable, and low-blast-radius. It is terrible when it is small, subtle, or unverifiable.

---

## A reality check worth keeping

In 2025 a randomised controlled trial found experienced open-source developers were **19% slower** with the AI tools of the time, while believing they were faster. The follow-up work in 2026 suggests the picture has improved — but also that the measurement itself has become unreliable, precisely because the most enthusiastic users now refuse to work without AI, which biases every study.

Two durable lessons survive the changing numbers:

1. **Felt speed is not measured speed.** Track something real, or you are guessing.
2. **The effect is task-dependent and person-dependent.** "AI makes developers 30% faster" is not a fact; it is an average over a distribution you are not in the middle of.

Full details and links: [the reality check](08-judgment.md#the-evidence-is-messier-than-the-marketing) and [the reading canon](../reading/README.md).

---

## Practice

Answer these in writing. One paragraph each. Do not look anything up.

1. Name the last three times a task took longer than you expected. In each case, where did the work actually wait — specification, execution, verification, or review?
2. Which of your current tasks are *unverifiable*? What would it take to make each one checkable?
3. What is one thing you have shipped recently that you could not debug without the agent? (If the answer is "nothing", you are in good shape. If it is "several", read [chapter 08](08-judgment.md).)

---

**Next:** [02 · The working loop](02-the-loop.md) — the six stages, and the two kinds of failure.
