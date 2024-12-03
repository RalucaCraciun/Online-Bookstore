from fastapi import HTTPException
from typing import Dict, List
from app.models.BookModel import BookRequest, Book
from uuid import uuid4


class BooksManager:
    def __init__(self, index: str = "books"):
        from app import elastic_connection
        self.es = elastic_connection
        self.index = index

    def retrieve_books(self) -> List[Dict]:
        """
        Retrieve a list of books.
        """
        try:
            body = {"query": {"match_all": {}}}
            response = self.es.search(index=self.index, body=body)
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve books. Error: {str(e)}")

    def add_book(self, book_data: Dict) -> str:
        """
        Add a new book to Elasticsearch.

        Returns:
        - The ID of the newly added book.
        """
        book_id = str(uuid4())
        book_data["bookId"] = book_id
        try:
            self.es.index(index=self.index, id=book_id, document=book_data)
            return book_id
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to add book. Error: {str(e)}")

    def retrieve_book_by_id(self, book_id: str) -> Dict:
        """
        Retrieve details of a specific book.
        """
        try:
            response = self.es.get(index=self.index, id=book_id)
            return response["_source"]
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found. Error: {str(e)}")

    def update_book(self, book_id: str, updated_data: Dict) -> Dict:
        """
        Update an existing book's details.
        """
        try:
            response = self.es.update(
                index=self.index,
                id=book_id,
                body={"doc": updated_data}
            )

            return response.body
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to update book. Error: {str(e)}"
            )

    def delete_book(self, book_id: str) -> Dict:
        """
        Delete a book by ID.
        """
        try:
            self.es.delete(index=self.index, id=book_id)
            return {"message": f"Book {book_id} deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete book. Error: {str(e)}")
