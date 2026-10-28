# Second opinion request

> Template for one request to a second opinion agent. Copy it into the reviewer's request queue (see `agent-mail.md` in the Part 7 folder) and fill every field. Checked on 23 October 2026; the template does not depend on Hermes.

```markdown
# Second opinion: <short subject>

**Status:** pending
**From:** <requesting agent or person>
**To:** <second opinion agent>
**Sent:** <date and time, with timezone>
**Respond by:** <deadline, or "no deadline">

## Question

<One precise question. "Is this ready for a decision?" is better than "What do you think?">

## Material

- Reviewed version: <path or attachment>, SHA-256 <hash>
- Supporting sources you may read: <list>
- Sources you may NOT read: <list, e.g. later outcomes, other reviewers' answers>

## Context

<What the material is for, who will act on it, and what decision follows. Keep it to what the reviewer needs.>

Blind or anchored: <"Blind: the author's conclusion is withheld." or "Anchored: the author's reasoning is included below.">

## What we want back

Replace the Outcome section below with:

1. Verdict first (ready / revise before decision / unresolved).
2. Confidence, and what it rests on.
3. The load-bearing assumption, and whether it holds.
4. Material objections, each with consequence and reference. Mark each as a reasoning failure, an uncertain fact, or a preference.
5. A simpler sufficient alternative, if any.
6. What you did not verify.
7. Anchoring disclosure.

Then stop. Do not rewrite the material.

## Decision or approval needed

None. This request carries context, not authority. Do not implement anything.

---

## Outcome

<Reviewer writes here.>

**Handled by:**
**Handled:**
**Reviewed version SHA-256:** <the hash the reviewer actually checked, or "not verified">
```

## Notes on use

- If the reviewer cannot confirm the hash or the material differs from what was described, it records the discrepancy instead of reviewing a guess.
- One targeted follow-up question is reasonable. A second full round on the same version usually means the question was wrong.
- Keep completed requests. They are the only record of what the reviewer was actually told.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
