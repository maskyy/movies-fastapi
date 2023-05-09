from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db
from ..internal.token import get_current_user

router = APIRouter(
    tags=["films"],
)


@router.get("/films", response_model=list[schemas.Film])
async def get_films(db: Session = Depends(get_db)):
    return crud.get_films(db)


@router.get("/films/{film_id}", response_model=schemas.FilmDetail)
async def get_film(film_id: int, db: Session = Depends(get_db)):
    film = crud.get_film(db, film_id)
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@router.post("/films", response_model=schemas.FilmDetail)
async def add_film(
    film: schemas.FilmCreate,
    user: Annotated[schemas.User, Security(get_current_user, scopes=["add_films"])],
    db: Session = Depends(get_db)
):
    return crud.create_film(db, film)
