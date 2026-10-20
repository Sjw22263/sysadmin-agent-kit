# Watching the estate: health monitoring, safe repair and reporting

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Where to use this

Use this once the script-only morning check from part 2 is running and its report reaches you. It adds continuous watching between mornings, and an agent that responds when the scripts find something they cannot fix.

## The loop

Monitoring is not "ping something". It is a loop:

1. collect objective health facts;
2. classify failures by severity;
3. repair only within the authority of whatever is doing the repair;
4. escalate serious problems quickly;
5. report concisely, and say nothing extra when everything is fine.

## Principles

- **Scripts measure, the model judges.** A script checks the same things the same way every time and costs nothing. Wake the model only when there is something to judge or repair.
- **Keep checks and repairs separate.** A script may observe broadly but repairs only what is on its explicit allow-list. A responder agent repairs under its mandate and the job's own limits. A review job that is proposal-only never repairs, whatever skills it has loaded.
- **The monitoring boundary is not the agent's to move.** If a dependency the monitor exists to watch is failing, that failure is the incident. Removing the check so the monitor goes green hides it. Narrow the scope only when the dependency is shown to be optional, and write that down.
- **Keep the normal report boring.** If everything is fine, say exactly that.
- **Escalate serious problems on the fastest channel you have.**

## Three jobs, three cadences

This is our current arrangement, generalised.

### 1. The morning report (daily)

The script runs every check. If everything is healthy, the script sends the report itself and tells the scheduler not to wake the agent: no model runs. If a fault remains after the script's own allow-listed repairs, the script **withholds** the report and wakes a responder agent. The responder investigates and repairs under its mandate, then runs the original script once more in a final-report mode, which sends the report whether the fault is fixed or has reached a genuine blocker.

The result is that the morning report says one of three things: everything is OK; something was broken and this is what was done about it; or something is broken and this is what is needed from you.

### 2. The watchdog (every five minutes)

A deterministic script checks network paths, key services, public websites with certificate validation, and mail TLS. A healthy tick wakes nothing and sends nothing. A confirmed fault wakes the responder. "Confirmed" is the important word: see the gating rules below.

### 3. The review of scheduled jobs (twice daily)

A proposal-only agent job reviews the previous period's job failures, scheduler state and runtime warnings. It does not repair. A material problem becomes a handoff to the agent that owns it. This is a retrospective control, not immediate response; do not describe it as either more or less than that.

> **Gotcha.** Job output files often contain the job's whole prompt as well as its result. Searching them for "error" or "failure" finds the instructions and historical examples. Read only the response section of agent jobs, and only real output or an explicit failed status for script jobs.

## Gating: check twice before you wake anyone

Our watchdog's rules, which answer the question "does it wake on one failure or several?":

1. **Every failed check is repeated immediately** before it can change anything. If the repeat passes, the event is silent and counts for nothing.
2. **Soft failures**, such as one website or one mail check, must fail both the scheduled check and the immediate repeat on **three consecutive ticks** before the agent wakes. At a five-minute cadence that is about ten minutes.
3. **Severe failures wake immediately** once confirmed: a network interface down or misconfigured, a core service stopped, the checker itself crashing, or failures in two independent areas at once (web and mail, say).
4. **Counters are per check** and reset individually on recovery. One check recovering must not clear another's count.
5. **The bare domain and `www` for the same site count as one failure**, not two.
6. **Identical repeated alerts are suppressed for 30 minutes**, then repeated, so a persistent fault is neither a storm nor silence.

> **Gotcha: a crashed checker can look like a recovery.** If the immediate repeat is filtered down to "the checks that failed the first time", a repeat that crashes reports a result under a different name, gets filtered out, and leaves an empty list of failures. The gate then concludes that the fault cleared. Always let checker-exception results through the filter.

Keep the gate a pure function of the results, the repeat results and the time, so you can test it with made-up results instead of live probes. `watchdog-gate.py` is a small template of this, with tests.

## Classify before you repair

A responder that repairs every symptom will eventually interrupt real work. Ours restarted a wireless network adapter during a large legitimate file transfer by another of my agents. The link showed high latency with zero packet loss: busy, not broken.

The watchdog now measures traffic on that link. High latency with zero packet loss while significant traffic is flowing, and a healthy wired path, is classed as busy and not repaired. Our first threshold was too high and missed a 4.25 Mbps transfer, so we lowered it to 1 Mbps. Later, a heavier transfer made public websites load slowly from inside the network while they were fine from outside; slow but successful responses during an established busy period are no longer failures.

What is **never** suppressed: packet loss, interface or address problems, a degraded wired path, stopped services, mail failures, and HTTP or certificate failures.

Work out what your own systems look like when they are busy and healthy, and write it into the classification before you give a responder repair authority.

## Repaired, recovered, or still broken

Report these three differently:

- **Repaired:** something was done and the original check now passes. One line: `fixed <fault>`.
- **Recovered by itself:** the fault cleared before anything was done. Say nothing. Nobody needs a notification for this.
- **Still broken:** what remains, what was tried, the current risk, and exactly what is needed.

Never call a spontaneous recovery "fixed". It claims work that was not done, and it teaches you to trust a signal that is not reliable. Re-run the failing check before deciding what made it pass.

## Pitfalls

- **Checking your public websites from inside your own network** cannot tell an address-translation quirk from a real outage. Use an external observer for public reachability, and treat partial or unavailable results from it as inconclusive, not as "down".
- **Investigating a problem the script already fixed.** Read the whole report first. A self-fixed problem is not a current one.
- **Treating an old error as current.** Check the job's present state before investigating a past notification.
- **"Lost carrier" in the logs does not prove a cable was pulled.** An administrative `ip link set ... down` writes the same messages. Check the interface's administrative state before calling the hardware faulty.
- **A responder should not depend on the thing it may need to repair.** If a job's working directory or scripts live on network storage, a network fault can stop the responder that would fix it. Use local paths for health-critical jobs.
- **The external check is a dependency too.** Ours once woke the responder because the observer service answered slower than our script waited. The responder found that the fault was in our checker, fixed the polling, and sent the report. Monitoring code needs maintenance like anything else.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
