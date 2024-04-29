from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status, FastAPI, \
    Form
from .schemas import UserSchema, UserSchemaAuth
from .utils import *
from pydantic import BaseModel
import uvicorn
from src.db.orm import SyncOrm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, \
    OAuth2PasswordBearer

http_bearer = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer('/token')

sync_orm = SyncOrm()


class Token(BaseModel):
    access_token: str
    token_type: str

#
# john = UserSchema(username='john', password=hash_password('qwerty'),
#                   email='john@mail.ru')
#
# sam = UserSchema(username='sam', password=hash_password('secret'),
#                  email='same@mail.ru')
#
# users_db: dict[str, UserSchema] = {
#     john.email: john,
#     sam.email: sam
# }

router = APIRouter(
    prefix='/jwt/auth',
    tags=['jwt']
)


def validate_auth_user(
        email: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = sync_orm.get_user_auth(email)
    if not user:
        raise unauthed_exc
    hashed_password = user[1]
    user = UserSchemaAuth(username=user[0], password=user[1], email=user[2])
    if not validate_password(
            password=password,
            hashed_password=hashed_password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


@router.post('/login/', response_model=Token)
def auth_user(user: UserSchema = Depends(validate_auth_user)) -> Token:
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email
    }
    token = encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type='Bearer'
    )


def get_current_token_payload_user(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        # token: str = Depends(oauth2_scheme)
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'invalid token error {e}')

    return payload


def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload_user)) -> UserSchema:
    useremail: str | None = payload.get('email')
    user = sync_orm.get_user(useremail)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid (user not found)'
        )
    user = UserSchema(user_login=user[0],
                      user_name=user[1],
                      user_email=user[2])

    return user


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='user inactive'
    )

# endpoint для теста
@router.get('/users/me')
def auth_user_check_self_info(
        user: UserSchema = Depends(get_current_active_auth_user)):
    return {
        'data': {
            'user_login': user.user_login,
            'user_name': user.user_name,
            'user_email': user.user_email,
        },
        'status': 'ok'
    }


@router.post('/registration')
def user_registration(user_login: str = Form(),
                      user_name: str = Form(),
                      user_email: str = Form(),
                      password: str = Form()):
    hashed_password = hash_password(password)
    sync_orm.add_user(user_name, user_email, hashed_password, user_login)
    return {
        'data': None,
        'status': 'ok'
    }


app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app)
