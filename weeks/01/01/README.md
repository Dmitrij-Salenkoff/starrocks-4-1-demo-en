# Why does the report show $45 instead of $33?

[Lesson slides (PDF)](slides.pdf)

Public demo · 18 minutes of video plus 30–45 minutes of practice. Trace a query from DataGrip to the data, isolate a retry and reconcile a gross capture metric.

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

## Independent work

1. Return the USD capture delivery count, event count, raw sum and deduplicated sum in a single row. State the unit of each column. Reconcile four deliveries, three events and a difference of 1,200 cents.
2. A colleague proposes `SUM(DISTINCT amount_minor)`. Predict the output, run the query and supply the two events that explain the lost value. Expect 2,100 cents and two different IDs sharing a denomination.
3. Calculate gross USD captures per merchant. Add another delivery of event 103 with `delivery_id=8`, recalculate and reconcile the merchant totals. The totals must remain 2,100 and 1,200 cents. Restore the fixture with `setup` after the experiment.
4. Save the relevant part of the grouping plan. Identify the component accepting the connection, the component scanning rows and the operator that reduces row cardinality. Annotate two roles and two operations from your plan.

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
