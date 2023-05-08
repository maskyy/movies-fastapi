from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security

from .. import schemas
from ..internal.token import get_current_user

router = APIRouter(
    tags=["films"],
)


@router.get("/films")
async def get_films():
    pass


@router.get("/films/{id}")
async def get_film():
    pass


@router.post("/films")
async def add_film(user: Annotated[schemas.User, Security(get_current_user, scopes=["add_films"])]):
    pass
