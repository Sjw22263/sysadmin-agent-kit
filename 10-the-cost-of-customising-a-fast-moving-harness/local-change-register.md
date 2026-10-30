# Local change register

> Checked on 30 October 2026 against Hermes Agent v0.22.5 (upstream commit `bf0203a7`, 22 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

Every change you make to the harness's own files is a maintenance commitment that comes due at every upgrade. This register is where you keep track of them: what each change is for, who approved it, how you know it still works, and when you would stop carrying it. `upgrade-reconciliation.md` checks every changed path against it.

Keep it outside the harness checkout, so an upgrade cannot overwrite it.

## Before you add an entry

Ask whether the change has to live in the harness's own code. Most of what an agent needs can go in configuration, skills, identity files or plugins, which upgrades leave alone (check that for your harness). A change to core files earns its place only when the behaviour cannot be had any other way. Ours that did: how requests for information are kept apart from requests to change things, write-safety checks on files, an authorisation check on skill changes, and model catalogue entries the release did not yet carry. We also carry corrections to a few skills that ship with Hermes, which are cheap but still have to be carried.

## Template

Copy one block per change.

```markdown
### <short name>

- **Behaviour it protects:** what goes wrong without it, in one or two sentences.
- **Why not configuration, a skill or a plugin:** the reason it has to be in core files.
- **Approved by / when:** the decision record.
- **Files:** every path it touches, tests included.
- **Proof it works:** the test(s), and for prompt or instruction changes a fresh-session check.
- **Upstream status:** not addressed / partly addressed / superseded in <version>. Checked at each upgrade.
- **Retire when:** the condition under which you would drop it.
- **Upgrade history:** <date> <version>: preserved / reconciled (what changed) / superseded / retired.
```

## Example (generalised from ours)

```markdown
### Information versus execution

- **Behaviour it protects:** a request to explain or review must not be treated as permission to change things.
  Without it, a stock tool instruction told the agent to patch a skill whenever it hit a problem.
- **Why not configuration, a skill or a plugin:** the conflicting text was in the harness's own tool
  instructions and prompt assembly, so the fix had to change them.
- **Approved by / when:** owner, as a local production trial with a tested rollback, then kept.
- **Files:** prompt assembly, system prompt, skill tool, and their tests.
- **Proof it works:** focused tests; a fresh session's assembled prompt puts the authority block first.
- **Upstream status:** still carried locally at v0.22.5. Reconciled by hand at every upgrade so far, because
  upstream edits the same files heavily.
- **Retire when:** upstream ships an equivalent rule, verified in a fresh session.
- **Upgrade history:** Aug: lost in the upgrade, restored (staged changes missed by plain `git diff`).
  Oct: preserved after resolving conflicts by hand in the prompt files and their test.
```

## Keep it honest

- Measure the total at each upgrade and write the date beside it. Ours on 30 October 2026: 47 files differ from the installed upstream release, 22 of them tests, with 1,585 lines added and 263 removed. That excludes everything outside the checkout.
- A path in the diff with no entry here is a finding. Find out where it came from before the upgrade.
- When an entry is superseded, retire it and say so. Carrying a change upstream has absorbed costs you a conflict at every upgrade and protects nothing.
