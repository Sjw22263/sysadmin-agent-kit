#!/usr/bin/env python3
"""watchdog-gate.py - TEMPLATE for a testable watchdog alert gate.

Part of "Guide for building an autonomous agentic system administrator", part 3.
Licensed under CC BY 4.0. Adapted from working documents developed by
Steve Waddington and Maxi Calder, his sysadmin agent.

Version: revised 23 October 2026. Hermes wake-gate behaviour checked against
Hermes Agent upstream commit e1fdf003 (5 October 2026).

This is a generalised starting point, not our production watchdog. It runs its
own tests (`python3 watchdog-gate.py --self-test`) and nothing else has been
verified. Write your probes with your agent; keep the gate a pure function.

Until you wire in probes, running it reports UNCONFIGURED and wakes the agent,
so a scheduled copy that nobody finished can never look healthy. Use `--demo`
to see the healthy skip output. Earlier versions printed "healthy" when
unconfigured; if you copied one, replace it.

You must persist State between runs (a small JSON file is enough) and stop two
runs overlapping (for example with a lock file), or the consecutive-failure
counts and alert suppression will not work.

Rules implemented (see server-health-monitoring.md):
  1. A failed scheduled check only counts if the immediate repeat also fails.
  2. Soft failures wake the agent after SOFT_FAILURES_TO_WAKE consecutive ticks.
  3. Severe failures wake immediately once confirmed.
  4. Counters are per failure domain and reset individually on recovery.
  5. Apex and www checks for one site share a failure domain.
  6. Identical alerts are suppressed for ALERT_REPEAT_SECONDS.
  7. A crashed checker is never mistaken for a recovery.
  8. A failed check with no repeat result is UNKNOWN, treated as a confirmed
     failure, never as a recovery.

The script prints one JSON line. With a Hermes agent-mode cron job, a JSON
object containing "wakeAgent": false on the last line skips the model run.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field

SOFT_FAILURES_TO_WAKE = 3
ALERT_REPEAT_SECONDS = 30 * 60
PROBE_EXCEPTION = "watchdog:probe-exception"


@dataclass(frozen=True)
class Result:
    name: str              # e.g. "web:www.example.com", "service:postfix"
    ok: bool
    severe: bool = False   # interface down, core service stopped, ...
    area: str = ""         # independent area, e.g. "web", "mail", "network"
    detail: str = ""


@dataclass
class State:
    failure_counts: dict[str, int] = field(default_factory=dict)
    last_alert: dict = field(default_factory=dict)   # {"fingerprint": str, "at": float}


def domain(name: str) -> str:
    """Apex and www for the same site are one failure domain."""
    kind, _, target = name.partition(":")
    if kind == "web" and target.startswith("www."):
        target = target[4:]
    return f"{kind}:{target}"


def gate(scheduled: list[Result], repeat: list[Result], state: State, now: float) -> tuple[dict, State]:
    """Pure decision function. No probes, no I/O."""
    failed_names = {r.name for r in scheduled if not r.ok}
    # Only failures confirmed by the immediate repeat count. Let a crashed
    # repeat probe through: it never appears in failed_names, and dropping it
    # would make a broken checker look like a recovery.
    confirmed = [r for r in repeat if not r.ok and (r.name in failed_names or r.name == PROBE_EXCEPTION)]
    # A scheduled failure whose repeat result is simply missing is UNKNOWN.
    # Absence of evidence is not a recovery, so count it as confirmed.
    repeated_names = {r.name for r in repeat}
    confirmed += [Result(r.name, False, r.severe, r.area,
                         (r.detail + "; " if r.detail else "") + "UNKNOWN: repeat probe missing")
                  for r in scheduled
                  if not r.ok and r.name != PROBE_EXCEPTION and r.name not in repeated_names]
    if any(r.name == PROBE_EXCEPTION for r in scheduled if not r.ok):
        confirmed += [r for r in scheduled if r.name == PROBE_EXCEPTION and r not in confirmed]

    counts = dict(state.failure_counts)
    confirmed_domains = {domain(r.name) for r in confirmed}
    for d in list(counts):
        if d not in confirmed_domains:
            del counts[d]                      # per-domain reset on recovery
    for d in confirmed_domains:
        counts[d] = counts.get(d, 0) + 1

    areas = {r.area for r in confirmed if r.area}
    severe = [r for r in confirmed if r.severe or r.name == PROBE_EXCEPTION]
    soft_due = [d for d in confirmed_domains if counts[d] >= SOFT_FAILURES_TO_WAKE]

    if severe:
        reason = "severe"
    elif len(areas) >= 2:
        reason = "correlated"
    elif soft_due:
        reason = "soft-threshold"
    else:
        reason = ""

    wake = bool(reason)
    last_alert = dict(state.last_alert)
    if wake:
        fingerprint = "|".join(sorted(confirmed_domains))
        recent = (last_alert.get("fingerprint") == fingerprint
                  and now - last_alert.get("at", 0) < ALERT_REPEAT_SECONDS)
        if recent:
            wake, reason = False, "suppressed-repeat"
        else:
            last_alert = {"fingerprint": fingerprint, "at": now}
    elif not confirmed:
        last_alert = {}

    payload = {
        "wakeAgent": wake,
        "status": "healthy" if not confirmed else "degraded",
        "reason": reason,
        "issues": [f"{r.name}: {r.detail}".rstrip(": ") for r in confirmed],
        "failure_counts": counts,
    }
    return payload, State(failure_counts=counts, last_alert=last_alert)


def unconfigured_payload() -> dict:
    """What an unfinished copy reports: never healthy, always wakes."""
    return {"wakeAgent": True, "status": "unconfigured", "reason": "unconfigured",
            "issues": ["watchdog-gate.py has no probes wired in; nothing was checked"],
            "failure_counts": {}}


# ---------------------------------------------------------------- self-test
def _self_test() -> int:
    import unittest

    ok = lambda n, **k: Result(n, True, **k)          # noqa: E731
    bad = lambda n, **k: Result(n, False, **k)        # noqa: E731

    class GateTests(unittest.TestCase):
        def test_healthy_is_silent(self):
            p, _ = gate([ok("web:example.com")], [], State(), 0)
            self.assertFalse(p["wakeAgent"])
            self.assertEqual(p["status"], "healthy")

        def test_transient_failure_cleared_by_repeat_does_not_count(self):
            p, s = gate([bad("web:example.com", area="web")], [ok("web:example.com")], State(), 0)
            self.assertFalse(p["wakeAgent"])
            self.assertEqual(s.failure_counts, {})

        def test_soft_failure_wakes_on_third_consecutive_tick(self):
            s = State()
            for tick in range(3):
                p, s = gate([bad("web:example.com", area="web")], [bad("web:example.com", area="web")], s, tick * 300)
            self.assertTrue(p["wakeAgent"])
            self.assertEqual(p["reason"], "soft-threshold")

        def test_apex_and_www_are_one_domain(self):
            r = [bad("web:example.com", area="web"), bad("web:www.example.com", area="web")]
            p, s = gate(r, r, State(), 0)
            self.assertEqual(s.failure_counts, {"web:example.com": 1})
            self.assertFalse(p["wakeAgent"])

        def test_severe_wakes_immediately(self):
            r = [bad("service:postfix", severe=True, area="mail")]
            p, _ = gate(r, r, State(), 0)
            self.assertTrue(p["wakeAgent"])
            self.assertEqual(p["reason"], "severe")

        def test_two_independent_areas_wake_immediately(self):
            r = [bad("web:example.com", area="web"), bad("mail:imap", area="mail")]
            p, _ = gate(r, r, State(), 0)
            self.assertEqual(p["reason"], "correlated")

        def test_crashed_repeat_is_not_a_recovery(self):
            p, _ = gate([bad("web:example.com", area="web")], [bad(PROBE_EXCEPTION, detail="timeout")], State(), 0)
            self.assertTrue(p["wakeAgent"])
            self.assertEqual(p["status"], "degraded")

        def test_missing_repeat_is_unknown_not_recovery(self):
            p, s = gate([bad("web:example.com", area="web")], [], State(), 0)
            self.assertEqual(p["status"], "degraded")
            self.assertEqual(s.failure_counts, {"web:example.com": 1})
            self.assertIn("UNKNOWN", p["issues"][0])

        def test_unconfigured_run_wakes(self):
            p = unconfigured_payload()
            self.assertTrue(p["wakeAgent"])
            self.assertEqual(p["status"], "unconfigured")

        def test_recovery_resets_only_that_counter(self):
            s = State(failure_counts={"web:example.com": 2, "mail:imap": 2})
            r = [bad("mail:imap", area="mail")]
            _, s = gate(r, r, s, 0)
            self.assertEqual(s.failure_counts, {"mail:imap": 3})

        def test_identical_alert_suppressed_then_repeated(self):
            r = [bad("service:postfix", severe=True, area="mail")]
            p1, s = gate(r, r, State(), 0)
            p2, s = gate(r, r, s, 600)
            p3, s = gate(r, r, s, 600 + ALERT_REPEAT_SECONDS)
            self.assertEqual([p1["wakeAgent"], p2["wakeAgent"], p3["wakeAgent"]], [True, False, True])

    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(GateTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    if "--demo" in sys.argv:
        # Demonstration only: shows the healthy skip output.
        payload, _ = gate([], [], State(), 0)
        print(json.dumps(payload, sort_keys=True))
        sys.exit(0)
    # Replace this with your probes, state load/save and lock. Until then an
    # unfinished copy reports UNCONFIGURED, wakes the agent and exits non-zero.
    print(json.dumps(unconfigured_payload(), sort_keys=True))
    sys.exit(2)
