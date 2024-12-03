from pydantic import BaseModel, Field
from typing import Optional


class BookRequest(BaseModel):
    title: str = Field(..., description="The title of the book", example="The Great Gatsby")
    author: str = Field(..., description="The author of the book", example="F. Scott Fitzgerald")
    genre: str = Field(..., description="The genre of the book", example="Fiction")
    price: float = Field(..., description="The price of the book", example=15.99)
    description: str = Field(..., description="A brief description of the book", example="A classic novel about the American Dream.")
    stock: int = Field(..., description="The available stock of the book", example=50)

    class Config:
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Fiction",
                "price": 15.99,
                "description": "A classic novel about the American Dream.",
                "stock": 50
            }
        }


class Book(BaseModel):
    bookId: str = Field(..., description="The unique ID of the book", example="abc123")
    title: str = Field(..., description="The title of the book", example="The Great Gatsby")
    author: str = Field(..., description="The author of the book", example="F. Scott Fitzgerald")
    genre: str = Field(..., description="The genre of the book", example="Fiction")
    price: float = Field(..., description="The price of the book", example=15.99)
    description: str = Field(..., description="A brief description of the book", example="A classic novel about the American Dream.")
    stock: int = Field(..., description="The available stock of the book", example=50)
    rating: Optional[float] = Field(None, description="The rating of the book", example=4.5)

    class Config:
        schema_extra = {
            "example": {
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
