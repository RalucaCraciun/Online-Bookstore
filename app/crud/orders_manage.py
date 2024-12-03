from typing import Dict
from uuid import uuid4
from datetime import datetime


class OrdersManager:
    def __init__(self):
        self.orders = {}

    def create_order(self) -> Dict:
        """
        Create a new order from the cart.
        """
        order_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        new_order = {
            "orderId": order_id,
            "items": [
                {"bookId": "abc123", "quantity": 2}  # Example items, replace as needed
            ],
            "totalPrice": 31.98,  # Example price, replace with calculated value
            "status": "Pending",
            "placedAt": now,
        }
        self.orders[order_id] = new_order
        return new_order

    def get_order(self, order_id: str) -> Dict:
        """
        Retrieve details of a specific order.
        """
        if order_id not in self.orders:
            raise ValueError("Order not found")
        return self.orders[order_id]
