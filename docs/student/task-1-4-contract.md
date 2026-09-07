# Task 1.4 contract

Only these paths are student-editable for this Task:

- `loadtest/model_provider_latency.py` (set `INJECTED_DELAY_MS` to the required value)
- `submission.yaml`

All other files, including the pinned traffic profile in `loadtest/locustfile.py`, are protected. If
your experiment genuinely requires a change there, stop and ask your instructor before proceeding — do
not assume it's permitted.

After the two baseline runs, set the assigned additional delay in the permitted harness file.
Apply it to the running worker with the helper command in `README.md`, then run
`poe reset-baseline` and `poe ready` through the locked environment. Run `poe load-harness`
only after those steps: it checks both the running worker configuration and an observed
provider span. This probe creates a real job. Run `poe reset-baseline` and `poe ready`
again, retaining the applied delay, before the measured `poe load-test` experiment.
Use one recorded cutoff for the experiment's counts so ongoing worker progress does
not turn consecutive queries into apparently contradictory totals.

Preserve your experiment evidence, reset the backlog and confirm readiness while retaining
the applied delay, then run `poe verify` before submitting. Both `poe load-harness` and
`poe answers` must pass.

## Answer and assessment contract

Use `evidence-pack.json` and `evidence-guide.md` in this directory for the graded
structured analysis. The public check verifies shape, permitted changes, runtime behavior, and any
published arithmetic checks. Protected automated answer checks establish semantic
correctness against the public fixed pack. They do not add a held-out scenario.
Preserve actual local experiment evidence for the one final instructor defense and
label it separately from supplied reference data. No separate instructor Task-answer
grade is required; the final defense assesses empirical reasoning and judgment.
