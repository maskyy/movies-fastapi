from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    tags=["comments"],
)

@router.get("/films/{id}/comments")
def get_film_comments():
    pass


@router.post("/films/{id}/comments")
def add_film_comment():
    pass


@router.delete("/comments/{id}")
def remove_comment():
    pass
