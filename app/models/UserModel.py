from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from typing import List
from datetime import datetime


class RegisterRequest(BaseModel):
    name: str = Field(..., description="User's full name", example="John Doe")
    email: EmailStr = Field(..., description="User's email address", example="john.doe@example.com")
    password: str = Field(..., description="User's password", example="password123")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address", example="john.doe@example.com")
    password: str = Field(..., description="User's password", example="password123")


# Response Model
class UserResponse(BaseModel):
    userId: str = Field(..., description="Unique ID for the user", example="123456")
    name: str = Field(..., description="User's full name", example="John Doe")
    email: EmailStr = Field(..., description="User's email address", example="john.doe@example.com")


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, description="Updated name of the user")
    email: Optional[EmailStr] = Field(None, description="Updated email of the user")
    password: Optional[str] = Field(None, description="Updated password of the user")


class Token(BaseModel):
    access_token: str
    token_type: str
