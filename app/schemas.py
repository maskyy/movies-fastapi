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
    video_link: str | None
    genre: list[str]


class FilmCreate(FilmBase):
    poster_image: str | None
    background_image: str | None
    background_color: str | None
    preview_video_link: str | None
    description: str
    director: str
    starring: list[str]
    run_time: int
    released: int
    imdb_id: str
    status: str


class Film(FilmBase):
    pass


class Favorite(BaseModel):
    pass


class CommentBase(BaseModel):
    pass


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    pass
