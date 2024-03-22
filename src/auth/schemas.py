import bcrypt
from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr
    active: bool = True
