from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    tags=["tokens"],
)

SECRET_KEY = "54a9aeaaa8744c58631c79d5050f730116653bb507198404c191bd61295d8d53"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={"add_films": "Добавление фильмов"},
)

invalid_tokens = []

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    if security_scopes.scopes:
        auth_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        auth_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=401,
        detail="Неверные данные",
        headers={"WWW-Authenticate": auth_value},
    )

    try:
        if token in invalid_tokens:
            raise credentials_exception

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, email=email)
    except (JWTError, ValidationError) as exc:
        raise credentials_exception from exc

    user = crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=401,
                detail="Недостаточно прав",
                headers={"WWW-Authenticate": auth_value},
            )
    return user


@router.post("/login", response_model=schemas.Token)
async def login_user(body: schemas.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Неверный логин или пароль")

    scopes = []
    if user.is_staff:
        scopes.append("add_films")
    access_token = create_access_token(
        data={"sub": user.email, "scopes": scopes}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_user(token: Annotated[str, Depends(oauth2_scheme)]):
    invalid_tokens.append(token)
    return {}
