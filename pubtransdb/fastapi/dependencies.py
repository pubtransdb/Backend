from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from pubtransdb.database.connection import make_session
from pubtransdb.graphql.context import Context


def get_db_session() -> Iterator[Session]:
    with make_session() as session:
        yield session


def get_graphql_context(db_session: Session = Depends(get_db_session)) -> Context:
    return Context(db_session=db_session)
