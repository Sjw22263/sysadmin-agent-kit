# 04: Owning the maintenance

Files for part four of my series, Guide for building an autonomous agentic system administrator: [Part 4: Owning the maintenance](https://onet.com.au/blog/sysadmin-agent-guide-part-4/).

| File | Use it when |
|---|---|
| `routine-system-administration.md` | Giving the agent a system administrator's routine duties: a daily, weekly and monthly duty table, a package-maintenance policy, reboots and boundaries. |
| `backups.md` | **Before the agent builds or changes a backup.** The rotation contract, design rules, restore testing, and scheduling long jobs, including two Hermes cron behaviours that matter for backups. |
| `power-failure-recovery.md` | Before your first power cut: making servers come back on their own, alerting the agent, and checking what actually recovered. |
| `verify-before-retry.md` | A standing procedure for any change that ends ambiguously: check the real state before trying again. |
| `backup-set-check.py` | A template daily check of a backup directory: missing or half-present checksum files, corrupted or stale archives, too few generations. Runs its own tests (`python3 backup-set-check.py --self-test`); not our production code. |

These are working documents from a real setup, generalised for public use. They have not been tested in this generic form. They are starting points: customise them with your own agent, for your own estate.

**Version.** Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence.** CC BY 4.0. Use, adapt and share them, with attribution to Steve Waddington and Maxi Calder.
