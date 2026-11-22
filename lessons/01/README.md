# 01 · From a payment event to a daily revenue mart

**Deliverable:** a logical view that finance can query each morning. A refund issued on Tuesday can make Tuesday negative even if the original sale happened on Monday. A day with only a declined payment still appears. Allow 40–55 minutes, including the plan experiment.

## Start the lab

You need Docker with Compose and uv. From this lesson's directory, run:

```sh
docker compose up -d --wait
uv run --project ../.. python ../../tools/lab.py setup
```

In DataGrip choose the MySQL driver and connect to host `127.0.0.1`, port `9030`, user `root`, with an empty password in the local lab. The container also includes a command-line client:

```sh
docker compose exec starrocks mysql -uroot -h127.0.0.1 -P9030 sr01
```

Setup rebuilds `sr01.payment_events` and the empty starter view `sr01.daily_revenue`. It is safe to repeat for a fresh exercise and replaces your lesson objects. Keep your own SQL in a separate file. The already-loaded seven rows are the entire exercise dataset.

## Follow the query

The client connects to a frontend (FE). The FE keeps the catalog, resolves names and types, plans the query and schedules its fragments. A backend (BE) stores the table's columnar data locally and executes scans and other operators. This local, shared-nothing deployment runs both services in one container. A shared-data deployment instead stores durable data in object storage or HDFS and uses compute nodes. The distinction matters when deciding which node to inspect if SQL accepts connections but a scan cannot run.

```sql
SHOW FRONTENDS;
SHOW BACKENDS;
SHOW CREATE TABLE sr01.payment_events;
SELECT event_id, event_day, order_id, event_type, amount_minor
FROM sr01.payment_events ORDER BY event_id;
```

Look for an FE with query port 9030 and an alive BE. In the DDL, `DUPLICATE KEY (event_id)` permits multiple inserted rows with the same key. This is an append-only journal. Our seven event IDs are unique because the fixture supplies unique events. Submitting an INSERT twice into this table can double-count a payment. Hash distribution with one bucket and replication factor one makes the physical layout small enough for this single BE.

## Define the number before writing SQL

The grain of the input is one payment **event**. The grain of the output is one **observed event day**. One order may contribute a capture on one day and a refund on another. The input date already represents the UTC accounting day. All amounts are positive magnitudes in USD cents. Recognize a refund on its event day. This is a cash-movement metric for this exercise, independent of any accounting revenue-recognition policy.

| event_type | capture_count | gross_minor | refund_minor |
| --- | ---: | ---: | ---: |
| capture | 1 | amount_minor | 0 |
| refund | 0 | 0 | amount_minor |
| decline | 0 | 0 | 0 |

For every output day, `net_minor = gross_minor - refund_minor`. A declined-only day has a group with zeros. A date with no input events has no group. To promise a row for every calendar date, you would need a calendar and a join. The view exposes integer minor units so consumers can format dollars only at the presentation boundary.

## Your work

1. Trace order 502 through the journal. Identify its capture and refund dates. Compute by hand the net for both days, including the other orders. Explain the sign on Tuesday.
2. Run the deliberately incorrect query below. It treats every event amount as money received. Identify the two event types that spoil this interpretation and explain the reported value for January 14.

   ```sql
   SELECT event_day, SUM(amount_minor) AS candidate_net
   FROM sr01.payment_events GROUP BY event_day ORDER BY event_day;
   ```

3. In your SQL editor write `CREATE OR REPLACE VIEW sr01.daily_revenue AS ...`. Produce exactly the five named columns below. Write one conditional sum per input contribution and compute the final difference in an outer query. Keep all input event types in the grouping. Query `SELECT * FROM sr01.daily_revenue ORDER BY event_day;`.
4. Inspect the physical plan. Find a scan of the base table and an aggregate operator. Write a sentence explaining why the view name can disappear from the plan. Look for an event-day predicate near the scan, recording its actual placement on your build.

   ```sql
   EXPLAIN SELECT event_day, net_minor
   FROM sr01.daily_revenue WHERE event_day = '2026-01-13';
   ```

5. From the lesson directory run `uv run --project ../.. python ../../tools/lab.py check`. The fixture check requires exactly these three rows and checks every amount. An empty starter view fails.

| event_day | capture_count | gross_minor | refund_minor | net_minor |
| --- | ---: | ---: | ---: | ---: |
| 2026-01-12 | 2 | 20000 | 2000 | 18000 |
| 2026-01-13 | 1 | 6000 | 8000 | -2000 |
| 2026-01-14 | 0 | 0 | 0 | 0 |

## Read the reference solution

After your attempt, open `solution.sql`. To apply it run `uv run --project ../.. python ../../tools/lab.py solve`, then run the check again. The inner query keeps all seven events and forms three groups. Each CASE selects one contribution and supplies zero for the others. The outer query exposes the two positive totals and subtracts them exactly once. `CREATE OR REPLACE VIEW` saves the definition, so querying the view reads the underlying data. Reapplying the solution replaces the same definition.

Reconcile across the whole fixture: captures sum to 26,000 cents and refunds to 10,000, giving 16,000 cents net. A correct grand total alone is insufficient. Assigning the 8,000-cent refund to Monday preserves that total but changes both daily results.

## Questions to answer aloud

- What does a successful connection to port 9030 tell you about the FE? Which command checks the BE separately?
- Why does filtering to captures and refunds before GROUP BY remove January 14?
- A second delivery of capture event 2 arrives. What does the table store? Which metric changes? What identity would an ingestion job need to make redelivery safe?
- Why can a logical view show a freshly inserted event without a refresh? Which part of the plan reads it?

## Official reading

[Architecture](https://docs.starrocks.io/docs/introduction/Architecture/) · [Duplicate Key tables](https://docs.starrocks.io/docs/table_design/table_types/duplicate_key_table/) · [Logical views](https://docs.starrocks.io/docs/sql-reference/sql-statements/View/CREATE_VIEW/) · [EXPLAIN](https://docs.starrocks.io/docs/sql-reference/sql-statements/cluster-management/plan_profile/EXPLAIN/)
