# Why does the report show $45 instead of $33?

[Lesson slides (PDF)](slides.pdf)

Public demo · 29-minute walkthrough and a 105-minute lab. Investigate a duplicate capture, then reconcile a revisioned ledger, a quarantined event and two errors that cancel in the total.

## Start the lab

Open the repository root in VS Code and run these commands in its terminal.

```sh
uv run python lab.py up 01/01
uv run python lab.py setup 01/01
```

Select this lab’s connection in DataGrip and run `USE course;`. Execute statements from `explore.sql` one at a time. From the terminal you can reproduce the entire walkthrough with

```sh
uv run python lab.py explore 01/01
```

## Which rows belong in the sum?

A payment processor recorded three successful US-dollar captures across two merchants. The statement shows 33 dollars while the dashboard shows 45. Both systems may have added their inputs correctly. Find out what one input row represents. The processor assigns a stable `event_id` to a capture. After a timeout, it can deliver the same event with a fresh `delivery_id`. Each row in the delivery log represents an envelope received.

The contract for **gross captured USD** adds each unique USD capture event exactly once. The fixture covers a single day. Refunds contribute to a different metric, and a failed attempt contributes no captured funds. The amounts in this exercise are integer cents. Divide by 100 when displaying dollars. Handling other currency scales requires currency metadata.

## Where the query runs

This container runs one Frontend (FE) and one Backend (BE). DataGrip submits SQL to the FE over the MySQL wire protocol. The FE resolves table metadata, constructs an execution plan, coordinates the work and returns results. The BE reads required columns, applies filters and executes aggregation operators. With multiple BEs, rows with the same grouping value may be on different nodes. The physical plan has to combine partial results. A single BE exposes the operators without providing a measurement of network exchange between nodes.

Run `SHOW FRONTENDS` and `SHOW BACKENDS` and inspect `Alive`. A responsive SQL endpoint establishes FE connectivity. A successful table scan also requires an available BE. In the `EXPLAIN` output, look for the table name in the scan and find the currency predicate. Aggregation implements grouping. The plan tells you how the result is computed; the metric definition comes from your SQL.

## Work through the discrepancy in DataGrip

Add a **MySQL** data source. With the defaults, use host `127.0.0.1`, port `9030`, user `root`, an empty password and database `course`. If your port differs, use the port reported by the lab. Download the JDBC driver on first use, click Test Connection, open a query console attached to the source and run `SELECT DATABASE();`. If the result is `NULL`, run `USE course;`.

Open `explore.sql` and stop after the first `SUM`. Write down all four USD capture amounts before scrolling further. Group by `event_id`. Event 101 arrives twice at the same amount. Event 102 has that same amount and a different identity. The window query keeps one delivery for each event. Ordering by descending delivery ID works here because each retry has an identical payload. Differing amounts for one ID would require an explicit revision rule or a conflict investigation.

## Second incident · A correct-looking total after an incorrect release

The second fixture is independent of the $45 dashboard. It is a different January 1 report, with a revisioned processor feed and two snapshots from a separate synthetic settlement statement. Their event identities (A, B, C, F, N, Q and R) belong to this ledger. The nominal amounts and cutoff rules of the first task do not carry over.

| Input | What one row means | What to trust |
|---|---|---|
| `case_input` | A received delivery of one version of a movement | `src_version` orders business revisions. `received_utc` establishes availability. |
| `case_cutoffs` | A named reporting instant | `closed` means before Jan 2 00:00 UTC. `revised` means before Jan 3 00:00 UTC. |
| `case_statement` | A separately supplied booked movement for a cutoff | Each (checkpoint, event_key) has merchant, currency, kind and signed minor units. |

### Canonicalize before computing money

For each cutoff, retain deliveries with `received_utc < cutoff_utc`. Take the greatest **source version** for each event across that visible history. Preserve every delivery tied at that version long enough to compare its business payload. The payload is the tuple (event day, merchant, currency, entry kind, amount). Repeated equal tuples collapse. Multiple distinct tuples under the highest visible version quarantine the **entire event at that cutoff**. An older accepted version cannot silently replace a conflicted one. A later unambiguous higher revision can release the event. This example has no deletes.

Look at A. Its final arrival is an old version 1, yet version 2 is already visible. Pick by last arrival and A regresses from 1,200 to 1,000. Now inspect Q: version 2 arrives twice with different amounts, 250 and 260. Choosing either is an unsupported accounting decision. First compute MAX(src_version) per cutoff and event. Join that version back to the deliveries visible at the same cutoff. A GROUP BY over the business fields gives one row per payload, with its delivery count. A second GROUP BY counts those payloads per cutoff and event. Join the count to each payload so both variants of Q show 2. Including `delivery_id` in the business grouping would incorrectly quarantine harmless retries.

After version selection, assign movements to their business day. For January 1, a `capture` contributes positive gross, a `refund` contributes a positive refund subtotal and a negative contribution to net, and `failed` contributes nothing. The source supplies already booked, independently identifiable refunds; linking a refund to the original authorization requires a different contract. EUR and USD are reported in separate minor units. The next-day movement N must stay out of January 1 even once it is known.

### Reconcile a number to a separate source

