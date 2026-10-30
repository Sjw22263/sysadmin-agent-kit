# Reconciling local changes with a harness upgrade

> Checked on 30 October 2026 against Hermes Agent v0.22.5 (upstream commit `bf0203a7`, 22 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

Use this before every upgrade of a harness checkout you have changed locally. It is the preparation half; `guarded-update-routine.md` is the cutover. Keep the list of what you changed, and why, in `local-change-register.md`.

If you have never edited the harness's own files, and your customisation lives only in configuration, skills, identity files and plugins, most of this does not apply. Read the configuration migration step anyway.

## The acceptance test

The one thing an upgrade must prove is this: every local change you made to the harness is either still present and still working, or has been deliberately retired because upstream now does the job. Everything else in this file serves that test. As Steve put it to the sysadmin agent after six hours of checks on a single upgrade: "The only thing you really need to do for a Hermes update is make sure the custom changes made to Hermes files are preserved, or, if superseded, retired."

Proportion matters as much as rigour. A single-operator estate is not a 24x7 service; if the upgrade breaks something, you can fix it or roll it back. Put effort into the checks that catch lost changes and into a rollback that works, not into simulating every possible interaction.

## 1. Know exactly what is installed and what you are moving to

- Installed commit and version, read from the checkout, not from memory or an old report.
- The target: a published stable release, pinned to its exact commit. The tip of the main branch can be well ahead of the last stable release.
- What your updater would actually select. In our October upgrade the installed updater resolved a different stable release from the one we had pinned. Check this rather than assuming the updater and the release page agree.

A version banner is not an inventory. Ours reports "Up to date" on a checkout carrying 47 modified files: it says nothing about local changes. On Hermes's main update channel the banner can also show a "carried commits" count; that is upstream history beyond an older cached reference, not changes you wrote. Ours once showed 4,787 when the true figure was zero local commits.

## 2. Inventory the net local divergence

Measure from the upstream commit your install is built on, through the working tree:

```bash
base=$(git -C "$repo" merge-base HEAD "$upstream_ref")   # or HEAD if you have no local commits
git -C "$repo" diff "$base" --binary --full-index > local-effective.patch
git -C "$repo" ls-files --others --exclude-standard     # untracked files, which no diff contains
```

`capture-effective-patch.py capture` does the same and refuses if untracked files exist.

> **Gotcha (August, ours, not upstream's).** Plain `git diff` shows only unstaged changes. After a three-way apply, most of your changes are staged. Our preservation patch after one upgrade contained a single line in a test file, and the authority safeguards it was meant to carry were missing. Use `git diff HEAD` (or diff against the base commit, as above), never plain `git diff`.

> **Gotcha.** Do not diff a behind install against the latest upstream. That exports every newer upstream change as if you had reverted it.

Report the result in terms a human can check: files changed, split into tests and everything else, and lines added and removed. Line counts are not features. Do not add overlapping subsets together.

## 3. Tie every change to a reason

Before reconciling anything, match every changed path to an entry in your local-change register: what behaviour it protects, who approved it, which test proves it. A path with no entry is either a forgotten change or something nobody authorised. Find out which before the upgrade, not after.

## 4. Build a candidate in isolation

- A separate clone of the exact target, with its own scratch and state directories. Do not fetch into, rebuild or migrate the live checkout to assess an upgrade.
- Apply the effective patch once with `git apply --3way`.
- For each conflict, read the upstream version first, then reapply the intent of your change. Line positions from last time are not the boundary; upstream may have moved, renamed or absorbed the code.
- Classify every register entry: **preserved** (reapplied and tested), **superseded** (upstream now does it; retire your version and say so in the register), or **retired** (no longer wanted). In our October upgrade four of 51 changed paths were dependency files where upstream had since shipped later fixes than ours. We took upstream's versions rather than forcing ours back.

## 5. Check what the upgrade removes or changes for you

Read the release notes and the configuration migrations between your version and the target.

- Migrations usually change only values still at the old default; deliberate overrides survive. Check your current values before assuming either way.
- Upstream can retire something you rely on. Our October target removed a command-security integration we had enabled, and a migration would have deleted its settings. Upstream had ported its key checks into the built-in detector. That was a decision for a human, made knowingly, not something to discover afterwards.

## 6. Test the candidate

- The tests that cover your local changes, run in the candidate with redirected home and state, never the live configuration.
- A fresh session's assembled instructions, if any of your changes affect prompts or instructions. A session that was already running can still carry the old prompt, so an unchanged old conversation proves nothing about new sessions.
- Record failures and timeouts as they are. A targeted re-run that passes is not a full-suite pass.

Then stop testing. Not every historical assertion is a reason to delay, and "one more check" has no natural end. Our sysadmin agent's own verdict on an earlier upgrade was "I've let the verification sprawl too far."

## 7. Record the decision

Target commit, effective patch hash, the candidate's effective tree ID (`capture-effective-patch.py tree`), test results, register classification, dependency changes, anything upstream removes, and the rollback plan. Preparation is not installation. Go to `guarded-update-routine.md` for the cutover.
