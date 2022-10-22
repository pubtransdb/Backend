from fastapi import FastAPI

from ..settings import settings


app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    description=settings.description,
    version=settings.version,
)
