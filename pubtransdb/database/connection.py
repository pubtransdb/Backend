from sqlalchemy import create_engine

from pubtransdb.settings import settings


engine = create_engine(settings.postgres_dsn, echo=settings.debug)
