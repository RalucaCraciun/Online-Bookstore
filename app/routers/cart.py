from fastapi import APIRouter, HTTPException
from typing import Dict
from app.crud.cart_manage import CartManager
from app.models.CartModel import Cart, CartItem

cart_router = APIRouter()


@cart_router.post("/cart", response_model=Cart)
async def add_item_to_cart(item: CartItem):
    """
    Add an item to the shopping cart.

    Example Request:
    {
        "bookId": "abc123",
        "quantity": 2
    }
    """
    manager = CartManager()
    try:
        cart = manager.add_to_cart(item.dict())
        return cart
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while adding the item: {str(e)}"
        )


@cart_router.get("/cart", response_model=Cart)
async def retrieve_cart():
    """
    Retrieve the current contents of the shopping cart.

    Example Response:
    {
        "items": [
            {
                "bookId": "abc123",
                "quantity": 2
            }
        ],
        "totalPrice": 31.98
    }
    """
    manager = CartManager()
    try:
        cart = manager.get_cart()
        return cart
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while retrieving the cart: {str(e)}"
        )


@cart_router.delete("/cart/{bookId}", response_model=Dict)
async def remove_item_from_cart(bookId: str):
    """
    Remove a specific book from the cart.

    Path Parameter:
    - `bookId`: The ID of the book to remove from the cart.

    Example Response:
    {
        "message": "Book abc123 removed from cart successfully."
    }
    """
    manager = CartManager()
    try:
        result = manager.remove_from_cart(bookId)
        return {"message": f"Book {bookId} removed from cart successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while removing the item: {str(e)}"
        )
