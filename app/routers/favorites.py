from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    tags=["favorites"],
)


@router.get("/favorite")
def get_favorites():
    pass


@router.post("/films/{id}/favorite")
def add_favorite():
    pass


@router.delete("/films/{id}/favorite")
def remove_favorite():
    pass