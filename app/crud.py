from passlib.hash import bcrypt
from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pwd = bcrypt.hash(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_pwd,
        name=user.name,
        avatar_url=user.avatar_url,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_films(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Film).offset(skip).limit(limit).all()


def get_film_ids(db: Session):
    return db.query(models.Film.id).all()


def get_film(db: Session, film_id: int):
    return db.query(models.Film).filter(models.Film.id == film_id).first()


def create_film(db: Session, film: schemas.FilmCreate):
    db_film = models.Film(**film.dict())
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


def get_favorites(db: Session, user_id: int):
    return (
        db.query(models.Favorite.film_id)
        .filter(models.Favorite.user_id == user_id)
        .all()
    )


def get_favorite_films(db: Session, user_id: int):
    favorites = [x for (x,) in get_favorites(db, user_id)]
    return db.query(models.Film).filter(models.Film.id.in_(favorites)).all()


def add_favorite(db: Session, film_id: int, user_id: int):
    db_fav = models.Favorite(film_id=film_id, user_id=user_id)
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav


def delete_favorite(db: Session, film_id: int, user_id: int):
    db.query(models.Favorite).filter(
        and_(
            models.Favorite.user_id == user_id,
            models.Favorite.film_id == film_id,
        )
    ).delete()
    db.commit()


def get_film_comments(db: Session, film_id: int):
    film = get_film(db, film_id)
    return film.comments


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def add_comment(db: Session, data: schemas.CommentBase, film_id: int, user_id: int):
    db_comment = models.Comment(
        film_id=film_id,
        user_id=user_id,
        **data.dict(),
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db.query(models.Comment).filter(models.Comment.id == comment_id).delete()
    db.commit()
