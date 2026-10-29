# Where a new skill goes

> Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

Agents create skills easily. Left alone, every lesson becomes a new skill, and within a few months nobody, including you, can say what the library contains. This rule applies whenever an agent creates, moves, installs or reviews a skill you maintain yourself. Skills shipped with the harness keep their upstream locations.

## The rule

1. **Existing home before new skill.** A new lesson normally belongs in an existing skill, in that skill's `references/` folder, or in the operational runbook it concerns. A standalone skill is justified only by a distinct recurring outcome or a capability that is useful on its own.
2. **One explicit category from a fixed list.** Every skill you maintain lives at `<category>/<skill-name>`, using one of a small number of categories you have agreed. When an agent creates a skill, it names the category explicitly. It does not leave it blank or invent a new one.
3. **The folder is the classification.** The physical category folder is authoritative. Any category recorded inside the skill must agree with it. Don't maintain a second list or registry of what each skill is.
4. **Changing the list needs your approval.** Adding, renaming, splitting or removing a category is a change to this rule, not a filing decision. An agent never creates a new shelf for one skill.
5. **Ownership is unchanged by placement.** Shared skills belong to the shared library's owner; local skills and addendums belong to the local agent (see `shared-and-local-skills.md`).

## Our categories

We use eight, chosen as recognisable kinds of work rather than by tool:

```text
research/
software-development/
systems-operations/
communication-and-coordination/
knowledge-and-documents/
publication-and-promotion/
creative-production/
personal-and-leisure/
```

The same eight apply in the shared library and in each agent's local skills. They are shelves for a human to navigate, not parent skills an agent must load. Choose your own; the test is whether you can say, without looking, where a given skill would be.

### Hermes notes

- `skill_manage` takes a `category` argument on create. Put "always pass one of the agreed categories explicitly" in the agent's instructions, or new skills land wherever the default puts them.
- Background review creates skills too. If it is allowed to write skills without approval (the upstream default; see Part 1's `hermes-self-modification.md`), this rule is advice the reviewer may not follow. With `skills.write_approval: true`, its proposals arrive in your review queue, where you can check placement.

## Gotcha: don't build the registry instead of moving the files

When we reorganised, an early proposal was to leave every skill where it was and add a classification registry over the old folders at runtime. It would have changed a dozen runtime files and fifteen test files, and left the folders as confusing as before. It was withdrawn in favour of actually moving the packages and updating every agent's configuration to the new paths. If the goal is a library a human can understand, the files on disk have to make sense.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
