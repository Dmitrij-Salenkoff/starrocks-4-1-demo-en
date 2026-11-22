"""Cups, receipts and coffee types for January 3."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from lab import connect


def daily_report(cursor, label):
    cursor.execute((HERE / "today.sql").read_text(encoding="utf-8"))
    cups, receipts, types = map(int, cursor.fetchone())
    print(f"{label}: {cups} cups, {receipts} receipts, {types} coffee types")
    return cups, receipts, types


def check_receipts(cursor):
    cursor.execute((HERE / "check.sql").read_text(encoding="utf-8"))
    if cursor.fetchone()[0] != 1:
        raise ValueError("The receipts differ from the example. Restore them with uv run python lab.py setup 01/01.")


def main():
    new_receipt = (HERE / "add_receipt.sql").read_text(encoding="utf-8")
    with connect() as connection, connection.cursor() as cursor:
        cursor.execute("USE course")
        check_receipts(cursor)
        daily_report(cursor, "Before adding the receipt")
        for label in ("After adding receipt 104", "After sending receipt 104 again"):
            cursor.execute(new_receipt)
            if daily_report(cursor, label) != (8, 4, 2):
                raise ValueError("Expected the same answer: 8 cups, 4 receipts and 2 coffee types.")
        check_receipts(cursor)
        cursor.execute("SELECT SUM(cups) FROM cafe_sales WHERE sale_day = '2026-01-02'")
        yesterday = int(cursor.fetchone()[0])
        print(f"January 2 still has {yesterday} cups.")
        print("The espresso on receipt 104 was counted once.")


if __name__ == "__main__":
    main()
