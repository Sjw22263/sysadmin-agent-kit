# A reflection store for the next run

**Use:** adapt alongside `improvement-research.md`, outside persistent system memory and outside the active skill loader. This is a document and example data shape, not installed software. Generalised from our working process, not run-tested as generic automation.

**Version:** Process inspected 21 October 2026, running Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence:** CC BY 4.0, Steve Waddington and Maxi Calder.

## The useful unit

Keep a specific lesson, its evidence and what to do differently when the situation recurs. 'Be more careful' does not qualify. Nor does writing 'I have learned' establish that behaviour changed. A reflection is working context for a task, not new authority, an approved policy or a model-weight update.

The store is a JSON object with an `items` array. This synthetic example illustrates the shape used by our process; it is not a recorded incident:

```json
{
  "version": 1,
  "items": [
    {
      "id": "refl-2026-10-23-example",
      "created": "2026-10-23",
      "lesson": "A proposed search plan repeated sources already inspected in the previous run.",
      "what_to_do_differently": "Before opening a source, look up its URL in the source index. Reinspect only with a recorded reason, such as a due watch item.",
      "dimensions": ["memory and continuity", "learning loops"],
      "source": "EXAMPLE ONLY: replace with the actual report or correction reference",
      "review_date": "2026-11-22",
      "reinforced_count": 0,
      "last_reinforced": null,
      "status": "active"
    }
  ]
}
```

Choose your own dimensions or omit them if they do no work. The important fields are the specific lesson, changed action, retrievable source, status and review history. Do not copy the synthetic example into a live evidence record as if it happened.

## Before a run

Load the active entries into the task's working context. Archived entries stay in the file but are not loaded by default. In our process, a lesson whose review date has passed and whose `reinforced_count` is zero is archived. That is not a rule to delete an old but reinforced lesson automatically.

**Gotcha:** the current rule is only a partial bound. Once a lesson has been reinforced, that zero-count expiry rule does not retire it later. It can remain active after its review date. Inspect the active set at process review rather than claiming a date field alone keeps the store small. Any revised expiry or active-size policy should be an explicit decision, not a silent change made while tidying the file.

Do not load raw reports, all archived entries and the entire store history just because they exist. The point is to make the relevant lesson available at the next decision, not to enlarge every context window.

## After a run or correction

Ask whether the run produced a specific lesson that would change a later action. If not, add nothing.

- For a genuinely new lesson, record the source, concrete action, creation date, a review date 30 days later, zero reinforcements and active status.
- When the same lesson is observed again, update its existing entry: increment the count, record the date and extend review by 30 days. Do not create a duplicate to make the store look active.
- If new evidence contradicts a lesson, preserve the correction and stop treating the old entry as current advice. Do not merge incompatible conclusions into an ambiguous instruction.
- Validate JSON, required keys, unique IDs and allowed status values. Use atomic per-file replacement and inspect before resuming a partly failed update.

**Gotcha:** reinforcement counts recurrence, not successful learning. A rule can be reinforced because the agent made the same mistake again. To claim improvement, inspect a later comparable task and its actual outcome.

## Review and separation

Periodically inspect active entries against their sources and later use. Is the lesson still accurate? Does it duplicate a procedure already maintained elsewhere? Did it ever alter a real decision? Is retaining it worth the context it consumes?

Keep this task store separate from persistent personal memory, governing instructions and active skills. A reflection that suggests changing any of them is a proposal through the applicable approval route. Neither an entry nor its repeated reinforcement authorises that change.

This pattern persists available context between runs. It does not teach the base model new weights or prove that the agent can detect its own blind spots.
