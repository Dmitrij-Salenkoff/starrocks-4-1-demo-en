## 00:00:00 · Why did daily revenue turn negative?

Tuesday shows negative twenty dollars in the daily report. Is that a load failure? We will account for every cent using seven payment events and build a revenue view that explains all three days.

## 00:00:12 · What does one row represent?

A row is one event. Order five hundred and one has both a capture and a partial refund. Keeping only one row per order would lose a real money movement. A decline is an observation for audit, but no money moved.

## 00:00:26 · Start the isolated lab

Open the repository in V S Code, sync dependencies, and change to the first lesson. Compose starts a frontend and backend. Setup creates the database and seeds seven rows. In DataGrip, use the My S Q L driver, localhost and port nine zero three zero.

## 00:00:45 · Aggregate by event type

Compute two amounts. Captures contribute to gross revenue. Refunds are recorded as positive cents in their own column. Subtract once to obtain net revenue. Now predict what happens to Wednesday if we remove all declined events before grouping.

## 00:01:02 · Reconcile against the ledger

Monday has two hundred dollars in captures and twenty in refunds. Tuesday has sixty dollars in captures and an eighty dollar refund for an earlier order. Wednesday has just one decline, so the row exists with zero revenue. A day with no events would need a calendar table to appear.

## 00:01:20 · Make the check fail

Build the view and run the check. Try filtering declines out before the aggregation and run it again. Which date went missing? Restore the formula and check once more. The worked solution is in the repository. Being able to explain the negative day and the zero day is the real test.
