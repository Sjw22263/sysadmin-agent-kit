# Owning the maintenance: routine system administration

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Where to use this

Use this once the agent is watching your systems (part 3) and you are ready to give it the rest of the job: the routine duties a human system administrator would own. It is a template for a duty list, a package-maintenance policy and the boundaries around both. Work through it with your agent and replace our examples with your own systems.

## Start with the job, not the tasks

The brief that started our duty list was five lines:

1. consider the tasks a competent system administrator would perform on a daily or routine basis.
2. make a comprehensive list of those tasks.
3. where scriptable, write cron jobs to perform the tasks.
4. Run through your checklist each day and do the unscriptable tasks.
5. take actions necessary (for example, updates, upgrades, security patches, etc)

If you have employed or managed system administrators, use the duties from their job descriptions. That gives you a standard you already know how to judge, and it tests the agent on ordinary work rather than demonstrations.

## How the duties run

- **Scripts collect facts. The agent handles exceptions.** Each duty has a control: a scheduled script, an existing check, or a review the agent performs. Routine success stays quiet. A material exception is reported with evidence, the action taken and any decision needed from you.
- **Use the wake gate from part 3.** Our daily maintenance audit runs early in the morning, after the backup window. It refreshes package lists, checks package integrity, pending reboots, failed services, disk, inode and memory pressure, and backup freshness. If nothing needs doing it prints `{"wakeAgent": false}` and no model runs. Otherwise it prints the findings and the agent does the work.
- **Every duty needs a control, not just a line in a table.** A duty with no scheduled job or named owner is an intention. Review the table for duties that nothing actually runs.

## Duty table (template)

Replace the controls with your own. The table is the job description; the controls are how you know it is being done.

### Daily

| Duty | Control | On exception |
|---|---|---|
| Core service and public health | Morning health check (part 2) and watchdog (part 3) | Repair known faults; escalate a material outage. |
| Recovery after a reboot | A boot-triggered check of the services each server provides | Treat any failed or inconclusive check as urgent; alert, repair, recheck. |
| Package state, pending reboots, failed services, disk/inode/memory pressure, backup freshness | Wake-gated daily maintenance audit | Apply ordinary updates, repair incomplete package state, schedule a controlled reboot. |
| Security events and configuration anomalies | Daily security check | Investigate, contain if the evidence is strong, escalate posture or access decisions. |
| Backups produced and copied | Backup jobs plus freshness checks (see `backups.md`) | Investigate a missed or failed backup before the next retention window is lost. |

### Weekly

| Duty | Control | On exception |
|---|---|---|
| Deferred and phased updates | Audit output and an upgrade simulation | Apply ordinary updates when they become eligible. |
| Storage and filesystem trends | Daily figures plus a weekly review | Investigate persistent growth, failing mounts or unexpected retention changes. |
| Backup chain | Weekly backup output and latest archives | Confirm the promoted weekly copy exists where it should. |
| Certificate expiry horizon | TLS checks and certificate inventory | Renew through existing automation, or investigate before expiry. |
| Scheduled-job integrity | Job state and run history | Repair a job only to restore its agreed purpose. Do not quietly expand it. |

### Monthly

| Duty | Control | On exception |
|---|---|---|
| Recovery readiness | Restore a representative backup into a scratch location and compare it with the source (see `backups.md`) | Treat unreadable or unrestorable backup data as an incident, not an administrative note. |
| Capacity and retention | Review disk, backup growth, logs and caches | Change retention or capacity only when the evidence requires it. |
| Security posture | Review exposed services, authentication logs, update posture, privileged access | Propose posture changes separately where they change firewall rules, access or exposure. |
| Runbook accuracy | Compare runbooks with live services and paths | Update documentation when durable facts have changed. |

> **Our gap, so you can avoid it.** The monthly row above is deliberately stronger than the one we had written for ourselves. Ours asked only that a representative archive be readable with a valid checksum, and a weekly backup job already does that much for one of our archives. What we had never established was a recurring test that actually restores data and compares it with the source. Restore tests were done when each backup was commissioned, and several of our jobs verify the checksums of the archives they write, but no schedule took a backup apart again afterwards. Two lessons rather than one: write the monthly row as the test you actually want, and then check that something runs it. Monthly duties are the easiest to write and the easiest to forget.

## Package maintenance policy

1. Keep the distribution's automatic security updates enabled.
2. Have the daily audit refresh package lists and find ordinary upgrades independently. Security-only automatic patching leaves ordinary stable updates waiting.
3. The routine action is the standard upgrade (`apt-get upgrade` on Debian and Ubuntu), because it neither installs new packages nor removes installed ones.
4. Full or distribution upgrades, package removals, dependency-changing driver or firmware updates, release upgrades and new third-party repositories need a separate, evidence-based decision. They are not routine automation.
5. When you approve something outside the routine, approve the exact transaction for one run: package names, candidate versions, counts of upgrades, new packages and removals, and an expiry. Have the job check the real transaction against the approval immediately before installing, and fail closed on any difference. Then delete the approval. An approval that is not used up becomes standing permission by accident.
6. Use the real transaction, not a report of it. A simulation run without privileges, or another agent's summary, can count packages differently from the transaction that will actually run.
7. A package manager exiting successfully does not finish the job. Check package state, the services that depend on the change, and the real endpoint or workload afterwards.

### Accepted deferrals

Write down a decision not to act, with the conditions that would reopen it. Otherwise the agent will raise the same kept-back package every day, or eventually "fix" it. Ours: a GPU driver package the package manager keeps back on a server with no GPU workload. The record says why, and what would change the decision (a GPU workload, a security issue in the installed branch, a faulty package state, or the owner changing their mind).

## Reboots

- A pending reboot is operational work, not something to put off indefinitely.
- Reboot in the maintenance window, after backups, in dependency order (the server others depend on first), with real post-boot checks of what each server provides.
- If other agents or long-running work share the host, coordinate before the window: say what will happen and when, ask for a list of active work, scheduled jobs and state that must survive, and check it yourself afterwards. Keep that list as a file, because the exchange cannot happen while the host is down.
- Urgent recovery does not wait for consultation. Act, then inform and reconcile afterwards.

## Boundaries

- Scripts do not make security-policy, firewall, credential, access-control or architecture changes.
- After a one-off recovery, a privileged rerun or a partial recovery, test the normal production path, not just the exceptional command. See the root-owned lock example in `backups.md`.
- Historical warnings are not incidents unless they are still active or recur.
- Routine success stays quiet. Report material exceptions with evidence, action and any decision needed.

## Hermes notes

- Hermes cron schedules use the timezone set in Hermes's `timezone` setting, or the server's local time if it is unset. The system scheduler (cron or systemd timers) uses the system timezone. If a maintenance job must run after a backup run by the other scheduler, check that both agree.
- Run the maintenance audit as an agent-mode job with a script, so the wake gate applies. See part 3's `wake-gated-cron-jobs.md`, including the warning that empty script output wakes the agent in this mode.
