from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_path_key: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_path_key: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()

