# 03: Watching the estate

Files for part three of my series, Guide for building an autonomous agentic system administrator: [Part 3: Watching the estate](https://onet.com.au/blog/sysadmin-agent-guide-part-3/).

| File | Use it when |
|---|---|
| `server-health-monitoring.md` | Adding continuous watching and an agent responder: principles, our three monitoring jobs, alert gating, classifying before repairing, and honest reporting. |
| `wake-gated-cron-jobs.md` | **Before you attach a script to a Hermes agent job.** The three job shapes, the wake gate, and why empty output means opposite things in different modes. |
| `edge-triggered-log-notifier.md` | Alerting from a log on the same machine, when a condition starts and ends, without a message for every line. |
| `watchdog-gate.py` | A template of the alert-gating rules as a pure, testable function. Runs its own tests (`python3 watchdog-gate.py --self-test`); not our production watchdog. Revised 23 October 2026: until you wire in probes it reports UNCONFIGURED and wakes the agent rather than looking healthy (`--demo` shows the healthy output), and a missing repeat result counts as a failure. |

These are working documents from a real setup, generalised for public use. They have not been tested in this generic form. They are starting points: customise them with your own agent, for your own estate.

**Version.** Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence.** CC BY 4.0. Use, adapt and share them, with attribution to Steve Waddington and Maxi Calder.
