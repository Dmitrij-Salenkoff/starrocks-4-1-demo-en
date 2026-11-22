# Where did 15 of the 16 tablets go?

[Lesson slides (PDF)](slides.pdf)

**28:00 video · 90-minute lab · StarRocks 4.1.4.** The same events produce the same sum in both tables, yet the FE schedules one tablet in the first case and sixteen in the second. Isolate the mechanism, reverse the result with a different access pattern and defend the decision using real profiles.

## Run the experiment

Open the repository root in VS Code. Start and seed the lab before connecting to the database. In DataGrip use MySQL on 127.0.0.1:9030, user root, an empty password and database course. All queries are supplied. Execute explore.sql one statement at a time and compare its output to the CLI.

```sh
uv run python lab.py up 01/01
uv run python lab.py setup 01/01
uv run python lab.py explore 01/01
uv run python lab.py check 01/01
uv run python lab.py run 01/01
uv run python weeks/01/01/run.py --profile
```

## What the sixteen units represent

The FE keeps catalog metadata and schedules work. The BE reads columnar segments. A native table’s partitions provide placement and maintenance boundaries. Within a partition the full distribution key determines a hash bucket; all rows for one key reach the same bucket. A bucket holds a logical tablet. Its physical copies are replicas. In this lab every tablet has one replica on the same BE. One machine can own many tablets.

| Property | A · sr_date_tenant | B · sr_event_hash |
|---|---|---|
| Partitions | Four date ranges | One implicit partition |
| Distribution | HASH(tenant_id), four buckets each | HASH(event_id), sixteen buckets |
| Local sort key | event_day, tenant_id, event_id | event_day, tenant_id, event_id |
| Inventory | 4 × 4 = 16 tablets | 1 × 16 = 16 tablets |

The generator spans January 1–4, 2026. The first less-than range also permits earlier dates; none occur here. There are 131,072 events. Every 32,768 consecutive IDs starts a new day. Tenant is ID modulo 128, cents is 100 plus ID modulo 1,000. B is copied from A. check.sql reconciles uniqueness, all business fields and the total 78,544,256 cents, so an offsetting loss and duplicate cannot hide behind an equal total.

## Read the plan

January 3 and tenant 7 select one date partition in A and a single bucket within it. Equality supplies the entire HASH(tenant_id) distribution key. Other tenants may share that bucket; the row predicate still does work. B has no date partition, and a tenant/day pair cannot identify an event_id. All sixteen buckets can contain matching rows. Both queries return 256 events and 154,528 cents.

Copy the raw scan ratios. Their numerators are selected partitions and tablets. The tablet denominator can refer to the selected partitions, so the FE might print 1/4. For the claim “one of sixteen in this table,” get the sixteen independently from SHOW TABLET. The plan never drops the other tablets. Numeric IDs belong to your run and may change when tables are recreated.

## Three tests

| Predicate | A · selected partitions / tablets | B · selected partitions / tablets | Rows / cents |
|---|---|---|---|
| Day and tenant | 1 / 1 | 1 / 16 | 256 / 154528 |
| Day only | 1 / 4 | 1 / 16 | 32768 / 19662976 |
| Event 65543 only | 4 / 16 | 1 / 1 | 1 / 643 |

The Python probe gets EXPLAIN text from the FE, counts actual tablet identities, executes each query and checks the selected counts and answer. An unexpected result includes the original plan. The --profile option also executes the focal pair with EXPLAIN ANALYZE. Read counters under the relevant scan operator. OutputRows and rows read can differ, and an omitted counter does not imply zero.

## Independent investigation

1. **Inventory, 15 min.** Record FE, BE, tablets and replicas. Identify one tablet and the BE holding it.
2. **Controlled comparison, 25 min.** Annotate predicate, selected counts and separate inventory in both plans. Add query results and name the controls that stayed fixed.
3. **Negative control, 20 min.** Predict the day-only and event-only plans, then run the checker. Identify the full distribution key behind each change.
4. **Profile, 20 min.** Save the actual scan node and available counters with units. Repeat the pair, mark it warm, and explain why sixteen times fewer tablets need not mean sixteen times lower latency.
5. **Decision, 10 min.** Give recommendations for both workloads, one operational cost and a condition that would change your choice. Explain what a single BE cannot measure.

For 80 day-and-tenant queries and 20 event lookups, total the selected tablets for each layout. Swap the mix and repeat. State what the count measures.

Save the evidence outside the stack, then run `uv run python lab.py down 01/01`.

## Sources

- [Data distribution](https://docs.starrocks.io/docs/table_design/data_distribution/)
- [Query plan and scan ratios](https://docs.starrocks.io/docs/best_practices/query_tuning/query_planning/)
- [EXPLAIN ANALYZE](https://docs.starrocks.io/docs/sql-reference/sql-statements/cluster-management/plan_profile/EXPLAIN_ANALYZE/)
- [Query profiles](https://docs.starrocks.io/docs/best_practices/query_tuning/query_profile_overview/)
