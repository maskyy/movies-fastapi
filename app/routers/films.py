from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    tags=["films"],
)


@router.get("/films")
def get_films():
    pass


@router.get("/films/{id}")
def get_film():
    pass


@router.post("/films")
def add_film():
    pass
