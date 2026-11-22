# Your first query in StarRocks

[Lesson slides (PDF)](slides.pdf)

**Demo lesson · 18-minute video · 35 minutes of hands-on practice · StarRocks 4.1.4**

At closing time on January 3, the café owner asks, “How many cups did we sell today?” A receipt can be for several cups. You will open a small café database, get the answer in DataGrip, then add a sale and see the answer change. An analytical database answers questions about a collection of sales, such as how many drinks a shift prepared. All the SQL is supplied.

### Start with the café open · 5 minutes

Start Docker Desktop. Open the **repository folder** in VS Code, then open **Terminal → New Terminal**. The folder contains `lab.py`. These commands use Docker Compose to start the practice database and load the café's opening receipts. Wait for each command to finish. The first download can take a few minutes.

```sh
uv run python lab.py up 01/01
uv run python lab.py setup 01/01
```

Use Python 3.14 and uv as described in the repository setup guide. `setup` restores the opening receipts whenever you want a fresh attempt.

### Connect DataGrip · 6 minutes

1. In DataGrip choose **File → New → Data Source → MySQL**. StarRocks accepts this connection type.
2. Set **Host** to `127.0.0.1`, **Port** to `9030`, **User** to `root` and **Database** to `course`. Leave the password empty for this local exercise.
3. If DataGrip offers **Download missing driver files**, click it. Click **Test Connection**, then **OK**. Open a query console for this connection. Use the **Execute** button to run selected SQL.

### Answer the owner's question · 8 minutes

One row in `cafe_sales` represents one receipt for one kind of drink. Each row has a receipt number (`receipt_id`), a date (`sale_day`), a drink (`coffee`) and the number of cups on the receipt (`cups`). Open `weeks/01/01/today.sql` in VS Code. Copy its complete contents into your DataGrip console, select the statement and click **Execute**. The file asks this question:

```sql
SELECT SUM(cups) AS cups, COUNT(*) AS receipts,
       COUNT(DISTINCT coffee) AS coffee_types
FROM cafe_sales
WHERE sale_day = '2026-01-03';
```

Read the result with its units: **6 cups, 3 receipts, 2 kinds of coffee**. One latte receipt can contain several cups. Open `weeks/01/01/explore.sql` and execute its first statement, reproduced below, to see which sales contributed.

```sql
SELECT receipt_id, sale_day, coffee, cups
FROM cafe_sales
ORDER BY sale_day, receipt_id;
```

Find receipts 101, 102 and 103. Their cup counts are 2, 1 and 3. Receipt 100 is for four espressos on **January 2**. It belongs to yesterday's report. You can also run the lesson's ready-made queries from the VS Code terminal:

```sh
uv run python lab.py explore 01/01
```

### Add the afternoon sale · 8 minutes

Receipt 104 records two espressos on January 3. Before accepting it, write down your predictions for today's receipts, today's cups and yesterday's cups.

```sh
uv run python lab.py run 01/01
```

The command applies `weeks/01/01/add_receipt.sql` and deliberately sends the same sale again. Read the three lines covering the opening state, the first submission and the repeat. In DataGrip **execute the original January 3 query again**. A result tab shows the answer from the last time you ran that query. You should now see **8 cups, 4 receipts, 2 kinds of coffee**. Run the same terminal command a second time and execute the query again. How many copies of receipt 104 appear in the detail readout?

### Explain and check · 8 minutes

Run this second report to compare dates on one screen.

```sql
SELECT sale_day, COUNT(*) AS receipts, SUM(cups) AS cups
FROM cafe_sales
GROUP BY sale_day
ORDER BY sale_day;
```

1. Explain why the opening answer was six when only three receipts matched the date. Name the three receipt numbers.
2. Compare the two days after adding receipt 104. What stayed at four cups? How did the all-days total move from ten to twelve?
3. Show a second run of the same receipt. Verify that January 3 still has four receipts and eight cups. Save the two-day result or write it in your notes with its units.

```sh
uv run python lab.py check 01/01
uv run python lab.py down 01/01
```

Run `check` before `down`. To practice again, use `up` and `setup`. If the stand is still running, `setup` alone restores January 3 to six cups.

### If your screen looks different

| What you see | What to do |
| --- | --- |
| The terminal cannot find `lab.py` | Open the folder containing `lab.py` in VS Code, then start a new terminal there. |
| Test Connection fails | Confirm `up` finished, check host and port, then test again. If the database `course` is missing, run `setup`. |
| DataGrip says no database is selected | Choose `course` in the console's database selector, or execute `USE course;` in that console. |
| Today's result already says eight | An earlier attempt added 104. Run `setup`, then execute the query again for the opening state. |
| You still see six after adding 104 | Execute the date query again in the same connection. Read the newest result tab. |
| You see ten or twelve for January 3 | Check that the statement you executed includes the January 3 date condition. Those are totals across both days. |

[DataGrip's MySQL connection guide](https://www.jetbrains.com/help/datagrip/mysql.html) · [StarRocks with Docker](https://docs.starrocks.io/docs/quick_start/shared-nothing/)
