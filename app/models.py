from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    name = Column(String(255), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    is_staff = Column(Boolean, default=False)

    favorites = relationship("Favorite", back_populates="user")


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    poster_image = Column(String(255))
    preview_image = Column(String(255))
    background_image = Column(String(255))
    background_color = Column(String(9))
    video_link = Column(String(255))
    preview_video_link = Column(String(255))
    description = Column(Text)
    director = Column(String(255))
    starring = Column(ARRAY(String))
    genre = Column(ARRAY(String))
    run_time = Column(Integer)
    released = Column(Integer)
    imdb_id = Column(String, nullable=False)
    status = Column(String, nullable=False)

    comments = relationship("Comment", back_populates="film")


class Favorite(Base):
    __tablename__ = "favorites"

    film_id = Column(Integer, ForeignKey("films.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    film = relationship("Film", uselist=False)
    user = relationship("User", uselist=False, back_populates="favorites")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    film = relationship("Film", uselist=False, back_populates="comments")
