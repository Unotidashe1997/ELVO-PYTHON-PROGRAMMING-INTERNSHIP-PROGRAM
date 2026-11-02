from datetime import date, timedelta

import pytest

from inventory import Inventory, PerishableProduct, Product


def test_negative_stock_rejected():
    p = Product("A", "Item", 1.0, 5)
    with pytest.raises(ValueError):
        p.remove_stock(6)
    with pytest.raises(ValueError):
        p.quantity = -1


def test_add_remove_stock():
    p = Product("A", "Item", 1.0, 5)
    p.add_stock(5); p.remove_stock(3)
    assert p.quantity == 7


def test_low_stock_alert():
    inv = Inventory()
    inv.add_product(Product("A", "Low", 1.0, 2))
    inv.add_product(Product("B", "Fine", 1.0, 50))
    assert [p.sku for p in inv.low_stock_alerts()] == ["A"]


def test_perishable_expiry():
    old = PerishableProduct("F", "Milk", 1.0, date.today() - timedelta(days=1), 10)
    assert old.is_expired() and old.status() == "EXPIRED"
    with pytest.raises(ValueError):
        old.remove_stock(1)
    assert old.write_off_expired() == 10 and old.quantity == 0


def test_duplicate_sku():
    inv = Inventory()
    inv.add_product(Product("A", "x", 1.0))
    with pytest.raises(ValueError):
        inv.add_product(Product("A", "y", 1.0))
