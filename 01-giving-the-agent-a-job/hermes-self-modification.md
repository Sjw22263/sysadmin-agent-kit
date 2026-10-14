# Before you start: how a Hermes agent changes its own instructions

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check each setting below against your installed version before relying on it.

## Why this comes first

Out of the box, a Hermes agent is designed to improve itself. That is a feature, and for a personal assistant it may be exactly what you want. For an agent with administrator access to your servers it is a problem, because the agent's skills and identity file are its operating procedures. If they can change without anyone reading the change, you no longer know what procedures your sysadmin agent is following.

We learned this the hard way. An automatic background review in one of our agents rewrote its skills and its own reading of what it was allowed to publish, without going through the review process we had agreed. Our sysadmin agent's summary at the time was:

> "The system took an unresolved conversation about unauthorised policy writing and responded by writing another policy."

Decide how you want each of the routes below to behave before the agent does any real work.

## The four routes, with default settings

### 1. The agent is told to patch skills during normal work

Hermes's standard instructions to the model include:

> "If a skill has issues, fix it with skill_manage(action='patch')."

and tell it to update a skill "before finishing" if it was missing steps. So in an ordinary conversation, the agent will edit its own procedures when it thinks they are wrong.

### 2. Background review runs after conversations

`auxiliary.background_review.enabled` is `true` by default. After a turn, Hermes starts a separate review agent that replays the conversation and decides what to save to memory and which skills to create or patch. With default settings it is prompted roughly every ten user turns for memory (`memory.nudge_interval: 10`) and every ten tool-calling iterations for skills (`skills.creation_nudge_interval: 10`). Setting an interval to `0` disables that prompt.

Neither route above asks permission by default: `skills.write_approval` and `memory.write_approval` are both `false`, which means writes go straight in.

### 3. The curator archives skills nobody has used

`curator.enabled` is `true` by default. Roughly weekly, when the agent has been idle for two hours, it marks the skills under its management as stale after 14 days unused and archives them after 30. Archiving is recoverable (`hermes curator restore <skill>`), but an archived skill is no longer offered to the agent.

By default the curator only touches local skills that carry its management marker, which in practice means skills created by the background review. Skills created in ordinary foreground conversation are stamped differently and are not automatically opted in, and skills you place by hand, built-in skills and hub-installed skills are excluded (pruning built-ins is a separate opt-in, `curator.prune_builtins`, default `false`). You can hand a skill over to the curator deliberately with `hermes curator adopt <skill>`. The automatic stale-and-archive pass does **not** go through `write_approval`; the optional LLM consolidation pass, which is off by default, does because it makes its changes through `skill_manage`.

> **Sysadmin warning.** Recovery procedures are used rarely by design. If the background review wrote one, the curator will archive it after a month without use, which may be before the day you need it. Run `hermes curator status` to see which skills it manages, and pin the ones you rely on (`hermes curator pin <skill>`), or turn the curator off.

### 4. The agent can edit its own SOUL.md

Hermes has an "always ask" approval gate for files that steer agent behaviour (`SOUL.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`). It is aimed at project folders. The agent's own Hermes home directory is deliberately exempt, and the exemption covers that whole tree rather than just the one file, so the file tools can rewrite the agent's own `SOUL.md` without asking, and `write_approval` does not cover it either. (Comments in the Hermes source disagree with each other on this point; the code exempts the home directory.)

An agent with a shell can also change any file its operating-system user can write. File-tool guards are not a security boundary. Operating-system permissions are.

## What we run

```yaml
skills:
  write_approval: true   # skill_manage changes are staged for human review
memory:
  write_approval: false  # memories are the agent's own
```

Review staged skill changes with `/skills pending`, `/skills diff <id>`, `/skills approve <id>` and `/skills reject <id>`. If you gate memory as well, the equivalent is `/memory pending`, `/memory approve <id>` and `/memory reject <id>`.

Note the scope: the gate stages changes made through the `skill_manage` tool. It is not a filesystem lock on the skills directory. An agent that edits a skill file with its ordinary file tools, or with a shell command, does not pass through this gate (see route 4).

Our rule came from a conversation with the sysadmin agent: "you need to be in control of your own short term durable memories. Skills need review, memories are yours." Skills are procedures the agent will follow on your systems; memory is its own working record. You may reasonably decide otherwise.

Changes to `SOUL.md` and to the agent's authority are reserved matters in its mandate (see `mandate-template.md`): the agent may propose them but must not make them without explicit approval. That is an instruction, not an enforcement mechanism. Version control helps you detect and undo an unreviewed change: keep the file in Git and check it for changes nobody approved. It does not prevent the change being made. Prevention means operating-system permissions the agent's own user cannot write or alter, and an account that controls those permissions is not an independent boundary.

## Checklist

- [ ] Decide `skills.write_approval`. For a sysadmin agent, we recommend `true`.
- [ ] Decide `memory.write_approval`.
- [ ] Decide whether background review should run at all (`auxiliary.background_review.enabled`).
- [ ] Pin recovery and rarely used procedures, or disable the curator (`curator.enabled`).
- [ ] Put identity and authority changes in the mandate's reserved matters.
- [ ] Ask your agent to confirm each setting against your installed Hermes version and show you the evidence.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
