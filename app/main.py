import os

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine
from .internal import token
from .routers import comments, favorites, films, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api")
app.include_router(token.router, prefix="/api")
app.include_router(films.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")
app.include_router(comments.router, prefix="/api")


app.mount("/img", StaticFiles(directory="img"), name="img")