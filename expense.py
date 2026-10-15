#!/usr/bin/env python3
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_FILE = "expenses.json"


def _load(path):
    if not os.path.exists(path):
        return {"entries": []}
    with open(path) as f:
        return json.load(f)


def _save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _parse_date(s):
    if s is None:
        return datetime.now(timezone.utc).date().isoformat()
    # accept YYYY-MM-DD, fail loudly on anything else so reports stay sortable
    try:
        datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        print(f"Invalid date '{s}', expected YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)
    return s


def cmd_add(args):
    data = _load(args.file)
    date = _parse_date(args.date)
    entry = {
        "date": date,
        "amount": round(args.amount, 2),
        "category": args.category,
        "note": args.note or "",
    }
    data["entries"].append(entry)
    _save(args.file, data)
    print(f"Added {entry['amount']:.2f} ({entry['category']}) on {entry['date']}.")


def cmd_list(args):
    data = _load(args.file)
    entries = data["entries"]
    if args.category:
        entries = [e for e in entries if e["category"] == args.category]
    if args.from_date:
        entries = [e for e in entries if e["date"] >= args.from_date]
    if args.to_date:
        entries = [e for e in entries if e["date"] <= args.to_date]
    entries = sorted(entries, key=lambda e: e["date"])
    if not entries:
        print("No expenses logged yet.")
        return
    for e in entries:
        note = f"  {e['note']}" if e["note"] else ""
        print(f"{e['date']}  {e['amount']:>10.2f}  {e['category']:<15}{note}")


def cmd_report(args):
    data = _load(args.file)
    entries = data["entries"]
    if args.from_date:
        entries = [e for e in entries if e["date"] >= args.from_date]
    if args.to_date:
        entries = [e for e in entries if e["date"] <= args.to_date]

    by_category = {}
    for e in entries:
        by_category.setdefault(e["category"], 0.0)
        by_category[e["category"]] += e["amount"]
    total = sum(by_category.values())

    if args.json:
        print(json.dumps({
            "by_category": {k: round(v, 2) for k, v in by_category.items()},
            "total": round(total, 2),
            "count": len(entries),
        }, indent=2))
        return

    if not entries:
        print("No expenses logged yet.")
        return
    for category, amount in sorted(by_category.items(), key=lambda kv: -kv[1]):
        print(f"{category:<20} {amount:>12.2f}")
    print("-" * 34)
    print(f"{'TOTAL':<20} {total:>12.2f}")


def cmd_export_csv(args):
    data = _load(args.file)
    entries = sorted(data["entries"], key=lambda e: e["date"])
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "amount", "category", "note"])
        for e in entries:
            w.writerow([e["date"], f"{e['amount']:.2f}", e["category"], e["note"]])
    print(f"Wrote {len(entries)} expenses to {args.out}")


def main():
    p = argparse.ArgumentParser(
        prog="freelance-expense",
        description="Track business expenses for tax reporting. No dependencies, no sign-up, no cloud — just a local JSON file.",
    )
    p.add_argument("--file", default=DEFAULT_FILE, help=f"Expenses file (default: {DEFAULT_FILE} in current directory)")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("add", help="Log an expense")
    sp.add_argument("amount", type=float, help="Amount spent")
    sp.add_argument("category", help="Category, e.g. software, travel, equipment")
    sp.add_argument("--date", help="Date (YYYY-MM-DD), default: today")
    sp.add_argument("--note", help="Optional note")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("list", help="List logged expenses")
    sp.add_argument("--category", help="Only this category")
    sp.add_argument("--from-date", dest="from_date", help="Only entries on/after this date (YYYY-MM-DD)")
    sp.add_argument("--to-date", dest="to_date", help="Only entries on/before this date (YYYY-MM-DD)")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("report", help="Summarize expenses by category, e.g. for a tax period")
    sp.add_argument("--from-date", dest="from_date", help="Only entries on/after this date (YYYY-MM-DD)")
    sp.add_argument("--to-date", dest="to_date", help="Only entries on/before this date (YYYY-MM-DD)")
    sp.add_argument("--json", action="store_true", help="Output as JSON")
    sp.set_defaults(func=cmd_report)

    sp = sub.add_parser("export-csv", help="Export all expenses to a CSV file (for a bookkeeper or tax filing)")
    sp.add_argument("--out", default="expenses.csv", help="Output CSV path (default: expenses.csv)")
    sp.set_defaults(func=cmd_export_csv)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
