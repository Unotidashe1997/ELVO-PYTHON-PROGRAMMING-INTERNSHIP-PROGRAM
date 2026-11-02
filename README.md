# Elevvo Python Programming & AI – Level 1

## Task 1: CLI Expense Tracker
`cd Level_1/task1_expense_tracker && python expense_tracker.py`
Add expenses (amount, category, date), view them, and get a monthly summary (bonus). Data persists in `expenses.json`.

## Task 2: Student Grade Processor
`cd Level_1/task2_grade_processor && python main.py`  (tests: `pytest`)
`grade_utils.py` is the importable module: average, highest/lowest, pass/fail, score validation,
custom `InvalidScoreError` and type hints (bonus).

## Level 2

### Task 3: Automated File Organizer
`python Level_2/task3_file_organizer/file_organizer.py <folder> [--dry-run]`
Sorts files into extension folders, never overwrites (renames to `name_1.ext`), logs every move to console and `organizer.log`, handles empty/missing folders and permission errors.

### Task 4: OOP Inventory Management
`cd Level_2/task4_inventory_system && python main.py`
`Product` base class with validated `@property` quantity/price, `PerishableProduct` subclass with expiry tracking, `Inventory` with add/remove stock, low-stock alerts and a formatted report. `__str__` and pytest tests included.
