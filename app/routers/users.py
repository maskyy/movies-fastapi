import uuid
from typing import Annotated

import aiofiles
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.exceptions import ValidationError
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db
from ..internal.token import get_current_user

router = APIRouter(
    tags=["users"],
)


async def save_file(file: UploadFile) -> str:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Выберите картинку в формате jpg, png"
        )

    content = await file.read()
    if not content:
        raise HTTPException(
            status_code=400,
            detail="Файл пустой"
        )
    if len(content) > 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Выберите картинку размером не более 10 Мб"
        )

    extension = "jpg" if file.content_type == "image/jpeg" else "png"
    filename = f"img/{uuid.uuid4()}.{extension}"
    async with aiofiles.open(filename, "wb") as out:
        await out.write(content)
    return filename


@router.post("/register", response_model=schemas.User)
async def create_user(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_confirmation: Annotated[str, Form()],
    name: Annotated[str, Form()],
    file: UploadFile | None = None,
    db: Session = Depends(get_db)
):
    try:
        user = schemas.UserCreate(
            email=email,
            password=password,
            password_confirmation=password_confirmation,
            name=name
        )
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    if file:
        user.avatar_url = await save_file(file)

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email занят")
    return crud.create_user(db, user)


@router.get("/user", response_model=schemas.User)
async def get_user(user: Annotated[schemas.User, Depends(get_current_user)]):
    return user
