# 05 · Environment

> **Principles 6 and 7** — Rules in the repo, gates in the tooling. Optimise the feedback loop.

---

## The claim

Two engineers use the same model, the same tool, the same prompt style, and get wildly different results. The difference is almost never the prompt. It is the **repository**.

An agent is a control system. Its output quality is bounded by how quickly and clearly the environment tells it that it is wrong. Everything in this chapter is about shortening that signal path.

> **The agent's speed is not the model's speed. It is your build's speed.**

---

## 1. Make the loop fast

| Slow | Fast | Why it matters |
|---|---|---|
| Whole test suite for every change | Single relevant test, whole suite on commit | 10× more iterations per hour |
| Cold start every run | Incremental / cached builds | Testing is cheap enough to actually do |
| 30s to boot the app | Watch mode, hot reload | The agent can observe behaviour |
| Reading 3 files to find the test command | `make test` | Three guesses eliminated |

Measure it. If your inner loop is over 60 seconds, that is your highest-leverage engineering project — above any AI tooling.

Test caching is underrated and language-dependent. Go's test cache means re-running is nearly free, which one experienced practitioner credits as a large part of why agents do well in Go. Languages where a test run costs 30 seconds of boot time make the same agent look much worse.

---

## 2. Make entry points deterministic

Agents guess. Every guess that can be eliminated is a failure that cannot happen.

Replace prose with commands:

```makefile
make dev      # start everything, refuse if already running
make test     # the fast suite
make test-all # everything, before commit
make logs     # tail the log file, not a terminal
make reset-db # seed to a known state
```

Two details matter more than they look:

**Idempotence.** If `make dev` is run twice, it should print *"already running"* and exit non-zero — not bind a second process to the same port. Agents genuinely do not know whether the server is already up, and they will start it again. A pidfile is a five-minute fix that removes an entire class of confusion.

**Persistence of output.** Print to the terminal *and* write to a log file. The agent can then read the log to diagnose, without you copying anything.

```bash
# bad: output only, gone when the terminal scrolls
npm run dev

# good: same output, plus a file the agent can read
npm run dev 2>&1 | tee -a .dev.log
```

---

## 3. Make side effects visible in development

The strongest environments let an agent complete a full user journey by itself.

Concrete example: sign-up sends an email with a verification link. In production that is invisible. In development, **log the email body and the link to stdout**. Now the agent can register, read the log, follow the link, and finish the flow — no human, no test-only backdoor.

Same principle for:

- Payment providers → a fake provider that logs the webhook payload.
- SMS / OTP → log the code in dev.
- External APIs → a recorded fixture directory.
- Queues → a local broker with a UI, or log the messages.

If a human must click something for the loop to close, the loop will not close unattended.

---

## 4. Write errors for a chaos monkey

Assume the caller will misuse every tool in every way. There is no undefined behaviour — only unhandled input.

A good tool error contains:

1. **What was wrong** ("unknown flag `--dry-runn`").
2. **What was expected** ("expected one of: `--dry-run`, `--verbose`").
3. **What to do next** ("did you mean `--dry-run`?").

A bad error is a stack trace with no context, or silence with exit code 1.

This applies to your own scripts too. Agents write helpers constantly; if those helpers fail opaquely, the agent burns ten turns guessing.

---

## 5. Prefer CLIs to MCP servers

MCP is useful when there is no other way to reach a system. It is overused.

For most integrations, a CLI is better:

| | CLI | MCP |
|---|---|---|
| Failure surface | One binary | Server, transport, auth, schema |
| Token cost | Only the output you asked for | Tool definitions loaded every session |
| Debuggable | You can run it yourself | Often opaque |
| Composability | Pipes, scripts | Tool calls only |

`gh`, `psql`, `aws`, `kubectl` — an agent that knows how to run `--help` can learn a CLI it has never seen. That is a general capability, and it costs nothing until used.

Use MCP when you need a structured, stateful integration (a browser, a design tool, a database with a schema contract). Do not use it to wrap a command that already exists.

---

## 6. Prose is advisory; hooks are deterministic

This distinction is worth internalising.

| Mechanism | Enforced? | Good for |
|---|---|---|
| Rules file | No — may be ignored | Conventions, context, preferences |
| Prompt | No | The current task |
| Hook / git hook / CI | Yes | Anything that must never happen |
| Linter rule | Yes | Style with an objective answer |
| Type system | Yes | Contracts |
| Sandbox | Yes | Blast radius |

If you have told the agent three times not to edit migrations, stop telling it. Add a hook that blocks writes to that directory. If you keep asking for the formatter to run, wire it to a post-edit hook.

> [!IMPORTANT]
> Every rule you enforce with prose is a rule you will eventually have to police manually. Convert the important ones into gates.

The corollary: **do not hook what should be a judgement call.** A hook that blocks all edits outside `src/` is a guardrail. A hook that decides whether an abstraction is justified is a straitjacket.

---

## 7. Control the blast radius, not the keystrokes

Permission prompts feel like safety and mostly produce fatigue. After the tenth approval you are clicking, not reading.

Better model:

- **Allowlist** the commands you trust (`make test`, `git status`, `npm run lint`).
- **Sandbox** the filesystem and network at the OS level.
- **Isolate** in a container or worktree for anything unfamiliar.
- **Deny by default** for unattended runs, with an explicit allowlist.

The goal is a space where the agent can act freely *and* where being wrong is bounded. Those are not in tension; they are the same design.

---

## Repo readiness scorecard

Score yourself honestly. Each "no" is a concrete project.

| | Question | If no… |
|---|---|---|
| ☐ | Can a new machine go from clone to passing tests with one documented command? | Write it. This is the single highest-value hour. |
| ☐ | Does the fast test suite finish in under 60 seconds? | Split it; cache it; parallelise it. |
| ☐ | Is there a single `make`/task entry point for dev, test, lint, logs? | Add one. |
| ☐ | Does the dev server refuse to start twice? | Add a pidfile. |
| ☐ | Are emails/codes/webhooks visible in dev logs? | Log them. |
| ☐ | Do your scripts fail with actionable messages? | Fix the top five. |
| ☐ | Are secrets absent from the repo and present in a documented env file? | Fix before anything else. |
| ☐ | Is the rules file under ~50 lines and free of things the code already says? | Prune it. |
| ☐ | Is formatting enforced automatically rather than requested? | Add a hook. |
| ☐ | Can you run an agent in a sandbox without giving it your whole home directory? | Set one up. |

---

## Practice

Time your own loop, literally, with a stopwatch:

1. From a clean checkout: how long until tests pass? (`t_clone`)
2. From an edit: how long until you see a result? (`t_inner`)
3. How long to run the full suite? (`t_full`)

Then compute how many iterations per hour you get: `3600 / t_inner`. That number is your actual agent throughput. Not tokens per second — iterations per hour.

Pick the largest of the three times and fix it this month.

---

**Next:** [06 · Code design](06-code-design.md) — the codebase is part of the prompt.
