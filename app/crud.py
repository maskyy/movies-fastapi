from passlib.hash import bcrypt
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
        avatar_url=user.avatar_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_films(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Film).offset(skip).limit(limit).all()
