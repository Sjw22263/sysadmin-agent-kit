# 10: The cost of customising a fast-moving harness

Files for part ten of Guide for building an autonomous agentic system administrator: [Part 10: The cost of customising a fast-moving harness](https://onet.com.au/blog/sysadmin-agent-guide-part-10/).

| File | Use it when |
|---|---|
| `local-change-register.md` | You have changed, or are about to change, the harness's own files. One entry per change: why it has to be in core, who approved it, how you prove it works and when you would retire it. |
| `upgrade-reconciliation.md` | Preparing an upgrade of a customised checkout: measure the net local divergence correctly, build an isolated candidate, classify each change as preserved, superseded or retired, and know when to stop testing. |
| `guarded-update-routine.md` | Doing the cutover: an executor outside what it stops, a rollback exercised through the real path, verification by content, and one completion check. Includes what went wrong in our October upgrade. |
| `capture-effective-patch.py` | Capturing every tracked local change, staged and unstaged, as one full-index patch, and comparing two checkouts by content rather than by patch text. Template with built-in tests: `python3 capture-effective-patch.py self-test`. |

These are generalised rewrites of our sysadmin agent's upgrade procedure, runbook and helper, not upstream Hermes skills. The method files have not been run-tested in this generic form; the script's self-tests pass, and it was run read-only against our own checkout. Customise them with your own agent, for your own estate.

The method does not depend on Hermes. The version banner, update channel and configuration migration notes are Hermes-specific. The cutover executor and the register are ours, not Hermes features.

**Version:** Checked on 30 October 2026 against Hermes Agent v0.22.5, upstream commit `bf0203a7` (22 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence:** CC BY 4.0. Use, adapt and share with attribution to Steve Waddington and Maxi Calder.
