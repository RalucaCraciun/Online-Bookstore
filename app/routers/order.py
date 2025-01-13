from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict
from app.crud.order_manage import OrderManager
from app.crud.cart_manage import CartManager
from app.routers.auth import get_current_user
from app.crud.books_manage import BooksManager

order_router = APIRouter()


@order_router.post("/orders", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_order_from_cart(user: Dict = Depends(get_current_user)):
    """
    Create an order based on the user's cart.

    This automatically clears the user's cart after creating the order.
    """
    user_id = user["userId"]
    cart_manager = CartManager()
    order_manager = OrderManager()

    try:
        # Retrieve the user's cart
        cart = cart_manager.get_cart(user_id)
        if not cart["items"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your cart is empty. Add items before creating an order."
            )

        # Create the order
        order = order_manager.create_order(user_id, cart["items"])

        # Clear the cart
        cart_manager.clear_cart(user_id)

        return {
            "message": "Order successfully created.",
            "orderId": order["orderId"],
            "status": "Created",
            **order
        }
    except HTTPException as e:
        raise e  # Pass specific HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the order: {str(e)}"
        )


@order_router.get("/orders/{orderId}", response_model=Dict, status_code=status.HTTP_200_OK)
async def get_order(orderId: str, user: Dict = Depends(get_current_user)):
    """
    Retrieve a specific order by orderId for the authenticated user.
    """
    user_id = user["userId"]
    order_manager = OrderManager()

    try:
        # Retrieve the order
        order = order_manager.get_order(user_id, orderId)
        return {
            "message": "Order successfully retrieved.",
            **order
        }
    except HTTPException as e:
        raise e  # Pass specific HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the order: {str(e)}"
        )


@order_router.post("/orders/{orderId}/place", response_model=Dict, status_code=status.HTTP_200_OK)
async def place_order(orderId: str, user: Dict = Depends(get_current_user)):
    """
    Place an order for the authenticated user. This reduces the stock of books.
    """
    user_id = user["userId"]
    order_manager = OrderManager()
    books_manager = BooksManager()

    try:
        # Retrieve the order
        order = order_manager.get_order(user_id, orderId)
        if order["status"] != "Created":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order is already placed or cannot be placed."
            )

        # Validate stock and reduce it
        for item in order["items"]:
            book = books_manager.retrieve_book_by_id(item["bookId"])
            if book["stock"] < item["quantity"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock for book {item['bookId']}."
                )
            # Update stock
            books_manager.update_book(
                item["bookId"], {"stock": book["stock"] - item["quantity"]}
            )

        # Update order status to 'Placed'
        order_manager.place_order(user_id, orderId)
        return {
            "message": "Order successfully placed.",
            "orderId": orderId,
            "status": "Placed"
        }
    except HTTPException as e:
        raise e  # Pass specific HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while placing the order: {str(e)}"
        )
