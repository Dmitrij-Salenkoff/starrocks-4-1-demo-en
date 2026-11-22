-- How does StarRocks plan to count the cups?
EXPLAIN
SELECT SUM(cups) AS cups
FROM cafe_sales
WHERE sale_day = '2026-01-03';

-- Get the actual answer.
SELECT SUM(cups) AS cups
FROM cafe_sales
WHERE sale_day = '2026-01-03';

-- Run the query again and inspect its execution profile.
EXPLAIN ANALYZE
SELECT SUM(cups) AS cups
FROM cafe_sales
WHERE sale_day = '2026-01-03';
