from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db
from ..internal.token import get_current_user

router = APIRouter(
    tags=["comments"],
)


@router.get("/films/{film_id}/comments", response_model=list[schemas.Comment])
async def get_film_comments(film_id: int, db: Session = Depends(get_db)):
    films = crud.get_film_ids(db)
    if (film_id,) not in films:
        raise HTTPException(status_code=404, detail="Film not found")

    comments = crud.get_film_comments(db, film_id)
    # FIXME
    formatted_comments = [{
        "id": c.id,
        "film_id": c.film_id,
        "text": c.text,
        "rating": c.rating,
        "author": c.user.name,
        "created_at": c.created_at,
    } for c in comments]
    return formatted_comments


@router.post("/films/{film_id}/comments", response_model=schemas.Comment)
async def add_film_comment(
    film_id: int,
    comment: schemas.CommentBase,
    user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)

):
    films = crud.get_film_ids(db)
    if (film_id,) not in films:
        raise HTTPException(status_code=404, detail="Film not found")

    comment = crud.add_comment(db, comment, film_id, user.id)
    return {
        "id": comment.id,
        "film_id": comment.film_id,
        "text": comment.text,
        "rating": comment.rating,
        "author": comment.user.name,
        "created_at": comment.created_at,
    }


@router.delete("/comments/{comment_id}")
async def remove_comment(
    comment_id: int,
    user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    comment = crud.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id and not user.is_staff:
        raise HTTPException(
            status_code=401,
            detail="Cannot delete others' comments"
        )

    crud.delete_comment(db, comment_id)
