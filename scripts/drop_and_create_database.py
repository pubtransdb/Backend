from pubtransdb.database.models import Base


def drop_and_create_database():
    from pubtransdb.database.connection import engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    drop_and_create_database()
