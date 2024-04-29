import bcrypt
from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    user_login: str
    user_name: str
    user_email: EmailStr
    active: bool = True

class UserSchemaAuth(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr
    active: bool = True