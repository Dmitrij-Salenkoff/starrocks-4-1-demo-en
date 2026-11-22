"""Follow the café query through StarRocks."""
from pathlib import Path
import re
import sys

import sqlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from lab import connect, verify_owner


def statements(name):
    return sqlparse.split((HERE / name).read_text(encoding="utf-8"))


def read_nodes(cursor, statement):
    cursor.execute(statement)
    fields = [field[0].lower() for field in cursor.description]
    rows = cursor.fetchall()
    alive = sum(str(row[fields.index("alive")]).lower() in {"true", "1"} for row in rows)
    return len(rows), alive


def evidence_lines(cursor, statement):
    cursor.execute(statement)
    text = "\n".join(str(value) for row in cursor.fetchall() for value in row if value is not None)
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    return [line.strip(" \t│├└─") for line in text.splitlines()]


def find_line(lines, pattern):
    for index, line in enumerate(lines):
        if re.search(pattern, line, re.IGNORECASE):
            return index
    raise ValueError("Missing expected evidence: " + pattern + "\n" + "\n".join(lines))


def show_profile_operator(lines, operator, label):
    pattern = rf"^{operator}\s*\(id\s*="
    index = next((i for i, line in enumerate(lines) if re.search(pattern, line, re.IGNORECASE)), None)
    if index is None:
        ranked = find_line(lines, rf"^\d+\.\s*{operator}\s*\(id\s*=")
        print(f"  {label}: {lines[ranked]}")
        return
    print(f"  {label}: {lines[index]}")
    for line in lines[index + 1:]:
        if re.search(r"\b[A-Z_]+\s*\(id\s*=", line, re.IGNORECASE):
            break
        if line.lower().startswith("outputrows:"):
            print(f"    {line}")
            break


def main():
    verify_owner(HERE)
    version_query, frontends, backends, compute_nodes = statements("architecture.sql")
    explain, query, analyze = statements("plan.sql")
    with connect() as connection, connection.cursor() as cursor:
        cursor.execute("USE course")
        cursor.execute(version_query)
        version, mode = cursor.fetchone()
        print(f"Version: {version}\nMode: {mode}")
        if not re.search(r"\b4\.1\.4\b", str(version)) or str(mode).lower() != "shared_nothing":
            raise ValueError("This lab expects version 4.1.4 in shared_nothing mode.")

        fe = read_nodes(cursor, frontends)
        be = read_nodes(cursor, backends)
        cn = read_nodes(cursor, compute_nodes)
        print(f"Nodes: FE {fe[1]}/{fe[0]} alive, BE {be[1]}/{be[0]} alive, CN {cn[0]} registered.")
        if fe != (1, 1) or be != (1, 1) or cn[0] != 0:
            raise ValueError("Check the lab: it expects one live FE, one live BE and no separate CNs.")

        cursor.execute((HERE / "check.sql").read_text(encoding="utf-8"))
        if cursor.fetchone()[0] != 1:
            raise ValueError("Prepare the receipts with uv run python lab.py setup 01/01.")
        cursor.execute("SET enable_query_cache = false")
        planned = evidence_lines(cursor, explain)
        print("\nPlan before execution")
        for label, pattern in (
            ("Table", r"\bTABLE:\s*(?:[\w`.:]+\.)?`?cafe_sales\b"),
            ("Read the receipts", r"\b(?:OlapScanNode|OLAP_SCAN)\b"),
            ("Add the cups", r"\b(?:AGGREGATE|AGGREGATION)\b"),
        ):
            print(f"  {label}: {planned[find_line(planned, pattern)]}")

        cursor.execute(query)
        actual = int(cursor.fetchone()[0])
        cursor.execute("SELECT cups FROM cafe_sales WHERE sale_day = '2026-01-03' ORDER BY receipt_id")
        quantities = [int(row[0]) for row in cursor.fetchall()]
        if actual not in {6, 8} or actual != sum(quantities):
            raise ValueError("The query answer differs from the saved receipts.")
        print("\nCross-check using receipt quantities: " + " + ".join(map(str, quantities)) + f" = {actual}")

        executed = evidence_lines(cursor, analyze)
        print("\nProfile from a separate execution")
        show_profile_operator(executed, "OLAP_SCAN", "Read the receipts")
        show_profile_operator(executed, "AGGREGATION", "Add the cups")
        print(f"January 3: {actual} cups.")


if __name__ == "__main__":
    main()
