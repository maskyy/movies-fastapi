from datetime import datetime

from pydantic import BaseModel, EmailStr, constr, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=8)
    password_confirmation: str
    name: str
    avatar_url: str | None = None

    @validator("password_confirmation")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Пароли не совпадают")
        return v


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str
    avatar_url: str | None

    class Config:
        orm_mode = True


class FilmBase(BaseModel):
    name: str
    preview_image: str | None
    preview_video_link: str | None
    genre: list[str] = []


class FilmCreate(FilmBase):
    poster_image: str | None = None
    background_image: str | None = None
    background_color: str | None = None
    video_link: str | None = None
    description: str | None = None
    director: str | None = None
    starring: list[str] = []
    run_time: int | None = None
    released: int | None = None
    imdb_id: constr(regex=r"tt\d+$")
    status: str

    @validator("status")
    def validate_status(cls, v):
        if v not in ["pending", "on moderation", "ready"]:
            raise ValueError('status should be "pending", "on moderation" or "ready"')
        return v

class Film(FilmBase):
    id: int

    class Config:
        orm_mode = True


class FilmDetail(FilmCreate):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str
    rating: int


class CommentCreate(CommentBase):
    film_id: int
    user_id: int


class Comment(CommentBase):
    id: int
    author: str
    created_at: datetime
