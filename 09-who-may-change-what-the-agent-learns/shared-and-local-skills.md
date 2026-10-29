# Shared methods and local practice

> Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

Once you have more than one agent, the same procedure ends up in several places. Each agent learns its own version of how to send mail, check a service or publish a page, and the copies drift. This file is the pattern we use to stop that without pretending every agent does the same job.

## Three separate questions

Keep these apart. Most of the mess comes from treating them as one.

1. **Who maintains it?** One owner per shared method. In our estate the sysadmin agent maintains the shared library, with one named exception for a package another agent owns.
2. **Who uses it?** Each agent selects only the shared packages its job needs. Using a shared method does not make you its owner, and a method can be shared even when only one agent uses it today.
3. **What is genuinely local?** Bindings and rules that belong to one agent: its own mailbox wrapper, its own approval gate, its own context. Those live in that agent's local skills.

Possessing a skill never grants authority. A shared publishing procedure tells an agent how to publish, not that it may.

## The pattern

- **One maintained source of shared skills**, outside every agent's own skill folder.
- **Selective consumption.** Each agent's configuration lists the individual shared packages it needs, not the whole library.
- **Local addendums with distinct names.** Where an agent needs local detail on top of a shared method, it gets a separate small skill named for itself, for example `<agent>-email-practice` alongside the shared `publishing-email`. The addendum points at the shared method and holds only the local bindings, gates and context.
- **Stock first.** Start from the harness's own shipped skill where there is one. A local edit qualifies for the shared library only if it is a genuine improvement for everyone, not a change specific to one agent's use. In my words at the time: "do not conflate changes specific to your use with an improvement to be shared."
- **Agents propose, owners edit.** An agent that finds a fault in a shared skill proposes the change to the owner. It doesn't edit the shared package because it happens to use it.

### Hermes notes

- Shared packages are selected with `skills.external_dirs` in each profile's `config.yaml`. List individual package directories rather than the whole shared root, so a new shared skill is opt-in for each agent.
- **Gotcha: a local skill with the same name as a shared one wins.** Hermes resolves names in tiers: trusted project skills, then the profile's local skills, then `skills.create_dir`, then `external_dirs`. A local copy called `publishing-email` silently shadows the shared `publishing-email`, so a fix to the shared package never reaches that agent. Give local addendums distinct names and remove stale local copies of shared skills.
- Within one tier, two different skills with the same name are refused as ambiguous rather than guessed. That is safer, but it means a duplicate can stop a skill loading at all.
- A skill's name and its presence in a folder do not tell you which bytes the model received. After any reorganisation, check real resolution for each agent: ask it to load the skill and confirm the path and content, or use the harness's own skill listing for that profile.

## When to use it

Set this up when the second agent arrives, before the copies start. Retrofitting it is possible (we did) but it means reconciling every agent's variants against stock, deciding which differences are improvements, and preserving the history somewhere outside discovery so it doesn't load by accident.

## Checklist

- [ ] One shared source, one named owner.
- [ ] Each agent lists only the shared packages it needs.
- [ ] Local addendums have distinct names and contain only local material.
- [ ] No local copy shares a name with a shared package.
- [ ] Real loading checked for each agent after any change.
- [ ] Old copies archived outside every skill search path.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
