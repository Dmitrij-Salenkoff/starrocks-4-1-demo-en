# Week 1 · Analytical databases and the query path in StarRocks

Look at two ways to store the same receipts, compare PostgreSQL, DuckDB, ClickHouse, BigQuery and StarRocks, then follow one query through the database. In the lab you will see which node accepts the request, which node reads the data and how individual sales add up to six cups for the day.

- [01 · Analytical databases and the StarRocks architecture](01/README.md) · [Lesson slides (PDF)](01/slides.pdf)

## Analytical databases and the StarRocks architecture

1. [Two questions about the same sales](01/slides.pdf#page=1)
2. [Establish the grain before writing SQL](01/slides.pdf#page=2)
3. [What OLTP and OLAP mean](01/slides.pdf#page=3)
4. [Query latency and data freshness have separate clocks](01/slides.pdf#page=4)
5. [Row storage and column storage](01/slides.pdf#page=5)
6. [What column projection actually saves](01/slides.pdf#page=6)
7. [Choosing an analytical system](01/slides.pdf#page=7)
8. [Why a team would choose StarRocks](01/slides.pdf#page=8)
9. [A fast join can still double a sale](01/slides.pdf#page=9)
10. [Meet the FE, BE and CN](01/slides.pdf#page=10)
11. [Where data lives: shared-nothing and shared-data](01/slides.pdf#page=11)
12. [Losing a replica and losing a cache](01/slides.pdf#page=12)
13. [A query’s journey from DataGrip to the result](01/slides.pdf#page=13)
14. [Inspect the running database](01/slides.pdf#page=14)
15. [Four SQL checks for the topology](01/slides.pdf#page=15)
16. [Read one real query plan](01/slides.pdf#page=16)
17. [Separate a changed fixture from a plan problem](01/slides.pdf#page=17)
18. [Choose an architecture for the workload](01/slides.pdf#page=18)

[Further investigation in DataGrip](01/investigate.sql)
