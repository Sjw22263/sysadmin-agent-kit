# Guide for building an autonomous agentic system administrator

Skills, templates and working documents for setting up an AI agent as a system administrator, from a real setup that has run since May 2026. These files accompany a blog series by Steve Waddington, one folder per post.

They are working documents, generalised for public use. They have not been tested in this generic form. Treat them as starting points to customise with your own agent, for your own estate. Each file says where to use it and puts the mistakes we made at the point where you would make them.

## Start here: staged authority

[`staged-authority.md`](staged-authority.md) sets out the order in which to hand the agent more authority, from read-only discovery to an outcome-based mandate, and what you should have seen before each step. It also shows which instruction wins when the mandate and a job's own limits disagree. Read it before you adapt the folders below.

## Contents

| Folder | Post | What it covers |
|---|---|---|
| `01-giving-the-agent-a-job/` | [Part 1: Giving the agent a job](https://onet.com.au/blog/sysadmin-agent-guide-part-1/) | Stop the agent rewriting its own procedures; the first brief; an identity file; an operating mandate. |
| `02-commissioning-the-agent/` | [Part 2: Commissioning the agent](https://onet.com.au/blog/sysadmin-agent-guide-part-2/) | Accounts, proven access, discovery, the first repair, email trust, and a script-only morning health check. |
| `03-watching-the-estate/` | [Part 3: Watching the estate](https://onet.com.au/blog/sysadmin-agent-guide-part-3/) | Wake the agent only for confirmed faults: alert gating, safe repair, honest reporting, wake-gated cron jobs and a log notifier. |
| `04-owning-the-maintenance/` | [Part 4: Owning the maintenance](https://onet.com.au/blog/sysadmin-agent-guide-part-4/) | Routine duties with a control for each, package policy, backups that can be trusted, power-failure recovery, verify before retry, and a backup-check template. |
| `05-reflection-that-changes-work/` | [Part 5: Reflection that changes work](https://onet.com.au/blog/sysadmin-agent-guide-part-5/) | Bounded improvement research, specific lessons for the next run, a human review route and trials that can be dropped as well as kept. |
| `06-continuity-without-a-memory-landfill/` | [Part 6: Continuity without a memory landfill](https://onet.com.au/blog/sysadmin-agent-guide-part-6/) | Memory as an index and Markdown as the archive, runbook and incident templates, memory review, and a trial for whether an extra memory layer earns its place. |
| `07-from-operator-to-estate-overseer/` | [Part 7: From operator to estate overseer](https://onet.com.au/blog/sysadmin-agent-guide-part-7/) | Onboarding a new agent, handing work between agents in plain files, and simplifying an estate with controls on decision provenance and retirement. |

More folders will be added as the series continues.

## Platform

The agent runs on [Hermes Agent](https://github.com/NousResearch/hermes-agent). Most of the method carries over to other agent platforms; the settings and commands are Hermes-specific. Each file states the Hermes version it was checked against. Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Licence

[CC BY 4.0](LICENSE). Use, adapt and share these files, including commercially, with attribution to Steve Waddington and Maxi Calder.

Maxi Calder is the sysadmin agent these documents were developed with. See the note in `01-giving-the-agent-a-job/README.md` on how it chose its name.
