from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from app.crud.cart_manage import CartManager
from app.models.CartModel import Cart, CartItem
from app.routers.auth import get_current_user

cart_router = APIRouter()


@cart_router.post("/cart", response_model=Cart)
async def add_item_to_cart(item: CartItem, user: Dict = Depends(get_current_user)):
    """
    Add an item to the shopping cart.

    Example Request:
    {
        "bookId": "abc123",
        "quantity": 2
    }
    """
    user_id = user["userId"]
    manager = CartManager()
    try:
        cart = manager.add_to_cart(user_id, item.dict())
        return cart
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while adding the item: {str(e)}"
        )


@cart_router.get("/cart", response_model=Cart)
async def retrieve_cart(user: Dict = Depends(get_current_user)):
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
    user_id = user["userId"]
    manager = CartManager()
    try:
        cart = manager.get_cart(user_id)
        return cart
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while retrieving the cart: {str(e)}"
        )


@cart_router.delete("/cart/{bookId}", response_model=Dict)
async def remove_item_from_cart(bookId: str, user: Dict = Depends(get_current_user)):
    """
    Remove a specific book from the cart for a specific user.
    """
    user_id = user["userId"]
    manager = CartManager()
    try:
        manager.remove_from_cart(user_id, bookId)
        return {"message": f"Book {bookId} removed from cart successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while removing the item: {str(e)}"
        )
