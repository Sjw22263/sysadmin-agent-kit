# 08: The second opinion agent

Files for part eight of Guide for building an autonomous agentic system administrator: [Part 8: The second opinion agent](https://onet.com.au/blog/sysadmin-agent-guide-part-8/).

| File | Use it when |
|---|---|
| `second-opinion-agent.md` | Setting up an agent whose only job is to review other agents' conclusions, plans and proposed changes: its authority and boundaries, the output you should require, where it sits in your review routes, and what it cannot do. |
| `review-request-template.md` | Sending it a request. One question, a frozen version with a hash, what it may and may not read, and the shape of the answer. |
| `testing-a-reviewer.md` | Before you trust it: a blind review against a known outcome, a scope test, checking its "not verified" lines, and the limits of simulated reviewer panels. |

These are generalised rewrites of our estate-authored skills and routing records, not upstream Hermes skills. They have not been run-tested in this generic form. Customise them with your own agents, and test the reviewer before you rely on it.

The method does not depend on Hermes. The notes about toolsets and delegation settings are Hermes-specific. The request template assumes the plain-file request queue from Part 7 (`07-from-operator-to-estate-overseer/agent-mail.md`), but works with any channel that keeps a record.

**Version:** Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence:** CC BY 4.0. Use, adapt and share with attribution to Steve Waddington and Maxi Calder.
