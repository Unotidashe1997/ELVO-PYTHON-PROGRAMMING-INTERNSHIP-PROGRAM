"""CLI Expense Tracker with persistent JSON storage.

Run:  python expense_tracker.py
Data is saved to expenses.json next to this script and reloaded on startup.
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.json")
DATE_FORMAT = "%Y-%m-%d"


# ---------- persistence ----------
def load_expenses(path=DATA_FILE):
    """Return the list of saved expenses, or [] if the file is missing/corrupt."""
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read saved data; starting with an empty list.")
        return []


def save_expenses(expenses, path=DATA_FILE):
    with path.open("w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


# ---------- input helpers ----------
def ask_amount():
    while True:
        raw = input("Amount: ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("  Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("  Please enter a valid number (e.g. 12.50).")


def ask_category():
    while True:
        category = input("Category (e.g. food, transport): ").strip().lower()
        if category:
            return category
        print("  Category cannot be empty.")


def ask_date():
    today = datetime.now().strftime(DATE_FORMAT)
    while True:
        raw = input(f"Date YYYY-MM-DD [{today}]: ").strip() or today
        try:
            datetime.strptime(raw, DATE_FORMAT)
            return raw
        except ValueError:
            print("  Invalid date. Use the format YYYY-MM-DD.")


# ---------- actions ----------
def add_expense(expenses):
    entry = {"amount": ask_amount(), "category": ask_category(), "date": ask_date()}
    expenses.append(entry)
    save_expenses(expenses)
    print(f"Saved: {entry['amount']:.2f} on {entry['category']} ({entry['date']})")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"\n{'#':<4}{'Date':<12}{'Category':<16}{'Amount':>10}")
    print("-" * 42)
    for i, e in enumerate(sorted(expenses, key=lambda x: x["date"]), start=1):
        print(f"{i:<4}{e['date']:<12}{e['category']:<16}{e['amount']:>10.2f}")
    print("-" * 42)
    print(f"{'Total':<32}{sum(e['amount'] for e in expenses):>10.2f}")


def monthly_summary(expenses):
    """Bonus: totals, counts and average per category for a chosen month."""
    month = input("Month YYYY-MM [current month]: ").strip() or datetime.now().strftime("%Y-%m")
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use the format YYYY-MM.")
        return

    selected = [e for e in expenses if e["date"].startswith(month)]
    if not selected:
        print(f"No expenses found for {month}.")
        return

    by_category = defaultdict(list)
    for e in selected:
        by_category[e["category"]].append(e["amount"])

    print(f"\nMonthly summary for {month}")
    print(f"{'Category':<16}{'Count':>6}{'Total':>12}{'Average':>12}")
    print("-" * 46)
    for cat, amounts in sorted(by_category.items()):
        total = sum(amounts)
        print(f"{cat:<16}{len(amounts):>6}{total:>12.2f}{total / len(amounts):>12.2f}")
    grand = sum(e["amount"] for e in selected)
    print("-" * 46)
    print(f"{'All categories':<16}{len(selected):>6}{grand:>12.2f}{grand / len(selected):>12.2f}")


MENU = """
=== Expense Tracker ===
1. Add expense
2. View all expenses
3. Monthly summary
4. Quit
"""


def main():
    expenses = load_expenses()
    print(f"Loaded {len(expenses)} saved expense(s).")
    actions = {"1": add_expense, "2": view_expenses, "3": monthly_summary}
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "4":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(expenses)
        else:
            print("Invalid option, please choose 1-4.")


if __name__ == "__main__":
    main()
