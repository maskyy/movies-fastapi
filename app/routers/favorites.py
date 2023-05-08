from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    tags=["favorites"],
)


@router.get("/favorite")
async def get_favorites():
    pass


@router.post("/films/{id}/favorite")
async def add_favorite():
    pass


@router.delete("/films/{id}/favorite")
async def remove_favorite():
    pass
