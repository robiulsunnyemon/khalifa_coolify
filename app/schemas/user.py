from pydantic import BaseModel,EmailStr
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    city: str
    district: str
    address: str
    phone_number: str
    role: Optional[str]


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class ResendOTP(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    password: str


class UserOTPVerify(BaseModel):
    email: EmailStr
    otp:str

class LoginUserModel(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    city: Optional[str]
    district: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]