# 06: Continuity without a memory landfill

Files for part six of Guide for building an autonomous agentic system administrator: [Part 6: Continuity without a memory landfill](https://onet.com.au/blog/sysadmin-agent-guide-part-6/).

| File | Use it when |
|---|---|
| `operational-notes.md` | Setting up where the agent keeps what it knows: a small memory used as an index, Markdown runbooks as the archive, incident notes and a subsystem index. Includes runbook and incident templates. |
| `memory-review.md` | Memory is filling up or going stale. Audit, classify, propose, back up, apply and verify, plus a light nightly review and what to expect from it. |
| `memory-layer-trial.md` | Deciding whether an extra memory layer (a vector store, a memory service, a knowledge graph) is earning its place, including how to switch it off for a fair trial and retire it cleanly. |

These are generalised rewrites of our estate-authored notes and procedures, not upstream Hermes skills. They have not been run-tested in this generic form. Customise them with your own agent: choose your own notes location, decide which facts deserve a permanent place in memory, and run the review by hand before you schedule it.

The method does not depend on Hermes. The memory limits, approval settings and background-review behaviour mentioned in the files are Hermes-specific.

**Version:** Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence:** CC BY 4.0. Use, adapt and share with attribution to Steve Waddington and Maxi Calder.
