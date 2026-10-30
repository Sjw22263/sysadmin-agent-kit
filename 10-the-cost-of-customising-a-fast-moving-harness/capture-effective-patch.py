#!/usr/bin/env python3
"""capture-effective-patch.py - TEMPLATE for capturing and checking local changes
to a harness checkout before an upgrade.

Part of "Guide for building an autonomous agentic system administrator", part 10.
Licensed under CC BY 4.0. Adapted from working documents developed by
Steve Waddington and Maxi Calder, his sysadmin agent.

This is a generalised starting point, not our production code. It runs its own
tests (`python3 capture-effective-patch.py self-test`) and nothing else has been
verified. It needs git and the Python standard library, nothing more.

Two commands, one for each mistake we made:

  capture REPO OUTPUT [--base REF]
      Write every tracked change in REPO, relative to REF (default HEAD), as one
      binary patch with full object IDs. Staged and unstaged changes are both
      included. Plain `git diff` shows only unstaged changes, and after a
      three-way apply most of your changes are staged: that is how we once
      "preserved" an almost empty patch. If REPO has untracked files the command
      refuses and lists them, leaving any earlier OUTPUT untouched. Decide about
      untracked files yourself; they are not in a diff.
      Use --base with the upstream commit your install is built on (for
      example `git merge-base HEAD <upstream-ref>`) when you also have local
      commits. Never diff a behind install against the latest upstream: that
      exports upstream's newer work as if it were a reversal.

  tree REPO
      Print the Git tree ID of REPO's working copy as it would be committed,
      tracked files only, using a throwaway index. Your index, files and
      branches are untouched; Git does add unreferenced objects to the
      repository's object store, which `git gc` later removes. Two checkouts
      with the same content give the same ID whatever their Git display
      settings. Compare this, not checksums of patch text: in October our upgrade
      rejected a correct result because Git abbreviated object IDs to eight
      characters in one repository and ten in the other, which changed the
      patch's checksum and nothing else.

Output is one JSON line. Exit codes: 0 success, 1 refused (untracked files),
2 usage or git failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


class GitError(RuntimeError):
    pass


def git(repo: Path, *args: str, env: dict[str, str] | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def untracked_files(repo: Path) -> list[str]:
    raw = git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    return [name.decode("utf-8", "replace") for name in raw.split(b"\0") if name]


def capture(repo: Path, output: Path, base: str = "HEAD") -> dict:
    repo = repo.resolve()
    output = output.resolve()
    if not (repo / ".git").exists():
        raise GitError(f"not a git checkout: {repo}")
    base_commit = git(repo, "rev-parse", "--verify", f"{base}^{{commit}}").decode().strip()
    untracked = untracked_files(repo)
    if untracked:
        return {"status": "refused", "reason": "untracked files are not in a diff", "untracked": untracked}

    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        # Diffing a commit against the working tree includes staged and
        # unstaged changes. --full-index makes the bytes independent of
        # core.abbrev and repository size.
        git(repo, "diff", base_commit, "--binary", "--full-index", f"--output={temporary}")
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)

    data = output.read_bytes()
    files = git(repo, "diff", base_commit, "--name-only", "-z").split(b"\0")
    return {
        "status": "captured",
        "base": base_commit,
        "patch": str(output),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "files": len([f for f in files if f]),
        "tree": effective_tree(repo),
    }


def effective_tree(repo: Path) -> str:
    """Tree ID of the tracked working copy, built in a throwaway index."""
    repo = repo.resolve()
    with tempfile.TemporaryDirectory() as scratch:
        env = dict(os.environ)
        env["GIT_INDEX_FILE"] = str(Path(scratch) / "index")
        git(repo, "read-tree", "HEAD", env=env)
        git(repo, "add", "--update", "--", ".", env=env)
        return git(repo, "write-tree", env=env).decode().strip()


# ---------------------------------------------------------------- self-test


def _sh(repo: Path, *args: str) -> bytes:
    return git(repo, *args)


def _new_repo(root: Path, name: str) -> Path:
    repo = root / name
    repo.mkdir()
    _sh(repo, "init", "-q")
    _sh(repo, "config", "user.email", "test@example.invalid")
    _sh(repo, "config", "user.name", "Test")
    _sh(repo, "config", "commit.gpgsign", "false")
    (repo / "a.txt").write_text("one\ntwo\nthree\n")
    (repo / "b.txt").write_text("alpha\n")
    (repo / "blob.bin").write_bytes(bytes(range(256)))
    _sh(repo, "add", ".")
    _sh(repo, "commit", "-q", "-m", "base")
    return repo


def _state(repo: Path) -> tuple[bytes, bytes]:
    return _sh(repo, "diff", "--cached", "--binary", "--full-index"), _sh(repo, "diff", "--binary", "--full-index")


def self_test() -> int:
    if shutil.which("git") is None:
        print("git is not installed", file=sys.stderr)
        return 2
    failures: list[str] = []

    def check(name: str, condition: bool) -> None:
        print(f"{'ok  ' if condition else 'FAIL'} {name}")
        if not condition:
            failures.append(name)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # 1. Staged-only change is captured (the August failure).
        repo = _new_repo(root, "staged")
        (repo / "a.txt").write_text("one\nTWO\nthree\n")
        _sh(repo, "add", "a.txt")
        out = root / "staged.patch"
        result = capture(repo, out)
        check("staged-only change captured", b"+TWO" in out.read_bytes())
        check("plain git diff would have missed it", _sh(repo, "diff") == b"")
        check("file count reported", result["files"] == 1)

        # 2. Unstaged-only and 3. combined.
        repo = _new_repo(root, "unstaged")
        (repo / "b.txt").write_text("beta\n")
        capture(repo, root / "unstaged.patch")
        check("unstaged-only change captured", b"+beta" in (root / "unstaged.patch").read_bytes())

        repo = _new_repo(root, "combined")
        (repo / "a.txt").write_text("one\nTWO\nthree\n")
        _sh(repo, "add", "a.txt")
        (repo / "b.txt").write_text("beta\n")
        (repo / "blob.bin").write_bytes(bytes(reversed(range(256))))
        before = _state(repo)
        out = root / "combined.patch"
        result = capture(repo, out)
        data = out.read_bytes()
        check("combined staged and unstaged captured", b"+TWO" in data and b"+beta" in data)
        check("binary change captured", b"GIT binary patch" in data)
        check("real index and working tree unchanged", _state(repo) == before)

        # 4. Round trip: the patch rebuilds the same effective tree on a clean copy.
        clean = root / "clean"
        subprocess.run(["git", "clone", "-q", str(repo), str(clean)], check=True)
        _sh(clean, "apply", "--3way", str(out))
        check("round trip reproduces effective tree", effective_tree(clean) == result["tree"])

        # 5. Abbreviation independence (the October failure).
        _sh(clean, "config", "core.abbrev", "12")
        _sh(repo, "config", "core.abbrev", "8")
        capture(clean, root / "clean.patch")
        same_bytes = (root / "clean.patch").read_bytes() == data
        check("patch bytes independent of core.abbrev", same_bytes)
        short_a = _sh(repo, "diff", "HEAD", "--binary")
        short_b = _sh(clean, "diff", "HEAD", "--binary")
        check("without --full-index the same change prints differently", short_a != short_b)
        check("tree ID equal across both checkouts", effective_tree(repo) == effective_tree(clean))

        # 6. Different content gives a different tree ID.
        (clean / "b.txt").write_text("gamma\n")
        check("changed content changes tree ID", effective_tree(clean) != effective_tree(repo))

        # 7. Untracked files refused; earlier output preserved.
        (repo / "new-file.txt").write_text("not tracked\n")
        refused = capture(repo, out)
        check("untracked file refused", refused["status"] == "refused" and "new-file.txt" in refused["untracked"])
        check("earlier patch left untouched", out.read_bytes() == data)
        (repo / "new-file.txt").unlink()

        # 8. --base: local commit plus working change, measured from upstream base.
        repo = _new_repo(root, "based")
        upstream = _sh(repo, "rev-parse", "HEAD").decode().strip()
        (repo / "a.txt").write_text("one\ncommitted\nthree\n")
        _sh(repo, "commit", "-q", "-am", "local commit")
        (repo / "b.txt").write_text("working\n")
        capture(repo, root / "based.patch", base=upstream)
        based = (root / "based.patch").read_bytes()
        check("--base includes local commits and working changes", b"+committed" in based and b"+working" in based)

    print(json.dumps({"self_test": "pass" if not failures else "fail", "failures": failures}))
    return 0 if not failures else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_capture = sub.add_parser("capture", help="write the effective patch")
    p_capture.add_argument("repo", type=Path)
    p_capture.add_argument("output", type=Path)
    p_capture.add_argument("--base", default="HEAD")
    p_tree = sub.add_parser("tree", help="print the effective tree ID")
    p_tree.add_argument("repo", type=Path)
    sub.add_parser("self-test", help="run the built-in tests")
    args = parser.parse_args(argv)

    try:
        if args.command == "self-test":
            return self_test()
        if args.command == "tree":
            print(json.dumps({"tree": effective_tree(args.repo)}))
            return 0
        result = capture(args.repo, args.output, args.base)
        print(json.dumps(result))
        return 0 if result["status"] == "captured" else 1
    except GitError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
