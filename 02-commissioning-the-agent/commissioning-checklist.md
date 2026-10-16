# Commissioning checklist: from brief to a job that runs

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Where to use this

Use it after the agent has evaluated its first brief (see `01-giving-the-agent-a-job/brief-template.md`) and before you schedule anything.

Commissioning is finished when six things are true:

1. the scope and repair boundary are agreed in writing;
2. the agent's access has been proven, not assumed;
3. the agent has inventoried the systems it is responsible for;
4. it has made one real repair, under your explicit instruction, and verified it;
5. you have received a report from it;
6. the job is scheduled, and the schedule has been read back.

Ours took a single working session. Most of the time went on the things below that were not as they seemed.

## 1. Scope

- Answer the questions the agent raised when it evaluated the brief. Write the answers down where the agent will find them again, not only in the chat.
- Write down what "trivial" means for an unattended job: which services, by exact name, it may restart, and what it must never do unattended (see the brief template).
- Name the channels: one for the routine report, one for urgent problems.

## 2. Give the agent its own identity and accounts

Create accounts for the agent under the agent's name, not the harness's. Our agent runs under a Unix account named after the harness on its own server, but every account created for it elsewhere is named for the agent. As I put it at the time: "I use Maxi as your identity rather than hermes, so accounts I create for you will be maxi@ or maxi-[function] etc." The agent's reply was: "“Hermes” is the runtime, framework, and sometimes the Unix account this process happens to run under ... It is not my identity."

A dedicated account also means the remote system's logs show which actions were the agent's, and its access can be removed without touching anyone else's.

Credentials never go into prompts, skills, runbooks, chat or email. The agent's scripts read them at run time from a protected file.

## 3. Prove access

- Create a dedicated SSH key for the agent.
- Add remote host keys deliberately: scan them, check the fingerprints, then add them. Do not let the first connection accept whatever it is offered.
- Test the login non-interactively, with an explicit user:

  ```bash
  ssh -o BatchMode=yes -o ConnectTimeout=5 agent@host 'hostname; id; sudo -n true && echo sudo_ok || echo sudo_failed'
  ```

- Use `sudo -n` in automation, so a job fails immediately instead of hanging on a password prompt.

**Gotchas we hit:**

- **A blocked approval prompt is not proof that `sudo` is missing.** Check with `sudo -n true` before concluding the agent lacks rights.
- **Always write `user@host`.** `ssh host` uses the local username. If that user does not exist on the remote machine you get `Permission denied (publickey)`, which looks exactly like a lost key. This gave us a false "access lost" alert.
- **Reuse one SSH connection per run if the remote firewall rate-limits SSH.** Our health script opened a new connection for every check. The firewall started blocking it partway through, and a blocked check looked like a stopped service. The fix is connection sharing, not a weaker firewall and not `sleep` between checks:

  ```bash
  ssh -o ControlMaster=auto -o ControlPath=~/.cache/health-%C -o ControlPersist=120 agent@host ...
  ```

- **A Docker socket permission error is not fatal** if `sudo -n docker ...` works. Use that in automation.

## 4. Discovery, read-only

Ask the agent to inventory what it is responsible for before it changes anything: hosts, services by exact name, listening ports, scheduled jobs, and where each service actually runs. Expect it to find things that are already broken. Ours found that the file-sharing service on the web server had failed at boot.

**Gotchas:**

- **Public addresses may not match the internal network.** With address translation, checks from the agent's server to our mail server's ports looked closed while the mail services were running normally. We moved the mail checks onto the mail server itself (service state, plus a local TLS test using the public certificate name) and used the daily report email as the real outbound delivery test.
- **A ping proves only that the machine answers pings.** It is not a health check.
- **Do not assume a health endpoint.** `/health`, `/status` and `/ping` are conventions, not standards. Find the real one in the service's documentation. A 404 from a path you guessed is a fault in the check, not in the service. If there is no documented endpoint, make one small real request instead.

## 5. One real repair, under explicit instruction

When discovery finds something broken, let the agent diagnose it, then tell it to fix it. Ours had found the failed file-sharing service and stopped. The service was set to listen only on one network address and started before that address existed at boot. Once I told it to go ahead, the agent made the service wait for the network to come up and restart if it failed, then limited its firewall rules to the local network.

Verify the repair at the level a user would notice: the service is active and enabled, it is listening, and the thing that depends on it works. After a repair like this, restarting that named service can join the list of trivial repairs the daily job may do on its own.

## 6. A report you have received

Run the job by hand first. It is working when the report is in your inbox, not when the agent says it has sent it.

## 7. Schedule it, then read the schedule back

- **Hermes cron scripts must be under `~/.hermes/scripts/`** (strictly, the `scripts` folder in the active Hermes home). The scheduler refuses a script that resolves outside it. Our first attempt to schedule the health check failed for exactly this reason.
- **Check that the job repeats.** Our first scheduled mail check was created to run once. The corrected schedule still showed it running once. Read back the job definition and confirm both the repeat setting and the next run time.
- **Hermes cron expressions use the scheduler's local time.** If the server is on your time zone, 6 am is `0 6 * * *`. Do not convert it to UTC. Check the next run time the scheduler reports.
- **Start with a script-only job** (`--no-agent`). The script is the whole job and no model runs. Empty output is a silent run; any output is delivered as written; a non-zero exit is reported as a failure. See `morning-health-check-job.md`.

  > **Before you change the mode.** If you later attach the same script to an ordinary (agent) job, the rules invert: empty output wakes the agent. Only a final output line that is a JSON object containing `"wakeAgent": false`, such as `{"wakeAgent": false}`, stops it. Part 3 covers this.

```bash
hermes cron list          # read back the job, its schedule, repeat and next run
hermes cron run <job-id>  # run it once on the next scheduler tick
```

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
