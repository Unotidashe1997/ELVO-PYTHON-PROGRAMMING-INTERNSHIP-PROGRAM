"""Demo script that imports grade_utils and processes sample student records."""

import grade_utils as gu

STUDENTS = [
    {"name": "Amina", "scores": [88, 92, 79, 95]},
    {"name": "Brian", "scores": [45, 52, 38, 60]},
    {"name": "Chloe", "scores": [100, 97.5, 99]},
    {"name": "Daniel", "scores": [70, -5, 80]},     # invalid: negative
    {"name": "Esther", "scores": [60, 105, 75]},    # invalid: above 100
    {"name": "Farai", "scores": [55, "abc", 65]},   # invalid: not a number
]


def main() -> None:
    results, errors = gu.process_students(STUDENTS)

    print(f"{'Name':<10}{'Average':>9}{'High':>8}{'Low':>8}  Status")
    print("-" * 45)
    for r in results:
        print(f"{r['name']:<10}{r['average']:>9.2f}{r['highest']:>8.1f}{r['lowest']:>8.1f}  {r['status']}")

    if errors:
        print("\nSkipped records with invalid scores:")
        for name, message in errors:
            print(f"  - {name}: {message}")

    # Interactive check of a single score using the custom exception
    raw = input("\nTry a score to validate (or press Enter to quit): ").strip()
    if raw:
        try:
            print("Valid score:", gu.validate_score(float(raw)))
        except ValueError as exc:  # covers float() failure and InvalidScoreError
            print("Rejected:", exc)


if __name__ == "__main__":
    main()
