# The first scheduled job: a script-only morning health check

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check the cron options below against your installed version.

## Where to use this

This turns the brief from part 1 into a job that runs every morning. Use it once the commissioning checklist is complete: access proven, services named, repair boundary written down.

## The shape

Start with a deterministic script, not an agent run. The script:

1. checks the things in the brief;
2. restarts only services on an explicit allow-list, and confirms they came back;
3. emails a report every morning, so the report itself proves the job ran;
4. prints to its output only when something serious remains unresolved.

Scheduled with `--no-agent`, the script is the whole job. No model runs, so it costs nothing beyond the script, and it does the same thing every day. Hermes delivers whatever the script prints to the job's delivery target, which makes that your urgent channel. Empty output is a silent run.

Our first scheduled version was exactly this. The judgement work, deciding what a fault means and fixing what the script cannot, comes later and only when the script finds a fault (part 3).

`morning-health-check.sh` is a template of this shape. Customise it with your agent, then run it by hand with `DRY_RUN=1` until the report reads correctly, then for real until you have received it. `DRY_RUN=1` makes no changes and sends nothing: a stopped service on the restart list is reported as "would restart". An earlier version of this template still restarted services in a dry run; if you copied it before 23 October 2026, replace it.

## The report

```text
Everything is OK.
```

or

```text
Everything is OK, except:

- what is broken, with the evidence
- what was tried, and the result
- what is needed from you
```

Only broken items. A report that lists every healthy check trains you to stop reading it.

Keep repairs separate from open problems. A service that was down, was restarted and is confirmed running is a fix, not an open issue. We once had successful restarts reported as unresolved incidents, which is the quickest way to make a report untrustworthy.

## Scheduling it

Put the script in `~/.hermes/scripts/`, make it executable, then ask your agent to create the job, or create it yourself:

```bash
chmod +x ~/.hermes/scripts/morning-health-check.sh
hermes cron create "0 6 * * *" --name "Daily server health report" \
  --script morning-health-check.sh --no-agent --deliver telegram
hermes cron list
```

Replace `telegram` with your own urgent channel. Then read back the job: schedule, repeat setting and next run time.

## Gotchas

- **Script location.** The scheduler refuses scripts outside `~/.hermes/scripts/`. Ours failed to schedule the first time for this reason.
- **Local time.** `0 6 * * *` means 6 am in the scheduler's local time. Do not convert to UTC.
- **Repeat.** Confirm in the read-back that the job repeats. One of our early jobs was created to run once.
- **Exit codes.** Exit non-zero only when the script itself is broken. Hermes reports a non-zero exit as a job failure, which is what you want for a broken checker and not what you want for "nothing to report".
- **The report is the delivery test.** If the script cannot send the report, it should say so on its output so the urgent channel catches it.
- **Mode change.** If you later attach this script to an agent job instead of a `--no-agent` job, empty output **wakes the agent**. Only a final output line that is a JSON object containing `"wakeAgent": false`, such as `{"wakeAgent": false}`, stops it. Read part 3 before switching.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