Run the final four statements in `explore.sql` in order. Before opening the last result, make a list of movement IDs you expect in each snapshot. On the internal side, A gains 200 and Q loses its original 200 as it enters quarantine. Those changes offset. Both USD cuts therefore have 2,600 gross, 300 refunds and 2,300 net. The EARLIER statement agrees. The revised statement expects Q for 250, bringing its total to 2,550. Its evidence can quantify the gap; under this contract it cannot silently repair the source stream. EUR remains 500 gross and net at both cutoffs.

`case_v_gaps` aligns both datasets at (checkpoint, event_key). An inner join would hide a movement present only on the statement. A complete comparison also checks currency, merchant and entry kind; a sum is too weak to detect misattribution. The negative experiment reads both tables, copies the internal result in memory, adds 100 cents to A and removes 100 from B. It leaves the database unchanged.

```sh
uv run python weeks/01/01/advanced-check.py
```

The aggregate USD residual (internal minus statement) remains −250. The baseline has one mismatching key, Q. The deliberately corrupted result has three. A successful exit means the test **detected** the injected errors. It does not certify the revised report for release.

**Suggested 105-minute lab.** Spend 15 minutes on connections and query execution, 20 on the gross discrepancy, 25 on revisions and quarantine, 25 on independent reconciliation and 20 on the release decision and write-up. Save your SQL and observed outputs in a separate work file.

## Independent work

1. Return the USD capture delivery count, event count, raw sum and deduplicated sum in a single row. State the unit of each column. Reconcile four deliveries, three events and a difference of 1,200 cents.
2. A colleague proposes `SUM(DISTINCT amount_minor)`. Predict the output, run the query and supply the two events that explain the lost value. Expect 2,100 cents and two different IDs sharing a denomination.
3. Calculate gross USD captures per merchant. Add another delivery of event 103 with `delivery_id=8`, recalculate and reconcile the merchant totals. The totals must remain 2,100 and 1,200 cents. Restore the fixture with `setup` after the experiment.
4. Save the relevant part of the grouping plan. Identify the component accepting the connection, the component scanning rows and the operator that reduces row cardinality. Annotate two roles and two operations from your plan.
5. For A and Q list the winning version, distinct winning payloads and observed delivery count at each cutoff. Compare A with a query that simply takes the latest receipt. Show which three distinct mechanisms you observed: identical retry, old late delivery and same-version conflict.
6. Tabulate gross captures, refunds and net in minor units for both currencies and cutoffs. Then simulate a source repair: insert delivery 14, a unique Q version 3, received Jan 2 16:00 UTC, for the same merchant, currency, kind and business day as Q version 2, for 250 cents. Predict the revised USD net and missing-key count. Rerun `setup` afterward.
7. Reproduce the independent key comparison. Run the negative experiment and report all the keys and signed residuals before and after injection. Treat a missing internal posting as zero only when quantifying an amount discrepancy. Explain the difference between a missing record and a real zero, and why an inner join hides Q.
8. Build a release-gate query returning one row per cutoff with distinct blocked-event count, unmatched/mismatched key count and READY/HOLD. Require both counts to be zero for READY. On a fresh fixture expect closed READY, revised HOLD. State who should provide Q’s correction, how to reproduce the original release, and why simply overriding Q from the statement bypasses the defined source contract.


## Assessment on an unfamiliar ledger

Allow another 25–40 minutes after the main lab. Write one SQL query. The grader creates a temporary database on your local StarRocks stand, generates new keys and amounts for each seed, and removes the database when the run finishes.

Start with the hypothesis in `starter.sql`. With stand 01/01 running, execute these commands in the repository root.

```sh
cp weeks/01/01/starter.sql my-answer.sql
uv run python weeks/01/01/assessment.py --query my-answer.sql
```

On PowerShell use `Copy-Item weeks/01/01/starter.sql my-answer.sql` to copy the starter. Expect a `mismatch` on the first run. Edit `my-answer.sql` in VS Code or DataGrip.

- `assessment_input(provider,event_key,rev,received_tick,event_day,merchant,currency,kind,amount_minor)` holds deliveries. Different providers may use the same event key. All source amounts are positive.
- `assessment_cutoffs(cut,cutoff_tick)` gives three exclusive arrival cutoffs. Reconstruct each provider's state at each cutoff. Ties at the highest visible revision can conflict even when their amount agrees. Compare the business day, merchant, currency and kind as well. A later unambiguous revision can release the movement from quarantine.
- Return postings for business day 1. Use a positive sign for captures and a negative sign for refunds. Exclude failed or quarantined movements. Return these columns in order: `cut, provider, event_key, merchant, currency, kind, signed_minor`. Emit exactly one row per eligible movement at each cutoff.

The grader compares the full rows including duplicate counts, then prints examples of missing and extra records. Pass the three default seeds and rerun with your own `--seed 83`. Explain a provider-key collision and one payment that re-enters the report after quarantine.

## Verify and stop

The check expects the original fixture. After write experiments, restore it with `setup`. Save your queries and observations separately before resetting.

```sh
uv run python lab.py check 01/01
uv run python lab.py down 01/01
```

## References

- [StarRocks architecture](https://docs.starrocks.io/docs/introduction/Architecture/)
- [EXPLAIN](https://docs.starrocks.io/docs/sql-reference/sql-statements/cluster-management/plan_profile/EXPLAIN/)
- [DataGrip data sources](https://www.jetbrains.com/help/datagrip/managing-data-sources.html)
