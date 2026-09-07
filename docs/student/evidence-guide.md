# Task 1.4 supplied evidence

Use [evidence-pack.json](evidence-pack.json) for the structured assessed answers. Run your own two baseline experiments and +300 ms experiment as required practical investigation and evidence for instructor defense; timings from your computer do not replace this fixed case.

The pack is a real Task 1.4 capture with 20 users, not Task 1.5's retuned 2-user profile. Read its provenance, windows and limitations before calculating. The observation window includes Locust process startup and exit, so divide the supplied counts by `window_seconds`, not by 30 or Locust's internal duration. No HTTP failures occurred.

For each run record acceptance and completion rates separately. Worker service is the sum/count of complete `coldline.process_exception` spans; accepted-to-terminal duration includes queue wait. Use terminal sum/count for that separate field. Outstanding work is accepted minus completed at the common cutoff; this capture has no failed terminal jobs. Redis XLEN counts retained stream entries and is not backlog. The pack includes individual span durations in microseconds for checking aggregation.

Compute signed percentage changes `(new - reference) / reference * 100`. Compare baseline 2 with baseline 1; compare injection with baseline 2. The supplied exercise repeatability threshold is 15% for acceptance rate, completion rate and mean service time. It does not establish statistical reproducibility. Calculate rates, means, and percentage changes from raw counts, sums, and windows at full precision. Round only the final value written into each answer field; never use rounded answer fields as inputs to later calculations. Round reported numbers to 3-6 decimal places; numeric tolerance is 0.001 in the named unit and 0.01 percentage points for percentage changes.

Choose a primary candidate, assess the specified provider alternative, and select evidence IDs as directed in the pack. `supported`, `contradicted`, and `insufficient-evidence` describe the supplied case only. A fixed local provider delay does not measure a production model service.

Keep the controlled profile fixed. After the experiment, apply the latency override to the running worker and reset the baseline before verification so a new diagnostic request is not trapped behind experiment backlog. The runtime check verifies both the worker setting and an actual provider span.
