# Wake-gated cron jobs: run the model only when there is a reason

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). The gate conventions below were read in the Hermes source at that commit (`cron/scheduler_prompt.py`, `cron/scheduler.py`, `cron/scheduler_script.py`). Hermes has thousands of commits per month, so ask your agent to check them against your installed version.

## Where to use this

Any scheduled job where most runs find nothing to do: watchdogs, inbox checks, queue watchers, change detection. If a job runs 288 times a day and finds something twice, 286 model runs are waste.

It is a poor fit for jobs that genuinely produce output every run, such as a daily report or a backup. Those can still use a script to do the work.

## Three job shapes in Hermes

| Shape | How | When nothing is wrong | When something is wrong |
|---|---|---|---|
| Script only | `--script x --no-agent` | Empty output: silent, no model | Output delivered as written, no model |
| Wake-gated agent | `--script x` (agent mode) | Last output line `{"wakeAgent": false}`: no model, no delivery | Script output is added to the agent's prompt and the agent runs |
| Monitor | `--monitor-script x` or `--monitor-url` | Output unchanged since last run: agent skipped | Changed output: agent runs with the difference |

Scripts must be in `~/.hermes/scripts/`. If the script exits non-zero, a script-only job reports a failure, and an agent-mode job wakes the agent and tells it the data-collection script failed. Either way, exit non-zero only when the checker itself is broken, never for "nothing to report".

> **The gotcha that costs money.** Script-only and wake-gated jobs treat empty output **oppositely**. In a script-only job, empty output is silence. In an agent-mode job, empty output **wakes the agent**. Only a last non-empty output line that parses as a JSON object with `"wakeAgent": false` stops it, for example `{"wakeAgent": false}`. Anything else, including malformed JSON, wakes the agent. Moving a script from one mode to the other without changing its output will start a model run on every tick.

## Writing a wake-gated script

- **Nothing to do:** make the last line `{"wakeAgent": false}`.
- **Something to do:** print the data the agent needs, then finish with a line the script controls, `{"wakeAgent": true}`, after all variable content. If you let variable data be the last line, data that happens to look like a false gate will suppress real work.
- **Checker broken:** exit non-zero.

A healthy tick from our watchdog prints a single JSON object with `"wakeAgent": false` and an empty issues list. The scheduler records a silent run and nothing else happens.

## Use a script for yes-or-no questions

If the question is a deterministic check over local state (does this file exist, did this happen in the last day, is this process running), answer it in a script, not a model. We had an agent job that ran the right search, got the right answer, and reported the opposite in its final message. A script cannot contradict its own `if` statement.

## When the message format matters, do not leave it to the model

We told a cheaper model to reply with exactly one of two fixed lines. It added helpful detail anyway. Stronger wording did not reliably fix it. The fix was to split the job in two:

1. an agent job investigates and writes a small, validated JSON result to a local file, and delivers nothing itself;
2. a script-only job, scheduled after it, reads the file, checks its date and shape, and prints one of the fixed lines.

A missing or malformed result is an alert, not a silent success.

## Notification modes

Choose deliberately for each job:

| Mode | When | Example |
|---|---|---|
| Silent | Nobody needs to know it ran | Agent replies exactly `[SILENT]`; script-only job prints nothing |
| One line | You want a heartbeat | `Weekly maintenance done` |
| Detail | Something needs attention | What is broken, what was tried, what is needed |

`[SILENT]` suppresses delivery of an agent job's reply. It does not save the model run: the agent has already run. Use the wake gate to save the run.

When you tell a model what counts as a problem, also tell it what does not: routine corrections the job made, historical errors from configurations no longer in use, harmless empty results, normal metrics. Without the negative examples, every observation becomes a "problem".

## Gotchas

- **A manual run has its own completion notice.** Running a job by hand reports back to you even when the job itself was silent. Check the job's own output and delivery state to confirm silence.
- **Pause the old job before enabling its replacement**, or both will process the same work.
- **Check the next tick.** After creating or changing a job, confirm the next scheduled run fires without error, not just that the job saved.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
