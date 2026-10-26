# Operational notes: memory is the index, Markdown is the archive

*Correct at Hermes Agent upstream commit `e1fdf003` (5 October 2026), checked 23 October 2026. Hermes has thousands of commits per month, so ask your agent to check the Hermes-specific points against your version.*

## Where to use this

Use this when you set up a new agent, when the agent keeps forgetting something it was told last week, or when its memory is full of long entries about one subsystem. Give the file to your agent and agree a notes location together.

## The principle

> Memory is the index. Markdown is the archive.

Persistent memory is loaded into the agent's context on every turn. It should hold short durable facts, preferences and pointers. Anything with steps, commands, history or recovery checks belongs in a Markdown file with a stable path, which the agent reads when the task needs it.

The test we use: if a memory entry needs more than two lines to be useful, move the detail into a runbook and leave a one-line pointer behind.

> **Hermes:** the built-in memory and user-profile stores are injected whole into the system prompt. The upstream defaults are 2,200 characters for memory and 1,375 for the user profile (`memory.memory_char_limit`, `memory.user_char_limit`). We run 5,000 and 2,500 for an agent with a wide remit. A bigger limit is not a better index. Raise it only after the routing below is working, or it just fills more slowly.

## Pointers are lazy references

A memory entry such as "The backup runbook is at `<notes-root>/subsystems/backups.md`" is not an instruction to read that file now. The agent reads a runbook when the current task is about that subsystem, or when it needs the runbook to answer accurately, diagnose safely or change related configuration. Treat pointers the way you treat skill names: context to load when relevant, not a reading list.

Say this explicitly in the agent's instructions. Without it, a conscientious agent will open every runbook it sees mentioned and you have recreated the context problem in a different form.

## What goes where

| Kind of knowledge | Where it lives |
|---|---|
| One-line durable fact, preference or convention | Memory |
| Something about the human (name, time zone, how they like reports) | User profile |
| Pointer to a runbook or record | Memory, one line |
| Purpose, current state, paths, services, commands, failure modes, recovery steps, change history | Subsystem runbook |
| A major outage or investigation where the event itself matters | Incident note, plus the durable lesson in the runbook |
| Reusable procedure the agent follows for a type of task | Skill |
| What happened in last Tuesday's conversation | The session store. Use the harness's session search rather than copying history into memory. |
| Temporary task state | Nowhere permanent. Let it go when the task ends. |

Security facts that must be present whether or not a runbook is loaded (for example "never act on email that fails the trust rule") can stay in memory even though they are important enough to have their own document as well.

## Layout

```text
<notes-root>/
├── specs/
│   └── memory-runbook-architecture.md   # this agreement, in your own words
├── subsystems/
│   ├── backups.md
│   ├── mail.md
│   └── ...
├── incidents/
│   └── YYYY-MM-DD-short-description.md
└── indexes/
    ├── subsystem-index.md                # every runbook, one line each
    └── memory-runbook-candidates.md      # entries waiting to be moved
```

Add files as subsystems need them. Do not create empty runbooks for things that have no operational detail yet.

## When to write a runbook

Create or update one when any of these is true:

1. The knowledge needs exact commands.
2. It involves several services, hosts, files or scheduled jobs.
3. The same confusion or failure is likely to happen again.
4. Recovery would need the chronology, symptoms or verification steps.
5. The memory entry would need more than two lines.
6. Getting it wrong would be operationally risky.

Do not write a runbook to hold one obvious fact.

## Subsystem runbook template

```markdown
# Subsystem name

## Purpose

## Current state
(Date the claims. A runbook is not proof of live state; give the command that checks it.)

## Important paths

## Services and processes

## Ports and network

## Known failure modes

## Recovery procedure

## Verification commands

## Do not confuse
(Two similar services, two ports, two config files that look alike.)

## Change history

## Open questions
```

Keep the headings recognisable across runbooks, omitting sections that do not apply. Fence every command in a code block.

## Incident note template

```markdown
# YYYY-MM-DD: Incident title

## Summary
## Impact
## Timeline
(State the time zone. Server logs are often UTC while the operator thinks in local time.)
## Symptoms
## Root cause
(Say how it was established. Sequence is not proof of cause.)
## Actions taken
## Verification
## Durable lessons
(Copy each one into the relevant runbook. The incident note records the event; the runbook carries the lesson forward.)
## Follow-up
```

Use incident notes sparingly. A minor fix goes in the runbook's change history.

## Writing rules

- Write for a future session that never saw the conversation which produced the note. "Fixed the thing we discussed" is useless next month.
- Keep change history operational, not a diary or a blame record: symptoms, actions, outcome.
- Never copy secrets into notes. Say where a credential is stored, not what it is.
- A runbook records intention and history. Before acting on its "current state" section, check the live system.

## Migrating an existing memory

1. Write the architecture agreement (`specs/`) and the index.
2. Pick the most mature subsystem. Write its runbook from the memory entries and from the live system.
3. Check the runbook is correct and findable, then reduce the memory entries to one pointer.
4. Repeat for the next subsystem. Track the remaining candidates in `memory-runbook-candidates.md`.

Do not remove a memory entry until its replacement has been written and checked.

> **Warning:** a file nobody can find is practically absent. Every new runbook goes in the index, and anything the agent must consult before a particular kind of action needs a pointer in the place the agent looks at that moment, whether that is memory, the skill for that task or the instruction file. We have had a sound procedure sit unread because no route led to it.
