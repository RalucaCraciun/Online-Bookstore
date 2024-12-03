from typing import Dict
from uuid import uuid4
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserManager:
    def __init__(self):
        from app import elastic_connection
        self.es = elastic_connection
        self.index = "users"
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        """
        Ensure the Elasticsearch index for users exists.
        """
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(
                index=self.index,
                body={
                    "settings": {"number_of_shards": 1, "number_of_replicas": 1},
                    "mappings": {
                        "properties": {
                            "userId": {"type": "keyword"},
                            "name": {"type": "text"},
                            "email": {"type": "keyword"},
                            "password": {"type": "text"},
                        }
                    },
                },
            )

    def register_user(self, user_data: Dict) -> Dict:
        """
        Register a new user.
        """
        query = {"query": {"term": {"email": user_data["email"]}}}
        existing_user = self.es.search(index=self.index, body=query)
        if existing_user["hits"]["hits"]:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_id = str(uuid4())
        user_data["userId"] = user_id
        self.es.index(index=self.index, id=user_id, document=user_data)

        return {"userId": user_id, "name": user_data["name"], "email": user_data["email"]}

    def login_user(self, email: str, password: str) -> Dict:
        """
        Authenticate a user and return their details.
        """
        query = {"query": {"term": {"email": email}}}
        search_result = self.es.search(index=self.index, body=query)
        if not search_result["hits"]["hits"]:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user = search_result["hits"]["hits"][0]["_source"]
        if not password == user["password"]:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return user

    def get_user_by_email(self, email: str) -> Dict:
        """
        Retrieve user details by email.
        """
        query = {"query": {"term": {"email": email}}}
        search_result = self.es.search(index=self.index, body=query)
        if not search_result["hits"]["hits"]:
            return None
        return search_result["hits"]["hits"][0]["_source"]

    def get_all_users(self) -> list:
        """
        Retrieve all users from Elasticsearch.
        Returns:
            A list of user dictionaries.
        """
        try:
            query = {"query": {"match_all": {}}}
            response = self.es.search(index=self.index, body=query, size=1000)  # Adjust size as needed
            users = [hit["_source"] for hit in response["hits"]["hits"]]

            # Remove passwords from the response for security
            for user in users:
                user.pop("password", None)

            return users
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve users. Error: {str(e)}")

    def update_user(self, user_id: str, updated_data: Dict) -> Dict:
        """
        Update a user's data by userId.

        Args:
            user_id: The ID of the user to update.
            updated_data: The data to update.

        Returns:
            The updated user data.

        Raises:
            HTTPException: If the user does not exist or update fails.
        """
        try:
            if not self.es.exists(index=self.index, id=user_id):
                raise HTTPException(status_code=404, detail="User not found")

            self.es.update(index=self.index, id=user_id, body={"doc": updated_data})

            updated_user = self.es.get(index=self.index, id=user_id)["_source"]

            updated_user.pop("password", None)

            return updated_user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update user. Error: {str(e)}")
