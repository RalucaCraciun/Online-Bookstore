from typing import Dict, List
from fastapi import HTTPException
from uuid import uuid4


class CartManager:
    def __init__(self, index: str = "carts"):
        self.cart = {"items": [], "totalPrice": 0.0}
        from app import elastic_connection
        self.es = elastic_connection
        self.index = index

    def add_to_cart(self, user_id: str, item: Dict) -> Dict:
        """
        Add an item to the user's cart.
        """
        cart = self.get_cart(user_id)

        # Check if item already exists
        for cart_item in cart["items"]:
            if cart_item["bookId"] == item["bookId"]:
                cart_item["quantity"] += item["quantity"]
                self.update_cart(user_id, cart)
                return cart

        # Add new item
        cart["items"].append(item)
        self.update_cart(user_id, cart)
        return cart

    def get_cart(self, user_id: str) -> Dict:
        """
        Retrieve the current cart for a user.
        """
        try:
            response = self.es.get(index=self.index, id=user_id)
            return response["_source"]
        except Exception:
            # If cart does not exist, create a new one
            return {"items": [], "totalPrice": 0.0}

    def remove_from_cart(self, user_id: str, book_id: str) -> None:
        """
        Remove an item from the user's cart.
        """
        cart = self.get_cart(user_id)
        cart["items"] = [
            item for item in cart["items"] if item["bookId"] != book_id
        ]
        self.update_cart(user_id, cart)

    def update_cart(self, user_id: str, cart: Dict):
        """
        Save the updated cart to Elasticsearch.
        """
        cart["totalPrice"] = sum(
            item["quantity"] * 15.99 for item in cart["items"]
        )
        try:
            self.es.index(index=self.index, id=user_id, document=cart)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to update cart. Error: {str(e)}"
            )

    def clear_cart(self, user_id: str) -> None:
        """
        Clear the cart for the user after an order is placed.
        """
        try:
            empty_cart = {"items": [], "totalPrice": 0.0}
            self.es.index(index=self.index, id=user_id, document=empty_cart)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to clear cart. Error: {str(e)}"
            )

    def update_total_price(self):
        """
        Calculate the total price of the cart.
        """
        self.cart["totalPrice"] = sum(
            item["quantity"] * 15.99 for item in self.cart["items"]
        )
