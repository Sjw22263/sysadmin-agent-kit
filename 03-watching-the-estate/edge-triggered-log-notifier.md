# Edge-triggered log notifier: alert on changes, not on every line

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). The log line formats below are Hermes's and change between versions: ask your agent to confirm them against your installed version and real log lines before relying on them.

## Where to use this

When the thing you want to know about is a line in a log on the same machine, and you want to hear when a condition **starts** and when it **ends**, not every time it is logged.

Our case: tell me when an agent's model falls back from its primary to a fallback, when it moves further down the chain, and when it recovers. During a provider outage every turn logs a fallback. A naive `grep | send` sends a message per turn.

Not this pattern:

- **Something outside the machine** (an external service calling you) is what webhooks are for.
- **A periodic measurement** (disk space, a website) belongs in a scheduled check (`wake-gated-cron-jobs.md`).

## The design: a state file and transitions

The daemon keeps a small state file recording the last state it told you about. It sends a message only when the state changes.

```text
state: {status, primary, current, current_rank, session_id}

on each successful model call:
    same model as current:        stay silent
    lower in the fallback chain:  send "degraded"
    back to primary:              send "recovered"
    higher, but not primary:      send "partly recovered"
```

A multi-hour outage then becomes a handful of messages, one per real change.

Treat the fallback list as ordered (index 0 is the primary) and do not assume steps are taken one at a time. A primary can drop straight to the last fallback, and the last fallback can recover straight to the primary.

## Rules that matter

- **Detect recovery from a positive success signal, not from silence.** No more fallback lines may just mean nobody is using the agent. In Hermes, alert from the successful API-call line, which names the model and provider that actually answered. The "fallback activated" line only records an attempted switch.
- **Debounce bursts.** One turn can log several steps down the chain in quick succession. Hold the alert for a few seconds and send one message naming where it started and where it landed.
- **Filter by session.** Scheduled jobs and other conversations write to the same log. Interleaved calls from different sessions using different models look like constant switching. Track one session at a time, with an expiry so a finished session does not lock the daemon forever. Test the session-ID pattern against every ID format you actually see.
- **Use chain membership for labels, not for access control.** A default model may not be in the fallback chain at all. A guard that ignores every call from a model outside the chain will freeze the state file at the first such call.
- **Send directly.** A fixed two-line notice does not need an agent run. Post straight to your messaging service's API from the daemon: no model cost, and no dependence on the agent gateway being up.
- **Read credentials at run time** from a protected file. Never put the token in the script, and never execute the credentials file with shell `source`.

## Reading the log

Do **not** use a `tail -F` subprocess and read from its pipe. When `tail` writes to a pipe its output is block-buffered, so lines can sit in the buffer for minutes. `stdbuf -oL` did not reliably fix it for us. Read the file directly in a polling loop (`os.open`, `os.read`, `os.lseek` in Python, once a second), handle rotation, and process each complete line as it arrives.

## Running it

Run it as a user service that restarts on failure and survives logout:

```ini
[Unit]
Description=Model fallback notifier
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 %h/.hermes/scripts/model-fallback-notifier.py
Restart=always
RestartSec=5
Nice=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now model-fallback-notifier.service
loginctl show-user "$USER" | grep Linger     # must be yes to survive logout and reboot
```

## Test before you trust it

1. Run the state machine against a throwaway log and state file, with the messaging token blanked so sends become "would have sent" log lines.
2. Feed it realistic sequences: primary to fallback, further down, partly back, straight back to primary, and repeated calls on the same model, which must stay silent.
3. Check that the state file ends on the last model that actually answered.
4. Then send one real message through the same code path and confirm it arrived. A dry run proves the logic, not the delivery.

## Gotcha: running, but silent

The service shows as running, the log shows fresh model calls, and no alerts arrive. Compare the state file's last-seen time with the newest calls in the log. If it has stopped advancing, the usual causes are the chain-membership guard above, a session claim that never expires because its last-seen time is not refreshed, or a session-ID format the pattern does not match. Fix the cause before restarting, or the new process will lock up the same way.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
