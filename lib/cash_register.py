#!/usr/bin/env python3


class CashRegister:
    """A simple cash register for an e-commerce site."""

    def __init__(self, discount=0):
        # discount is a percentage off the total (20 means 20% off).
        # Assigning through the property below runs the validation.
        self._discount = 0
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        """Percentage (0-100) taken off the total by apply_discount()."""
        return self._discount

    @discount.setter
    def discount(self, discount):
        # bool is a subclass of int in Python, so exclude it explicitly.
        if (
            isinstance(discount, int)
            and not isinstance(discount, bool)
            and 0 <= discount <= 100
        ):
            self._discount = discount
        else:
            print("Not valid discount")

    def add_item(self, item, price, quantity=1):
        """Add `quantity` of an item to the register and record the transaction."""
        self.total += price * quantity
        # One entry in items per unit, so 3 eggs adds "eggs" three times.
        self.items.extend([item] * quantity)
        self.previous_transactions.append(
            {"item": item, "price": price, "quantity": quantity}
        )

    def apply_discount(self):
        """Take the discount percentage off the total and print the new total."""
        if self.discount == 0 or not self.previous_transactions:
            print("There is no discount to apply.")
            return
        self.total = self.total * (100 - self.discount) / 100
        # Show whole-dollar totals without a trailing ".0" (e.g. $800).
        amount = int(self.total) if self.total == int(self.total) else round(self.total, 2)
        print(f"After the discount, the total comes to ${amount}.")

    def void_last_transaction(self):
        """Remove the most recent transaction from the total and the items list."""
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return
        last = self.previous_transactions.pop()
        # Round to 2 places so float arithmetic doesn't leave 0.9900000000000002.
        self.total = round(self.total - last["price"] * last["quantity"], 2)
        # Remove the units that this transaction added to the end of items.
        del self.items[len(self.items) - last["quantity"]:]