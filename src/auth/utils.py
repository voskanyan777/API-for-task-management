from datetime import timedelta, datetime
from .config import settings
import jwt
import bcrypt


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes):
    ''' Геренация токенов'''
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm)

    return encoded


def decode_jwt(token: str | bytes, public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm):
    '''Чтение и валидация'''
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
