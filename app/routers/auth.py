import os
from typing import Dict, Set
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.helper import create_access_token, TOKEN_BLACKLIST, is_token_blacklisted
from app.crud.user_manage import UserManager
from app.models.UserModel import UpdateUserRequest
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "ABC"
ALGORITHM = "HS256"


# Routes
@auth_router.post("/register")
async def register_user(name: str, email: str, password: str):
    """
    Register a new user.
    """
    user_manager = UserManager()
    user_data = {"name": name, "email": email, "password": password}
    print("here", user_data)
    return user_manager.register_user(user_data)


@auth_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user and return a JWT token.
    """
    user_manager = UserManager()
    user = user_manager.login_user(email=form_data.username, password=form_data.password)

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/profile")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current logged-in user's information.
    """
    SECRET_KEY = "ABC"
    ALGORITHM = "HS256"

    if is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted")

    user_manager = UserManager()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = user_manager.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return {"userId": user["userId"], "name": user["name"], "email": user["email"]}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@auth_router.get("/users", response_model=list)
async def get_all_users(token: str = Depends(oauth2_scheme)):
    """
    Retrieve all users.

    Example Response:
    [
        {
            "userId": "123e4567-e89b-12d3-a456-426614174000",
            "name": "John Doe",
            "email": "john.doe@example.com"
        },
        {
            "userId": "789e4567-e89b-12d3-a456-426614174111",
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        }
    ]
    """
    user_manager = UserManager()
    return user_manager.get_all_users()


@auth_router.put("/users/{userId}", response_model=Dict)
async def update_user(userId: str, updated_data: UpdateUserRequest, token: str = Depends(oauth2_scheme)):
    """

    Example Response:
    [{
        "userId": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Updated Name",
        "email": "updated.email@example.com"
    }]
    """

    updated_dict = updated_data.dict(exclude_unset=True)

    user_manager = UserManager()

    return user_manager.update_user(user_id=userId, updated_data=updated_dict)


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(token: str = Depends(oauth2_scheme)):
    """
    Logout the user by blacklisting their JWT token.
    """
    try:
        # Decode the token to validate it
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("sub"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Add token to the blacklist
        TOKEN_BLACKLIST.add(token)
        return {"message": "User logged out successfully", "status": 200}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
