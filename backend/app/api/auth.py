"""
Authentication API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=dict)
async def register(user: UserRegister):
    """Register a new user"""
    return {
        "message": "User registered successfully",
        "username": user.username
    }


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login and get access token"""
    # TODO: Implement actual authentication
    return {
        "access_token": "dummy_token",
        "token_type": "bearer"
    }


@router.get("/me")
async def get_current_user():
    """Get current user information"""
    return {
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin"
    }
