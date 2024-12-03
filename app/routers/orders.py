from fastapi import APIRouter, HTTPException
from app.crud.orders_manage import OrdersManager
from app.models.OrderModel import Order
from typing import Dict

orders_router = APIRouter()


@orders_router.post("/orders", response_model=Order)
async def place_order():
    """
    Place an order.

    Example Response:
    {
        "orderId": "order123",
        "items": [
            {
                "bookId": "abc123",
                "quantity": 2
            }
        ],
        "totalPrice": 31.98,
        "status": "Pending",
        "placedAt": "2024-12-02T12:34:56Z"
    }
    """
    manager = OrdersManager()
    try:
        order = manager.create_order()
        return order
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while placing the order: {str(e)}"
        )


@orders_router.get("/orders/{orderId}", response_model=Order)
async def retrieve_order_details(orderId: str):
    """
    Retrieve details of a specific order.

    Path Parameter:
    - `orderId`: The ID of the order to retrieve.

    Example Response:
    {
        "orderId": "order123",
        "items": [
            {
                "bookId": "abc123",
                "quantity": 2
            }
        ],
        "totalPrice": 31.98,
        "status": "Pending",
        "placedAt": "2024-12-02T12:34:56Z"
    }
    """
    manager = OrdersManager()
    try:
        order = manager.get_order(orderId)
        return order
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {orderId} not found: {str(e)}"
        )
