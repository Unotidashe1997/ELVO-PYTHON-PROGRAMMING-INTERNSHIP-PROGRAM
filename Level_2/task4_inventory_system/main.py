"""Demo of the inventory system."""

from datetime import date, timedelta

from inventory import Inventory, PerishableProduct, Product


def main() -> None:
    inv = Inventory()
    inv.add_product(Product("P001", "USB Cable", 5.99, 40))
    inv.add_product(Product("P002", "Keyboard", 29.50, 4))
    inv.add_product(PerishableProduct("F001", "Milk 1L", 1.40, date.today() + timedelta(days=2), 20))
    inv.add_product(PerishableProduct("F002", "Yoghurt", 0.90, date.today() - timedelta(days=1), 12))

    inv.add_stock("P001", 5)
    inv.remove_stock("P001", 10)
    try:
        inv.remove_stock("F002", 1)
    except ValueError as exc:
        print("Blocked:", exc)
    try:
        inv.remove_stock("P002", 100)
    except ValueError as exc:
        print("Blocked:", exc)

    print("\n" + inv.generate_report())
    print("\nLow-stock alerts:")
    for p in inv.low_stock_alerts():
        print("  ", p)
    print("\nExample __str__:", inv.get("F001"))


if __name__ == "__main__":
    main()
