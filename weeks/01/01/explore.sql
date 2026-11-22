-- Look at the receipts from both days.
SELECT receipt_id, sale_day, coffee, cups
FROM cafe_sales
ORDER BY sale_day, receipt_id;

-- How many cups were sold on January 3?
SELECT SUM(cups) AS cups
FROM cafe_sales
WHERE sale_day = '2026-01-03';

-- How many receipts and coffee types were there that day?
SELECT SUM(cups) AS cups, COUNT(*) AS receipts, COUNT(DISTINCT coffee) AS coffee_types
FROM cafe_sales
WHERE sale_day = '2026-01-03';

-- How many cups were sold of each drink?
SELECT coffee, SUM(cups) AS cups
FROM cafe_sales
WHERE sale_day = '2026-01-03'
GROUP BY coffee
ORDER BY coffee;

-- How many cups were sold yesterday and across both days?
SELECT SUM(cups) AS yesterday_cups
FROM cafe_sales
WHERE sale_day = '2026-01-02';

SELECT SUM(cups) AS all_cups
FROM cafe_sales;
