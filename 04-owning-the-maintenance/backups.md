# Owning the maintenance: backups that can be trusted

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Where to use this

Use this when you ask the agent to build, change or review a backup. It is a set of design rules and the mistakes behind them. It is not a backup tool. Use proper backup software where it fits; these rules apply whatever does the copying.

## Agree the rotation contract before anything is built

"Copy the backups to the external drive" is not a specification. Before the agent builds anything, have it restate, for each data set:

- how often a backup is made, how it is named and how many are kept;
- which backups are promoted to weekly and monthly tiers, how they are named and how long they are kept;
- which tiers go to which destination (all dailies, or only promoted copies);
- what runs first. A copy job must run after the job that creates the files it copies.

Do not let a contract agreed for one data set be assumed for another.

## Design rules

1. **Keep history, not a single slot.** Do not use fixed names such as `weekly` and `monthly` for data that changes. If something corrupts the data while nobody is looking, each tier is overwritten with corrupt data in turn, and every restore point is bad. Name generations by date, keep several, and prune by retention.
2. **Verify before a new generation counts.** Write to a temporary name, verify it (checksum manifest, archive integrity), and only then publish it as a restore point. An interrupted partial copy is not a restore point.
3. **"Immutable" means not overwritten, not "known good".** On each run, re-verify retained generations as well as the new one, and fail the whole run if any are damaged. A retained archive that is never re-read can decay while the job keeps reporting success.
4. **A half-present pair is a fault.** If an archive exists without its checksum file, or the other way round, stop and investigate. Regenerating the missing half destroys the evidence of an earlier incomplete run.
5. **Fail closed when the destination is missing.** Check the destination is actually mounted before writing. A script that writes to an empty mount point fills the system disk and reports success.
6. **Never prune before verifying.** A failed copy or verification must leave the existing generations untouched.
7. **Test the failure paths.** The success path passes easily. Write a test that corrupts a retained generation and confirms the next run fails.
8. **Quiet success, loud failure.** Do not send a message for every successful backup. People stop reading them, and the failure that matters arrives in a stream of noise. Send failures with the job name, exit code and a short excerpt. Record a failed alert delivery somewhere the daily report will see it.
9. **Separate data history from quick-recovery bundles.** A current export of a container or service is useful for fast recovery, but it does not replace dated data history.
10. **Be honest about where the copies are.** Two copies on two devices in the same building protect against a failed device, not against fire or theft. Ours are both on-site at the time of writing; we know that, and you should know it about yours.

## Restore testing

- Restore into a scratch directory, never over live data.
- Compare what you restored with the source: checksums for regular files, and the things checksums miss, such as symbolic link targets, hard links, ownership and permissions.
- For a database, import the dump into a disposable database, compare something meaningful (row counts by type, for example), then drop it.
- Restore when each backup is commissioned, and again on a schedule. A restore test that is only on a duty list is not happening; see `routine-system-administration.md`.
- `backup-set-check.py` in this folder is a template for the cheaper daily part of this: every archive has a valid checksum, nothing is half-present, the newest is recent enough and enough generations exist. It does not replace an actual restore.

## After an outage

- A job that was scheduled while the machine was down may have been missed, or it may run late. Check your scheduler before you decide: some catch up after boot (persistent systemd timers, for example) and some do not. Report it as a missed, delayed or failed run on the evidence of the run record and the artefact it should have produced, with the next scheduled run and whether a catch-up is needed. Do not call it data loss unless the expected data is missing and cannot be regenerated.
- Restore chains in source-first order. If one job creates an archive and another copies it off the server, run the creator first and verify its output, then run the copy. Copying first succeeds and preserves yesterday's archive.

## After running a job by hand, test the normal path

Running a backup by hand to recover from a failure, especially as a different user, can leave behind files the normal scheduled run cannot use. Ours: a recovery run as root created the backup's lock file in `/tmp` with root ownership. The next scheduled run, as the normal user, could not open it, and failed although nothing held the lock. The fix was to keep the lock inside the backup's own directory, require that it is a regular file and not a symbolic link, and reset ownership of anything root created. The non-symlink condition matters: a check that accepts a symbolic link will follow it, which is worse when the next step changes ownership with privilege. The general rule: after any manual or privileged recovery run, prove the next normal run works.

## Scheduling long backup jobs

- **Put long infrastructure jobs on the system scheduler** (cron or systemd timers) rather than the agent's scheduler. They then run when the agent platform is down or restarting, and they keep their own locking and logs.
- **Hermes note: check the script timeout for your version.** Hermes stops a cron job's script when it reaches its timeout. Until late June 2026 the default was 120 seconds, too short for multi-gigabyte backups, which is why we moved ours to system cron. Upstream raised the default to one hour (`cron.script_timeout_seconds` in `config.yaml`, or the `HERMES_CRON_SCRIPT_TIMEOUT` environment variable). Our own notes still warned about 120 seconds when we prepared this file, which is a fair example of why every version-specific claim needs checking.
- **A timeout is a kill, not a polite stop.** When Hermes times a script out it kills the script's whole process tree with SIGKILL. A shell `trap ... EXIT` does not run. If a backup stops a service and relies on an exit trap to restart it, a timeout leaves the service stopped. After any timeout on a script that changes service state, check the service.
- **Watch the timezone.** Hermes cron uses its configured `timezone` (or server local time); the system scheduler uses the system timezone. Do not convert to UTC unless your scheduler actually runs in UTC.
- **Make the environment explicit.** System cron runs with a sparse environment. Set `HOME`, `SHELL` and `PATH` in the crontab, and have scripts read any secrets they need from a protected file at run time rather than storing them in the script.

## Recovery procedures and the Hermes curator

Recovery procedures are used rarely by design. If your agent's background review wrote a restore procedure as a skill, the curator may archive it after a month unused. Part 1's `hermes-self-modification.md` explains how to check what the curator manages (`hermes curator status`) and pin what you rely on (`hermes curator pin <skill>`).
