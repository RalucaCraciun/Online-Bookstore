from pydantic import BaseModel, Field
from typing import List


class CartItem(BaseModel):
    bookId: str = Field(..., description="The unique ID of the book", example="abc123")
    quantity: int = Field(..., description="The quantity of the book in the cart", example=2)

    class Config:
        schema_extra = {
            "example": {
                "bookId": "abc123",
                "quantity": 2
            }
        }


class Cart(BaseModel):
    items: List[CartItem] = Field(..., description="List of items in the cart")
    totalPrice: float = Field(..., description="The total price of the items in the cart", example=31.98)

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "bookId": "abc123",
                        "quantity": 2
                    }
                ],
                "totalPrice": 31.98
            }
        }
