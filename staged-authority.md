# Staged authority: widening what the agent may do

*Checked 23 October 2026. The method does not depend on Hermes. Where it refers to Hermes settings, they were checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check those points against your version.*

## Where to use this

Use this before you start, and again each time you are deciding whether to let the agent do more. The rest of this repository is organised by topic: identity, commissioning, monitoring, maintenance. This file shows the order in which those powers can be handed over, and what you should have seen before each step.

Treat it as an apprenticeship. The agent starts with very little authority, and each widening is earned by evidence you have checked yourself, not by how capable the agent sounds.

## Before stage 1

- Write the brief, identity and mandate as separate documents, and close default self-modification (part 1).
- Name the accountable human, and a fallback for when that person is unavailable. Every alert, report and reserved decision needs somewhere to go that a person actually reads.
- Decide where reports and urgent alerts are delivered, and check you can receive both.

## Stage 1: Read-only discovery

**The agent may:** log in, inspect, measure and write its own notes. Nothing else.

**Kit:** part 2, `commissioning-checklist.md` sections 1 to 4.

**Before moving on, you have seen:**

- access proven non-interactively, with the agent's own accounts and keys;
- an inventory of the estate that you have read and corrected;
- a negative test: the agent asked to change something, and either refusing because the mandate does not allow it yet or being stopped by a technical control. Prefer the technical control. A mandate is an instruction, not an enforcement mechanism.

## Stage 2: Named, reversible repairs

**The agent may:** repair a short list of named things in a named way, such as restarting an allow-listed service, and report what it did. Everything else is still report-only.

**Kit:** part 2, `commissioning-checklist.md` sections 5 to 7 and `morning-health-check.sh`; part 3, `server-health-monitoring.md`.

**Before moving on, you have seen:**

- one real repair done under your explicit instruction, and verified;
- a report you have actually received, saying only what is broken;
- the first **unattended** scheduled run, with its report received;
- a failure notification received. Break something harmless on purpose and check that the alert arrives where you expect it;
- an **overdue-report check**: if the morning report has not arrived by a set time, something independent of the agent tells you. Silence only counts as "all well" when you can show the check still ran;
- a dry run that makes no changes. Test it; don't assume it;
- what happens when the agent or its model provider is unavailable: which checks still run, and who finds out.

## Stage 3: Routine maintenance duties

**The agent may:** carry out the duties you would give a human sysadmin, such as standard package upgrades, backups, log and disk housekeeping and certificate renewals, under written policies, with anything outside routine coming back to you.

**Kit:** part 4, `routine-system-administration.md`, `backups.md`, `power-failure-recovery.md`, `verify-before-retry.md`.

**Before moving on, you have seen:**

- several weeks of unattended runs whose reports you have read, including at least one week with something to report;
- each written duty matched to a job that actually performs it. A runbook row is an intention until something runs it;
- recovery exercised, not assumed: a restore compared with its source, and a service brought back after a restart or power loss;
- a **denied-action test** for each reserved category that applies to you, for example a release upgrade or a package removal. The agent should stop and ask, and where possible a control should stop it anyway;
- a **revocation test**: remove one of the agent's permissions, check that it reports it can no longer do the job rather than finding a way round, then restore the permission.

## Stage 4: Outcomes, with residual authority

**The agent may:** do what a competent sysadmin would do to achieve the delegated outcomes, except for the reserved matters, under its governing duties.

**Kit:** part 1, `mandate-template.md`.

- Run it as a trial for a fixed period first, then review it and make it permanent or change it.
- Keep the reserved matters short and serious, and back them with technical controls where you can.
- Review on a schedule, and after any significant incident.

## Moving back down

A stage is not permanent. An incident of a particular kind returns that kind of work to an earlier stage until the cause is understood and the evidence has been rebuilt. Examples: an unverified repair reported as done, a report that silently stopped arriving, or a reserved action taken without approval. Reducing authority for a while is a correction, not a punishment, and the mandate should say so.

## When two instructions disagree: the narrower limit applies

The mandate grants broad powers. Individual jobs and policies narrow them. Example from these files:

- The part 1 mandate template's ordinary powers include installing, updating and removing software.
- The part 4 package policy says full or distribution upgrades, package removals and new repositories need a separate decision, and are not routine.
- So the daily maintenance job runs the standard upgrade only. A full upgrade waits for an approved exact transaction, even though the mandate in general would allow it.

The rule: a job's instructions and a written policy can narrow the mandate but never widen it. The agent obeys both, and where they differ the narrower one wins. To widen a job, change its instructions through the normal approval route. Do not let the agent decide in the moment that the mandate's broader wording covers it.

## How it went for us

The stages above are written in hindsight. Our sysadmin agent did move through them, roughly in this order. At the end of May it could inspect the estate and was told to fix trivial issues and report. Its first real repair was made on explicit instruction. Routine maintenance duties came in July, with a written mandate that ran as a one-week trial before it was made permanent, and the outcome-based mandate with residual authority followed in August.

What we did not do was write down the evidence for each step in advance. Mostly it was the human's judgement at the time. Several of the checks above, the overdue-report check and the revocation test in particular, are ones we would put in at the start if we were doing it again.

*Licence: CC BY 4.0. Use, adapt and share with attribution to Steve Waddington and Maxi Calder.*
