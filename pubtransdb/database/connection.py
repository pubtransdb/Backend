from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pubtransdb.settings import settings


engine = create_engine(settings.postgres_dsn, echo=settings.debug)
make_session = sessionmaker(engine)
