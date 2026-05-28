from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    firstName: str
    lastName: str
    phoneNumber: Optional[str] = None

class UserCreate(UserBase):
    password: str
    membershipType: Optional[str] = "FREE GUEST"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: str
    nickname: Optional[str] = "Elite Member"
    bio: Optional[str] = ""
    weight: Optional[float] = 0
    height: Optional[float] = 0
    weightGoal: Optional[float] = 0
    goal: Optional[str] = "Maintenance"
    points: Optional[int] = 0
    membershipType: Optional[str] = "FREE GUEST"
    profilePicture: Optional[str] = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: str

class ChangePasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str