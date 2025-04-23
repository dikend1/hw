from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime

class LoginForm(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class FlowerCreate(BaseModel):
    name:str
    price:float
    description: Optional[str] = ""

class FlowerUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    description:Optional[str]

class FlowerOut(BaseModel):
    id: int
    name:str
    price: float
    description:str
    created_at:datetime
