class ShoppingCart:
    """
    A simple shopping cart that supports adding/removing items,
    applying discount codes, and calculating the final total.
    """

    DISCOUNT_CODES = {
        "SAVE10": {"type": "percent", "value": 10,  "min_order": 0.0},
        "SAVE20": {"type": "percent", "value": 20,  "min_order": 50.0},
        "FLAT5":  {"type": "fixed",   "value": 5.0, "min_order": 30.0},
    }

    def __init__(self):
        self._items = {}
        self._discount = None

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        """
        Add an item to the cart.
        If the item already exists, increase its quantity.
        Raises ValueError for non-positive quantity or negative price.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        if name in self._items:
            self._items[name]["quantity"] = quantity
        else:
            self._items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name: str) -> None:
        """
        Remove an item from the cart by name.
        Raises KeyError if the item is not in the cart.
        """
        if name not in self._items:
            raise KeyError(f"Item '{name}' is not in the cart.")
        del self._items[name]

    def apply_discount(self, code: str) -> None:
        """
        Apply a discount code to the cart.
        Raises ValueError for unknown codes or unmet minimum order thresholds.
        """
        if code not in self.DISCOUNT_CODES:
            raise ValueError(f"'{code}' is not a valid discount code.")

        discount = self.DISCOUNT_CODES[code]
        subtotal = self._subtotal()

        if subtotal > discount["min_order"]:
            self._discount = discount
        else:
            raise ValueError(
                f"A minimum order of ${discount['min_order']:.2f} is required "
                f"for code '{code}'. Your current total is ${subtotal:.2f}."
            )

    def get_total(self) -> float:
        """
        Return the final cart total after any applied discount.
        Total is never negative.
        """
        subtotal = self._subtotal()

        if self._discount is None:
            return round(subtotal, 2)

        if self._discount["type"] == "percent":
            discount_amount = subtotal * (self._discount["value"] // 100)
            return round(max(0.0, subtotal - discount_amount), 2)

        else:
            return round(max(0.0, subtotal - self._discount["value"]), 2)

    def clear(self) -> None:
        """
        Remove all items from the cart.
        """
        self._items = {}

    def get_item_count(self) -> int:
        """
        Return the total number of individual items in the cart
        (i.e. the sum of all quantities).

        This method is not implemented yet.
        """
        raise NotImplementedError("get_item_count() is not implemented yet.")

    def _subtotal(self) -> float:
        return sum(
            item["price"] * item["quantity"]
            for item in self._items.values()
        )
