# 02: Commissioning the agent

Files for part two of my series, Guide for building an autonomous agentic system administrator: [Part 2: Commissioning the agent](https://onet.com.au/blog/sysadmin-agent-guide-part-2/).

| File | Use it when |
|---|---|
| `commissioning-checklist.md` | Taking the agent from an evaluated brief to a scheduled job: accounts, access, discovery, the first repair, the first report and the schedule. |
| `email-trust-rule.md` | **Before the agent acts on any email.** Authenticate the sender, then check it against an approved list. |
| `morning-health-check-job.md` | Scheduling the first daily health check as a script-only job, with the report format and the scheduling gotchas. |
| `morning-health-check.sh` | A template for that script. Syntax-checked and dry-run with placeholder targets only; customise it before use. |

These are working documents from a real setup, generalised for public use. They have not been tested in this generic form. They are starting points: customise them with your own agent, for your own estate.

**Version.** Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence.** CC BY 4.0. Use, adapt and share them, with attribution to Steve Waddington and Maxi Calder.
