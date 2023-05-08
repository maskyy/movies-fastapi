from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    tags=["comments"],
)

@router.get("/films/{id}/comments")
async def get_film_comments():
    pass


@router.post("/films/{id}/comments")
async def add_film_comment():
    pass


@router.delete("/comments/{id}")
async def remove_comment():
    pass
