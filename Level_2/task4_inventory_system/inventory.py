"""Object-oriented inventory management system."""

from datetime import date, timedelta
from typing import Dict, List, Optional


class Product:
    """A basic stock item with validated price and quantity."""

    def __init__(self, sku: str, name: str, price: float, quantity: int = 0,
                 low_stock_threshold: int = 5) -> None:
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity
        self.low_stock_threshold = low_stock_threshold

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        self._quantity = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = float(value)

    def add_stock(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Amount to add must be positive.")
        self.quantity += amount

    def remove_stock(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Amount to remove must be positive.")
        if amount > self.quantity:
            raise ValueError(f"Insufficient stock for {self.name}: "
                             f"{self.quantity} available, {amount} requested.")
        self.quantity -= amount

    def is_low_stock(self) -> bool:
        return self.quantity <= self.low_stock_threshold

    def total_value(self) -> float:
        return self.price * self.quantity

    def status(self) -> str:
        return "LOW STOCK" if self.is_low_stock() else "OK"

    def __str__(self) -> str:
        return (f"{self.sku} | {self.name} | qty {self.quantity} | "
                f"${self.price:.2f} | {self.status()}")


class PerishableProduct(Product):
    """A product with an expiry date; expired stock cannot be sold and can be written off."""

    def __init__(self, sku: str, name: str, price: float, expiry_date: date,
                 quantity: int = 0, low_stock_threshold: int = 5, warn_days: int = 3) -> None:
        super().__init__(sku, name, price, quantity, low_stock_threshold)
        self.expiry_date = expiry_date
        self.warn_days = warn_days

    def is_expired(self, today: Optional[date] = None) -> bool:
        return (today or date.today()) > self.expiry_date

    def expires_soon(self, today: Optional[date] = None) -> bool:
        today = today or date.today()
        return not self.is_expired(today) and self.expiry_date - today <= timedelta(days=self.warn_days)

    def remove_stock(self, amount: int) -> None:
        if self.is_expired():
            raise ValueError(f"Cannot sell {self.name}: expired on {self.expiry_date}.")
        super().remove_stock(amount)

    def write_off_expired(self) -> int:
        """Remove all stock if expired; return how many units were discarded."""
        if not self.is_expired():
            return 0
        discarded, self.quantity = self.quantity, 0
        return discarded

    def status(self) -> str:
        if self.is_expired():
            return "EXPIRED"
        if self.expires_soon():
            return "EXPIRES SOON"
        return super().status()

    def __str__(self) -> str:
        return f"{super().__str__()} | exp {self.expiry_date}"


class Inventory:
    """Collection of products with stock operations, alerts and reporting."""

    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        if product.sku in self._products:
            raise ValueError(f"SKU {product.sku} already exists.")
        self._products[product.sku] = product

    def get(self, sku: str) -> Product:
        try:
            return self._products[sku]
        except KeyError:
            raise KeyError(f"No product with SKU {sku}.") from None

    def add_stock(self, sku: str, amount: int) -> None:
        self.get(sku).add_stock(amount)

    def remove_stock(self, sku: str, amount: int) -> None:
        self.get(sku).remove_stock(amount)

    def low_stock_alerts(self) -> List[Product]:
        return [p for p in self._products.values() if p.is_low_stock()]

    def generate_report(self) -> str:
        lines = [f"{'SKU':<8}{'Name':<18}{'Qty':>5}{'Price':>10}{'Value':>11}  Status",
                 "-" * 62]
        for p in sorted(self._products.values(), key=lambda p: p.sku):
            lines.append(f"{p.sku:<8}{p.name:<18}{p.quantity:>5}{p.price:>10.2f}"
                         f"{p.total_value():>11.2f}  {p.status()}")
        lines.append("-" * 62)
        total = sum(p.total_value() for p in self._products.values())
        lines.append(f"{'Total inventory value':<41}{total:>11.2f}")
        return "\n".join(lines)
