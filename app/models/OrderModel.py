from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderItem(BaseModel):
    bookId: str = Field(..., description="The unique ID of the book", example="abc123")
    quantity: int = Field(..., description="The quantity of the book in the order", example=2)

    class Config:
        schema_extra = {
            "example": {
                "bookId": "abc123",
                "quantity": 2
            }
        }


class Order(BaseModel):
    orderId: str = Field(..., description="The unique ID of the order", example="order123")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    totalPrice: float = Field(..., description="The total price of the order", example=31.98)
    status: str = Field(..., description="The status of the order", example="Pending")
    placedAt: datetime = Field(..., description="The timestamp when the order was placed", example="2024-12-02T12:34:56Z")

    class Config:
        schema_extra = {
            "example": {
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
        }
