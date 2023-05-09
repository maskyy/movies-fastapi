from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db
from ..internal.token import get_current_user

router = APIRouter(
    tags=["favorites"],
)


@router.get("/favorite", response_model=list[schemas.Film])
async def get_favorites(
    user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    films = crud.get_favorite_films(db, user.id)
    return films


@router.post("/films/{film_id}/favorite")
async def add_favorite(
    film_id: int,
    user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    films = crud.get_film_ids(db)
    if (film_id,) not in films:
        raise HTTPException(
            status_code=404,
            detail="Film not found",
        )
    favs = crud.get_favorites(db, user.id)
    if (film_id,) in favs:
        raise HTTPException(
            status_code=422,
            detail="Film already in favorites",
        )
    crud.add_favorite(db, film_id, user.id)


@router.delete("/films/{film_id}/favorite")
async def remove_favorite(
    film_id: int,
    user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    films = crud.get_film_ids(db)
    if (film_id,) not in films:
        raise HTTPException(status_code=404, detail="Film not found")
    favs = crud.get_favorites(db, user.id)
    if (film_id,) not in favs:
        raise HTTPException(status_code=422, detail="Film not in favorites")
    crud.delete_favorite(db, film_id, user.id)
