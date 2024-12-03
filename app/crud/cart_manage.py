from typing import Dict, List
from uuid import uuid4


class CartManager:
    def __init__(self):
        self.cart = {"items": [], "totalPrice": 0.0}

    def add_to_cart(self, item: Dict) -> Dict:
        """
        Add an item to the cart.
        """
        for cart_item in self.cart["items"]:
            if cart_item["bookId"] == item["bookId"]:
                cart_item["quantity"] += item["quantity"]
                self.update_total_price()
                return self.cart

        self.cart["items"].append(item)
        self.update_total_price()
        return self.cart

    def get_cart(self) -> Dict:
        """
        Retrieve the current cart.
        """
        return self.cart

    def remove_from_cart(self, book_id: str) -> None:
        """
        Remove an item from the cart.
        """
        self.cart["items"] = [
            item for item in self.cart["items"] if item["bookId"] != book_id
        ]
        self.update_total_price()

    def update_total_price(self):
        """
        Calculate the total price of the cart.
        """
        self.cart["totalPrice"] = sum(
            item["quantity"] * 15.99 for item in self.cart["items"]
        )
