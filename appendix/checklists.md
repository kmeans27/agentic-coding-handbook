# Checklists

Copy-paste these. They are deliberately short — a checklist you will not use is worse than none.

---

## 1 · Before you prompt (60 seconds)

- [ ] I can state how I will know this worked.
- [ ] The task fits in one session. If not, I have split it.
- [ ] I know which files or module are involved — or I have scoped the exploration.
- [ ] I know what is **out of scope**.
- [ ] This is worth delegating: it is not trivially small, and I can verify it.
- [ ] My context is clean enough that this task is the main thing in it.

If any box is unticked, fix that before typing.

---

## 2 · Spec template

```markdown
## Goal
One paragraph, written for someone who has not seen the ticket.

## Files and interfaces
- path/to/file.ts — what changes, which function/interface
- Reuse: path/to/existing/pattern.ts (follow this pattern)

## Out of scope
- Things the implementer might reasonably be tempted to do, but must not.

## Verification
- New test: <name> — <what it proves>
- Existing checks that must stay green
- Manual / visual step, if applicable
```

Rule of thumb: if you cannot fill in **Out of scope**, you have not decided what the change is.

---

## 3 · Definition of done

Customise per project. Every line must be one you would actually enforce.

```markdown
- [ ] A test failed before the change and passes after — and I saw both.
- [ ] Full suite passes; I have seen the summary line, not a claim.
- [ ] Types and lint pass.
- [ ] The diff contains nothing outside the stated scope.
- [ ] Structural and behavioural changes are in separate commits.
- [ ] UI: screenshot matches the target (differences listed and resolved).
- [ ] Data/migrations: run against a copy and rolled back.
- [ ] I can explain the change without opening the agent.
```

---

## 4 · Reviewing a diff

Read the diff, not the summary.

- [ ] Does it do what the spec asked — and **only** that?
- [ ] Are test changes additions, or weakenings?
- [ ] Is any error swallowed (`except: pass`, empty catch, ignored rejection)?
- [ ] Is any assertion tautological or mocked around the thing under test?
- [ ] Are permission / auth checks present **at the point of change**?
- [ ] Are new dependencies justified, or could 30 lines replace them?
- [ ] Is anything irreversible (migration, deletion, config) without a rollback?
- [ ] Would this survive a hostile reader trying to break it?

**Fresh-context review prompt:**

```text
Review this diff against PLAN.md. You did not write it.
Report only gaps that affect correctness or a stated requirement.
For each: file, line, what breaks, how to reproduce.
Do not report style, naming, or speculative future needs.
```

---

## 5 · Repo readiness

Score one point per box. Below 7 is a project.

- [ ] Clone → passing tests in one documented command
- [ ] Fast suite under 60 seconds
- [ ] One entry point for dev / test / lint / logs
- [ ] Dev server refuses to start twice
- [ ] Emails, OTPs and webhooks visible in dev logs
- [ ] Scripts fail with actionable error messages
- [ ] Secrets in a documented env file, never in the repo
- [ ] Rules file under ~50 lines, no restating of the code
- [ ] Formatting enforced by a hook, not a request
- [ ] Agents can run sandboxed without access to your home directory

---

## 6 · Weekly self-audit (5 minutes, Friday)

- [ ] Did any diff merge that I could not explain on Monday?
- [ ] Which task took longest, and where did it actually wait?
- [ ] Did I revert anything? What would have prevented it?
- [ ] What did I tell the agent twice this week? → move it into a rule or a hook.
- [ ] What did I learn that belongs in the rules file, and what should be deleted from it?

---

## 7 · When the agent is stuck

In order. Stop at the first that applies.

1. **Is it a specification error?** Has it failed twice in the same place? → clear, rewrite the plan.
2. **Is the context polluted?** Long session, many failed attempts? → clear, restate with what you learned.
3. **Is the task too large?** Can you split it into independently verifiable pieces? → split.
4. **Is the feedback loop too slow or too noisy?** → fix the tool, not the prompt.
5. **Is the requirement actually unclear to *you*?** → stop prompting; decide.
6. **Is this unverifiable?** → do it yourself, or build the check first.

---

**Back to:** [README](../README.md) · [Prompt patterns](prompt-patterns.md)
