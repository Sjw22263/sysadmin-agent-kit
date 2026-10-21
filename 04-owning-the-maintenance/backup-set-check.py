#!/usr/bin/env python3
"""backup-set-check.py - TEMPLATE for a daily check of a set of backup archives.

Part of "Guide for building an autonomous agentic system administrator", part 4.
Licensed under CC BY 4.0. Adapted from working documents developed by
Steve Waddington and Maxi Calder, his sysadmin agent.

This is a generalised starting point, not our production code. It runs its own
tests (`python3 backup-set-check.py --self-test`) and nothing else has been
verified. It checks that backups exist and are intact. It does not prove they
can be restored: do real restore tests as well (see backups.md).

Checks, for one directory of archives with sha256sum-style sidecar files:
  1. The destination is a mount point, if --require-mount is given.
  2. Every archive has a checksum file and every checksum file has an archive.
     A half-present pair is reported, never repaired.
  3. Each checksum file names its own archive, and the archive matches it.
  4. The newest archive is younger than --max-age-hours.
  5. At least --min-generations archives exist. An empty set is never healthy.
  6. A crash in the checker itself is reported as a problem, never as healthy.

Output is one JSON line. Healthy: {"wakeAgent": false}. Problems:
{"wakeAgent": true, "issues": [...]}. With a Hermes agent-mode cron job, the
healthy line skips the model run and anything else wakes the agent.
Exit codes: 0 when the check ran (healthy or not), 2 when the checker failed.
With --exit-code, problems also exit 1, for use under the system scheduler.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

SIDECAR_SUFFIX = ".sha256"


def sha256_of(path: Path, chunk: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


def read_sidecar(path: Path) -> tuple[str, str]:
    """Return (hex digest, file name) from a `sha256sum` line: '<hex>  <name>'."""
    text = path.read_text(encoding="utf-8").strip()
    if not text or len(text.splitlines()) != 1:
        raise ValueError("expected exactly one line")
    digest, _, name = text.partition(" ")
    name = name.lstrip(" *")
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest.lower()):
        raise ValueError("first field is not a SHA-256 digest")
    if not name:
        raise ValueError("no file name")
    return digest.lower(), Path(name).name


def check_backup_set(
    directory: Path,
    pattern: str,
    max_age_hours: float,
    min_generations: int,
    require_mount: Path | None = None,
    verify_hashes: bool = True,
    now: float | None = None,
) -> list[str]:
    issues: list[str] = []
    now = time.time() if now is None else now

    if require_mount is not None and not os.path.ismount(require_mount):
        return [f"not-mounted: {require_mount} is not a mount point"]
    if not directory.is_dir():
        return [f"missing-directory: {directory}"]

    archives = {p.name: p for p in directory.glob(pattern)
                if p.is_file() and not p.name.endswith(SIDECAR_SUFFIX)}
    sidecars = {p.name[: -len(SIDECAR_SUFFIX)]: p
                for p in directory.glob(pattern + SIDECAR_SUFFIX) if p.is_file()}

    for name in sorted(set(archives) - set(sidecars)):
        issues.append(f"half-present: {name} has no checksum file")
    for name in sorted(set(sidecars) - set(archives)):
        issues.append(f"half-present: checksum file for {name} has no archive")

    for name in sorted(set(archives) & set(sidecars)):
        try:
            expected, named = read_sidecar(sidecars[name])
        except (OSError, ValueError, UnicodeDecodeError) as exc:
            issues.append(f"bad-checksum-file: {name}: {exc}")
            continue
        if named != name:
            issues.append(f"checksum-names-other-file: {name} sidecar names {named}")
            continue
        if verify_hashes and sha256_of(archives[name]) != expected:
            issues.append(f"checksum-mismatch: {name}")

    if not archives:
        issues.append(f"no-archives: nothing matching {pattern} in {directory}")
    elif len(archives) < min_generations:
        issues.append(f"too-few-generations: {len(archives)} found, {min_generations} required")
    if archives:
        newest = max(p.stat().st_mtime for p in archives.values())
        age_hours = (now - newest) / 3600
        if age_hours > max_age_hours:
            issues.append(f"stale: newest archive is {age_hours:.1f}h old (limit {max_age_hours}h)")
    return issues


def emit(issues: list[str]) -> str:
    if not issues:
        return json.dumps({"wakeAgent": False})
    return json.dumps({"wakeAgent": True, "issues": issues})


def self_test() -> int:
    import tempfile

    def make(d: Path, name: str, data: bytes, sidecar: bool = True, age_h: float = 1) -> Path:
        p = d / name
        p.write_bytes(data)
        if sidecar:
            (d / (name + SIDECAR_SUFFIX)).write_text(
                f"{hashlib.sha256(data).hexdigest()}  {name}\n", encoding="utf-8")
        t = time.time() - age_h * 3600
        os.utime(p, (t, t))
        return p

    def run(d: Path, **kw) -> list[str]:
        args = dict(pattern="*.tar.zst", max_age_hours=30, min_generations=2)
        args.update(kw)
        return check_backup_set(d, **args)

    failures = 0

    def expect(label: str, cond: bool) -> None:
        nonlocal failures
        print(("ok   " if cond else "FAIL ") + label)
        failures += 0 if cond else 1

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)

        d = base / "healthy"; d.mkdir()
        make(d, "site-2026-10-19.tar.zst", b"one", age_h=25)
        make(d, "site-2026-10-20.tar.zst", b"two", age_h=1)
        expect("healthy set emits wakeAgent false", emit(run(d)) == '{"wakeAgent": false}')

        d = base / "half"; d.mkdir()
        make(d, "a-2026-10-20.tar.zst", b"a")
        make(d, "b-2026-10-20.tar.zst", b"b", sidecar=False)
        (d / "c-2026-10-19.tar.zst.sha256").write_text("0" * 64 + "  c-2026-10-19.tar.zst\n")
        issues = run(d)
        expect("archive without checksum is reported", any("b-2026-10-20" in i and "half-present" in i for i in issues))
        expect("checksum without archive is reported", any("c-2026-10-19" in i and "half-present" in i for i in issues))

        d = base / "corrupt"; d.mkdir()
        make(d, "x-2026-10-19.tar.zst", b"good", age_h=25)
        p = make(d, "x-2026-10-20.tar.zst", b"good2")
        p.write_bytes(b"bad!!")
        expect("corrupted retained archive is reported", any(i.startswith("checksum-mismatch") for i in run(d)))
        expect("--no-hash skips content verification", not any(i.startswith("checksum-mismatch") for i in run(d, verify_hashes=False)))

        d = base / "stale"; d.mkdir()
        make(d, "s-2026-10-17.tar.zst", b"1", age_h=80)
        make(d, "s-2026-10-18.tar.zst", b"2", age_h=50)
        expect("stale newest archive is reported", any(i.startswith("stale") for i in run(d)))

        d = base / "few"; d.mkdir()
        make(d, "f-2026-10-20.tar.zst", b"1")
        expect("too few generations is reported", any(i.startswith("too-few-generations") for i in run(d)))

        d = base / "empty"; d.mkdir()
        expect("empty set is never healthy, even with --min-generations 0",
               any(i.startswith("no-archives") for i in run(d, min_generations=0)))

        d = base / "misnamed"; d.mkdir()
        make(d, "m-2026-10-19.tar.zst", b"1", age_h=20)
        make(d, "m-2026-10-20.tar.zst", b"2")
        (d / "m-2026-10-20.tar.zst.sha256").write_text(hashlib.sha256(b"2").hexdigest() + "  other.tar.zst\n")
        expect("checksum naming another file is reported", any(i.startswith("checksum-names-other-file") for i in run(d)))

        d = base / "garbage"; d.mkdir()
        make(d, "g-2026-10-19.tar.zst", b"1", age_h=20)
        make(d, "g-2026-10-20.tar.zst", b"2")
        (d / "g-2026-10-20.tar.zst.sha256").write_text("not a checksum\n")
        expect("malformed checksum file is reported", any(i.startswith("bad-checksum-file") for i in run(d)))

        expect("missing directory is reported", run(base / "nope") != [])
        expect("unmounted destination is reported",
               any(i.startswith("not-mounted") for i in run(base / "healthy", require_mount=base / "healthy")))

        out = main_guarded(["--dir", str(base / "nope-crash"), "--max-age-hours", "not-a-number"], capture=True)
        expect("checker crash wakes the agent and exits 2",
               out[0] == 2 and json.loads(out[1])["wakeAgent"] is True)

    print(f"{'all tests passed' if not failures else f'{failures} test(s) failed'}")
    return 1 if failures else 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dir", type=Path, required=True, help="directory holding the archives")
    parser.add_argument("--pattern", default="*.tar.zst", help="archive glob (default: *.tar.zst)")
    parser.add_argument("--max-age-hours", type=float, default=30.0)
    parser.add_argument("--min-generations", type=int, default=1)
    parser.add_argument("--require-mount", type=Path, help="fail unless this path is a mount point")
    parser.add_argument("--no-hash", action="store_true", help="skip content hashing (presence and age only)")
    parser.add_argument("--exit-code", action="store_true", help="exit 1 when problems are found")
    return parser.parse_args(argv)


def main_guarded(argv: list[str], capture: bool = False):
    """Run the check. Any failure of the checker itself is reported, never hidden."""
    try:
        args = parse_args(argv)
        issues = check_backup_set(
            args.dir, args.pattern, args.max_age_hours, args.min_generations,
            args.require_mount, not args.no_hash)
        line, code = emit(issues), (1 if issues and args.exit_code else 0)
    except BaseException as exc:  # includes argparse's SystemExit: a misconfigured check is a fault
        if isinstance(exc, KeyboardInterrupt):
            raise
        line = json.dumps({"wakeAgent": True,
                           "issues": [f"checker-error: {type(exc).__name__}: {exc}"]})
        code = 2
    if capture:
        return code, line
    print(line)
    return code


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    sys.exit(main_guarded(sys.argv[1:]))
