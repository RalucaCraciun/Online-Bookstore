from fastapi import APIRouter, HTTPException, status
from app.crud.books_manage import BooksManager
from app.models.BookModel import BookRequest, Book
from typing import Dict


books_router = APIRouter()


@books_router.get("/books", response_model=Dict, status_code=status.HTTP_200_OK)
async def retrieve_books():
    """
    Retrieve a list of books.
    """
    manager = BooksManager()
    try:
        books = manager.retrieve_books()
        return {"books": books}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve books. Error: {str(e)}"
        )


@books_router.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def add_book(book_data: BookRequest):
    """
    Add a new book to the store.

    Example Request:
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Fiction",
        "price": 15.99,
        "description": "A classic novel about the American Dream.",
        "stock": 50
    }
    """
    manager = BooksManager()
    try:
        book_dict = book_data.dict()
        book_id = manager.add_book(book_dict)

        return {
            "bookId": book_id,
            **book_dict,
            "rating": None  # Optional field
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add book. Error: {str(e)}"
        )


@books_router.get("/books/{bookId}", response_model=Dict, status_code=status.HTTP_200_OK)
async def retrieve_book_details(bookId: str):
    """
    Retrieve details of a specific book.

    Path Parameter:
    - `bookId`: The ID of the book to retrieve.

    Example Response:
    {
        "book": {
            "bookId": "abc123",
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "genre": "Fiction",
            "price": 15.99,
            "description": "A classic novel about the American Dream.",
            "stock": 50,
            "rating": 4.5
        }
    }
    """
    manager = BooksManager()
    try:
        books = manager.retrieve_book_by_id(bookId)
        return {"book": books}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve books. Error: {str(e)}"
        )


@books_router.put("/books/{bookId}", response_model=Dict, status_code=status.HTTP_200_OK)
async def update_book_details(bookId: str, updated_data: Dict):
    """
    Update details of a book.

    Path Parameter:
    - `bookId`: The ID of the book to update.

    Example Request:
    {
        "title": "Updated Title",
        "price": 18.99
    }
    """
    manager = BooksManager()

    try:
        # Call the update function and extract necessary data
        result = manager.update_book(bookId, updated_data)
        if result.get("result") == "updated":
            return {
                "message": "Book updated successfully",
                "bookId": bookId,
                "updated_fields": updated_data
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {bookId} not found."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book. Error: {str(e)}"
        )


@books_router.delete("/books/{bookId}", response_model=Dict, status_code=status.HTTP_200_OK)
async def delete_book(bookId: str):
    """
    Delete a book.

    Path Parameter:
    - `bookId`: The ID of the book to delete.

    Example Response:
    {
        "message": "Book abc123 deleted successfully"
    }
    """
    manager = BooksManager()
    try:
        result = manager.delete_book(bookId)
        return result
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {bookId} not found."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete book. Error: {str(e)}"
        )
