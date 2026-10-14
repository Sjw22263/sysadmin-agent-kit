# The first brief: a daily health check

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Where to use this

This is the first real job to give a sysadmin agent once it is installed and can reach your systems. It is small, useful every day, and it exercises everything the agent will need later: access, discovery, judgement about what is broken, a repair boundary, and a report that reaches you.

Write it the way you would brief a new human sysadmin. Then ask the agent to evaluate it before building anything.

## The brief

Replace the bracketed parts. Keep the last paragraph.

```text
The next task is a daily morning health check and briefing.

Each morning at [time]:
- Check that these websites are responding and have no issues: [sites].
- Run a health check on your own server, including [services you care about].
- Run a health check on [other servers], and check that [mail / databases / other services] are working.

If there is a trivial issue, try to fix it. If there is a serious issue, plan how to fix it
and tell me via [urgent channel]. Tell me if you need escalation or permissions.

Send me a report via [channel] called "[report name]". The default should be
"Everything is OK, except:". Only report what is broken. For a serious issue, tell me
how it can be fixed and what you need me to do.

Before you set this up, please evaluate the task and the resources you will need.
Ask if you want any clarification or can see anything I might have missed.
```

## Why the last paragraph matters

When I gave this brief to my own agent, it came back with nine findings and seven questions before building anything. Among other things, it found:

- it could not yet log in to one of the servers;
- it could not tell from outside where mail was actually handled, because the public addresses and the internal network did not line up in an obvious way;
- it lacked the permissions to check part of its own server, and had stopped rather than force the issue.

Its recommendation was: "don't create the cron job yet ... otherwise I'd be building a daily health check with a blind spot exactly where you care about it." Without that paragraph in the brief, I would have had a health check that reported on everything except the parts I most cared about.

## Expect these questions, and answer them before the job runs

These are the questions my agent asked. Yours will ask similar ones if you invite it to.

1. Which account does it use on each server, and how is it authorised to log in?
2. Does it have the elevated rights it needs (for example `sudo`) to inspect and repair, and on which machines?
3. Which services, by exact name, may it restart?
4. Where does each service actually run? (Address translation and split networks can make this unclear from the agent's side. Tell it.)
5. Should it send a real test message to prove mail works, or only test connectivity?
6. Which channel is for urgent alerts, and which for the routine report?

## Define "trivial" in writing

"If there is a trivial issue, try to fix it" is only safe once trivial is defined. My agent proposed this split, and it is a good starting point.

**Allowed in the daily job:**

- restart named services on its own server;
- restart a named application stack if its health check fails;
- remove stale lock or temporary files only where they are known to be safe;
- restart services on other servers only by exact, pre-approved name.

**Not allowed in the daily job:**

- editing configuration;
- upgrading packages;
- rebooting servers;
- changing DNS or firewall rules;
- renewing certificates by hand;
- deleting logs or mail queues;
- repairing databases.

These limits are for an unattended daily job, not for the agent in general. As trust grows, upgrades and patching become owned work under the agent's mandate (see `mandate-template.md`).

## The report

After the first report arrived I tightened the rule: "I only want the report to say what is broken." A report that lists every healthy service trains you to stop reading it. Default to one line when all is well. For anything serious, the report should say what failed, what was tried, the result, and exactly what the agent needs from you.

## Gotchas

- **Verify the report reaches you.** The job is not working until you have received a report, not when the agent says it has sent one.
- **Prefer a script for the checks.** Let a deterministic script collect the facts on schedule and keep the model for judgement and repair. It is cheaper, and the result is the same every day. (Running checks without waking the model is the subject of a later post.)
- **Turn off agent self-modification first.** See `hermes-self-modification.md`.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
