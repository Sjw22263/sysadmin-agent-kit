# Does the extra memory layer earn its place?

*Correct at Hermes Agent upstream commit `e1fdf003` (5 October 2026), checked 23 October 2026. Hermes has thousands of commits per month, so ask your agent to check the Hermes-specific points against your version.*

## Where to use this

Use this before you add a memory service, vector store, knowledge graph or similar layer to an agent that already has built-in memory and session search, and again when you are deciding whether to keep one you have. It is a method for an operator's practical judgement on their own estate. It is not a benchmark.

## What we ran

Honcho is the memory service we have records of running. It was self-hosted with its own API, database, cache and a deriver process that turns stored conversations into derived memory. Over its life we changed its embedding backend twice, from a hosted model to a local one and then to a smaller local model after the first saturated the CPU. Those were changes inside one service, not new memory systems. We evaluated several other providers on paper; the records we have show evaluation, not deployment.

In July we switched Honcho off for a week, keeping its data, then retired it. Steve's verdict, as the operator, was that switching it off had made no practical difference, but it had reduced token overhead and the number of things that could break. That is a judgement about one estate with one workload. It says nothing about memory services in general, and you should not quote it as if it did.

## Healthy is not useful

Before you can judge usefulness, check the layer is actually working end to end:

- **Stored is not derived.** Our first failure was conversations being stored but never turning into derived memory, because short sessions never reached the batch threshold. The API was healthy throughout. Check that the derivation queue empties and that a search returns something you know was said recently.
- **Healthy API is not useful recall.** A service that answers health checks can still return nothing relevant. Test with questions whose answers you know.
- **Local embeddings are not a local pipeline.** Moving embeddings to a local model does not move the extraction or reasoning calls. Check where every model call goes, and what it costs.

## Running a fair trial

1. **Write down what the layer is for.** Name the questions or tasks that should go better with it. If you cannot name any, you have your answer already.
2. **Keep the comparison honest.** The alternative is not "no memory". It is the built-in memory, runbooks and session search the agent already has. Compare against that.
3. **Switch the integration off, keep the data.** You may want it back. Record exactly what you disabled.
4. **Make sure it is really off.** Disabling our integration did not stop the service's containers restarting. Check processes, containers and scheduled jobs, not just the agent's configuration.
5. **Run normal work for a set period.** A week was enough for us to see whether anything was missed. Note any task where the agent failed to recall something it would previously have had.
6. **Decide on the record.** What was missed, what it cost to run, what could break, how much attention it took.

> **Hermes:** only one external memory provider can be active at a time (`memory.provider`). The built-in memory review interval (`memory.nudge_interval`) is described upstream as 0 when an external provider extracts memories automatically. Check what your version actually does with both settings when you add or remove a provider, so the built-in review and the provider are not both writing without your knowing.

## Retiring it

- Archive the data and verify the archive (checksums, and a test that it can be read) before deleting anything.
- Remove the service, its network and its scheduled jobs. Confirm afterwards that nothing is running.
- Remove the agent's configuration for it, and any memory entries or runbooks that describe it as current.
- Keep detached storage until the archive is verified, then remove it and record that you did.
- Write a short note saying what was retired, why, where the archive is, and how to restore it.

## When the answer might be different

A memory service may well earn its place where the agent handles many conversations with many people, where relevant history is too large for search to find, or where the built-in memory cannot be kept small. Run the trial on your own workload rather than taking our result, or anyone else's, as the answer.
