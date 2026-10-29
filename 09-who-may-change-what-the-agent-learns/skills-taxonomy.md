# A skills taxonomy for human control

> Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

This is the method we used to reorganise a skills library that had grown past the point where I could understand it. At the first inventory it held 242 packages across six agents, with 45 pending change proposals. The full account is in our paper *Human in Command* (linked from the Part 9 post). This file is the method.

## The goal

My brief was "one, understandable, taxonomy for all skills with the underlying principle of simplicity and necessity", because "once it gets too complicated that the parts no longer cohere in my head, then effective control is lost."

That is a governance goal, not an efficiency one. Hold onto that, because the efficiency numbers may not cooperate (see below).

## Principles

1. **Necessity before preservation.** For each skill, ask whether it is needed at all before asking where it goes. Stock harness skills, ordinary records and conversation corrections already cover a lot.
2. **Jobs before lessons.** A skill should correspond to a recognisable job ("publish to the website", "check backups"), not to a lesson learned along the way. Lessons go inside the job's skill, at the point where they apply.
3. **One procedural owner per job.** If two skills both claim to tell the agent how to do the same thing, one of them goes.
4. **Conditional detail.** Keep the main skill short and put detail in reference files the skill tells the agent to read only when the task needs it.
5. **Shelves, not parents.** Categories are for navigation (see `skill-placement.md`). Don't create umbrella skills the agent must load first.
6. **No second framework without evidence.** No runtime registry, catalogue or classification layer unless a real problem requires it.

## Method

1. **Inventory everything.** Every shared and local package, every pending proposal, every scheduled job that preloads a skill. Counts and paths, not impressions.
2. **Disposition each package:** keep, merge into another, move to references, replace with the stock version, or retire. Record the reason.
3. **Pilot on real work.** Run a handful of real jobs with the old and new structure and compare what loaded, how often the agent had to go and fetch something, and whether the work came out right.
4. **Move the files.** Physically relocate packages, update each agent's configuration, and archive old locations outside every search path.
5. **Verify from each agent's side.** Real loading for each agent, every scheduled job's preloaded skills resolving, and a few representative tasks. Record what was not verified.

## What our pilot showed

Six jobs, twelve runs. The new structure loaded 18.3% less skill text, but needed 13 retrievals against 10 and 18 model calls against 13. The sysadmin agent's summary: "That is not a clean efficiency win." We went ahead anyway, because the reason for the work was a library a human could understand, control and maintain. Don't sell a taxonomy to yourself as a token saving unless you've measured one.

Tidier folders are also not proof of better behaviour. Our migration verified that every agent loaded the right files and that scheduled jobs still resolved their skills. Whether the agents work better for it is a separate question we haven't measured.

## Gotchas

- **Remove instructions, not agency.** An early proposal to test whether our custom skills were needed would have compared the current agent with a copy stripped of tools as well as skills. As I put it at the time, putting an agent "in a straightjacket with no agentic access and asking it to do agentic tasks will tell us that it fails at agentic tasks." Change one thing at a time. The sysadmin agent's version of the principle: "remove unnecessary instructions, not agency."
- **Don't let the migration machinery become the project.** Our first cutover plan grew a guarded executor with containment markers, scheduler locks and service drop-ins. I said it seemed "way too complicated to me for what it needs to do", and the agent agreed it had let the recovery machinery become the project. A supervised direct cutover with a backup and a checked restore path did the job.
- **A same-named skill is not the same skill.** When replacing local forks with the stock version, check the content, not just the name.
- **Scheduled jobs are consumers too.** A job that preloads a skill by name will break or silently load something else when the skill moves. Inventory them before you move anything.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
