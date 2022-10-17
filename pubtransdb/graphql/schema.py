from strawberry import Schema

from .query import Query


schema = Schema(query=Query)
