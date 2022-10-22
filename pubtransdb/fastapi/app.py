from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from strawberry.fastapi import GraphQLRouter

from pubtransdb.graphql.schema import schema

from ..settings import settings
from .dependencies import get_graphql_context


app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    description=settings.description,
    version=settings.version,
)

graphql_router = GraphQLRouter(
    schema=schema,
    debug=settings.debug,
    context_getter=get_graphql_context,
)
app.include_router(graphql_router, prefix="/graphql")


@app.get("/")
def get_index():
    return RedirectResponse("/graphql")
