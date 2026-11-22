# Recording script · Why Tuesday's revenue is negative

**Target:** 5–6 minutes, terminal + SQL editor. Start in the lesson directory with Docker available and the image pulled. Keep `solution.sql` open in a second tab. Use the actual result grid and plan on screen. Pause long enough after each query for viewers to read the rows.

| Time | Screen | Say and do |
| --- | --- | --- |
| 0:00–0:35 | Title, then the three expected rows from the handout | “A finance analyst sees minus twenty dollars on Tuesday. Did the report break? We will rebuild that number from seven payment events. Watch the order that was captured on Monday and refunded on Tuesday. Our deliverable is a view the analyst can query tomorrow.” |
| 0:35–1:15 | Run the two shell commands below. Open a SQL console on sr01. Run SHOW FRONTENDS and SHOW BACKENDS. | “Compose starts the frontend and backend. Setup creates our seven events. The SQL client calls the frontend on port 9030. In the first grid, find its query port. In the second, find an alive backend. Here the backend owns the local data and does the scan. A real deployment can spread these jobs across machines.” |
| 1:15–2:00 | Run the event listing below. Highlight rows 2 and 6. | “Amounts are cents. Order 502 captured eight thousand cents on the twelfth. The same order returned eight thousand on the thirteenth. Keep both dates. The event day tells finance when the money moved. Notice order 505 as well. It was declined. Its amount describes an attempt.” |
| 2:00–2:40 | Run the deliberately incorrect sum. Point at 3,000 for Jan 14. | “The easy query gives thirty dollars on a day with one declined attempt. It also adds the refund. Before touching SQL, assign each type a contribution. Capture adds to gross and increments the count, refund adds to a separate positive refund bucket, and decline contributes zero to both. We still need the decline's date.” |
| 2:40–3:50 | Open solution.sql. Reveal the inner SELECT first, then its outer SELECT. Run the full file in the SQL editor. | “Group all events by day. Here the first CASE counts captures. The next two expressions sum the amounts conditionally. They return zero for the other event types. If I placed a filter on event type before the grouping, the fourteenth would vanish. At the top we subtract refunds once. This saved definition is the mart.” |
| 3:50–4:35 | Run the ordered report. Trace each row with the pointer. | “Monday: twenty thousand gross less two thousand refunded gives eighteen thousand. Tuesday: six thousand in, eight thousand out, minus two thousand. Wednesday is present with four zeroes. Across the three days we retain sixteen thousand cents. That total is a second check, while the refund date establishes that Tuesday is correct.” |
| 4:35–5:25 | Run the EXPLAIN below. Scroll to the scan name, then aggregate. In the terminal run the checker. | “The logical view expands into a query over payment_events. Locate that table in the scan and find the aggregate operator. Your build may label the fragments differently. This is a plan, so it tells us the intended work. The checker asks for the actual three rows, including Wednesday. Now we can answer the analyst: Tuesday's refund relates to a Monday sale.” |

## Commands in recording order

```sh
docker compose up -d --wait
uv run --project ../.. python ../../tools/lab.py setup
```

Use DataGrip's MySQL connector with `127.0.0.1:9030`, user `root`, empty local password. Or use `docker compose exec starrocks mysql -uroot -h127.0.0.1 -P9030 sr01`.

```sql
USE sr01;
SHOW FRONTENDS;
SHOW BACKENDS;
SELECT event_id, event_day, order_id, event_type, amount_minor
FROM payment_events ORDER BY event_id;
SELECT event_day, SUM(amount_minor) AS candidate_net
FROM payment_events GROUP BY event_day ORDER BY event_day;
```

At 2:40 execute `solution.sql`. The terminal equivalent is `uv run --project ../.. python ../../tools/lab.py solve`. Then use:

```sql
SELECT * FROM sr01.daily_revenue ORDER BY event_day;
EXPLAIN SELECT event_day, net_minor FROM sr01.daily_revenue
WHERE event_day = '2026-01-13';
```

```sh
uv run --project ../.. python ../../tools/lab.py check
```

**Viewer pause:** Before revealing the solution, ask, “If Wednesday had no events at all, would GROUP BY create a row?” Give viewers five seconds. Resume with, “A group exists only for an input day. Here a declined event gives Wednesday its group.”
