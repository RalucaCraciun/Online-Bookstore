from typing import Dict, List
from uuid import uuid4
from fastapi import HTTPException


class OrderManager:
    def __init__(self, index: str = "orders"):
        from app import elastic_connection
        self.es = elastic_connection
        self.index = index

    def create_order(self, user_id: str, items: List[Dict]) -> Dict:
        """
        Create an order for the user.
        """
        order_id = str(uuid4())
        order_data = {
            "orderId": order_id,
            "userId": user_id,
            "items": items,
            "status": "Created"  # Default status
        }
        try:
            self.es.index(index=self.index, id=order_id, document=order_data)
            return order_data
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to create order. Error: {str(e)}"
            )

    def get_order(self, user_id: str, order_id: str) -> Dict:
        """
        Retrieve a specific order by ID.
        """
        try:
            response = self.es.get(index=self.index, id=order_id)
            order = response["_source"]
            if order["userId"] != user_id:
                raise HTTPException(
                    status_code=403, detail="Unauthorized to access this order."
                )
            return order
        except Exception as e:
            raise HTTPException(
                status_code=404, detail=f"Order with ID {order_id} not found. Error: {str(e)}"
            )

    def place_order(self, user_id: str, order_id: str) -> None:
        """
        Mark an order as placed.
        """
        try:
            order = self.get_order(user_id, order_id)
            if order["status"] == "Placed":
                raise HTTPException(status_code=400, detail="Order is already placed.")

            order["status"] = "Placed"
            self.es.index(index=self.index, id=order_id, document=order)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to place order. Error: {str(e)}"
            )
