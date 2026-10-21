# Owning the maintenance: power failure and post-outage recovery

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Where to use this

Use this before your first power cut, not during it. It is a checklist for making servers come back on their own, telling the agent they came back, and checking what actually recovered. Go through it with your agent and record the result for each server.

## Two layers, firmware first

Recovery after a power failure happens in two layers:

1. **Firmware and hardware.** Does the machine switch itself back on when power returns?
2. **Operating system and services.** Do the system, its services, containers, the agent platform and scheduled jobs come back after it boots?

The second layer is irrelevant if the machine stays off. Check the first one first.

### Firmware

Look in the BIOS or UEFI settings for an option called something like *Restore on AC Power Loss*, *AC Power Recovery*, *After Power Failure*, *State After G3* or *Power On After Power Fail*. For a server, set it to *Power On* rather than *Last State*, unless you have a reason. Then test it with a controlled power interruption when that is safe.

Record the result per server. Some older boards do not have the option at all. One of ours does not, so it needs someone to switch it on after a power failure. That is a fact to write down, not a problem to discover during an outage.

> **Boot times are not evidence of automatic recovery.** After one of our outages, the boot times on both servers looked exactly like they had switched themselves back on. They had not: both had been switched on by hand. The agent's record of that event now says so, and treats automatic power-on as unverified until it is tested. If the agent infers firmware behaviour from boot times, it will tell you something comforting and wrong.

### Operating system and services

For each server, check and record:

- the services it provides are enabled to start at boot;
- services that need working connectivity at startup are ordered after it and actually wait for it. On systemd that means both `Wants=network-online.target` and `After=network-online.target`, with the matching wait-online implementation enabled; `After=` alone is ordering and does not ask for the target at all. Note also that network-online does not prove any particular remote endpoint is reachable, so a service that depends on a remote host still needs its own retry. Do not add this dependency to every network service by reflex: it delays boot. See <https://systemd.io/NETWORK_ONLINE/>. Set services to restart on failure where appropriate;
- user-level services (an agent platform running as a normal user is common) start at boot without anyone logging in. On systemd that needs lingering enabled for the user (`loginctl enable-linger <user>`);
- the server boots from the right disk. A machine with an old operating system on a second disk can come back up on the wrong one, with a different address and different host keys, and every check will fail.

## Tell the agent the machine rebooted

- A small boot-time service on the agent's host that sends one message per boot, with the hostname and boot time. It must not depend on the agent platform already running, and it must not treat a failed send as fatal: after a power cut the router may still be starting.
- For other servers, a check on the agent's host that notices a changed boot ID and then validates what that server provides: services active, websites answering over HTTPS with valid certificates, mail ports accepting connections. A failed or inconclusive check is urgent: alert, wake the agent to repair, then check again.
- A Hermes cron job cannot be your boot alert for the agent's own host, because it only runs once Hermes is running. Use it for the follow-up checks.

## Post-outage check

A script that gathers the facts, with no side effects:

1. boot time, uptime, load, memory and disk for each host;
2. each expected service and listening port;
3. scheduled jobs on both the system scheduler and the agent's scheduler;
4. backup logs, and which jobs fell inside the outage window.

Then the agent compares the outage window with the schedules. A job scheduled while the machine was down was not necessarily skipped: check whether that scheduler catches up after boot, then check the run record and the artefact before calling the run missed, delayed or failed. Report the next run and whether a catch-up is needed. It is only data loss if the expected data is missing and cannot be regenerated.

## What the agent may restore without asking

Decide this in advance and write it down. A deliberately conservative starting point, to settle against your own mandate:

- **May do after confirming the exact failure:** restart a known service that has failed (web server, mail services, file sharing, the agent platform's own services).
- **Needs a decision first:** firewall changes, DNS changes, certificate reissue, database repair, deleting queues, logs, mail, backups or user data, and broad configuration edits.

Separate the two questions. Some work that belongs on the second list in a post-outage context already has standing authority as routine maintenance: ordinary package upgrades and a controlled maintenance-window reboot are examples in our estate, authorised by the routine-maintenance policy in `routine-system-administration.md` rather than by a fresh decision each time. What needs a new human decision is work outside that standing authority, or work whose cost of being wrong is large. Write down which of yours is which, in one place, and keep that record current: a stale restriction in one runbook and a broader permission in a live job is a governance problem waiting for an outage.

The second list is not a judgement on the agent. It is the list of things where you would also want a human administrator to check with you.

## Report

```text
Power event recovery check complete.

Recovered:
- <host/service>: <evidence>

Everything is OK, except:
- <broken item>
  Evidence: <observed fact>
  Tried: <repair attempted or "none">
  Fix: <next repair path>
  Needed from you: <action or "none">
```

If everything recovered: `Power event recovery check complete. Everything is OK.`

## A related warning: power-path faults are not host faults

Two unclean shutdowns within eight days look like an unstable server. Check the evidence before buying hardware or adding a watchdog. In our case the logs showed no crash, no memory or disk errors, and a second server on the same network stayed up while its links to the agent's host and to the router dropped within seconds of each other. That pointed to the power path serving the agent's host and the router, not to the operating system, although a failing power adapter could not be ruled out. A watchdog that reboots a hung system does nothing for a machine that has lost power. Check the outlet, the power board and what else shares it, and consider a UPS for the agent's host and the router.
