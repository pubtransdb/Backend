from sqlalchemy import create_mock_engine

from pubtransdb.database.models import Base


def test_ddl_snapshot(snapshot):
    results = list[str]()

    def dump(sql, *multiparams, **params):
        ddl = sql.compile(dialect=engine.dialect)
        results.append(str(ddl))

    engine = create_mock_engine("postgresql://", dump)  # type: ignore
    Base.metadata.create_all(engine)

    result = "".join(results).strip() + "\n"

    snapshot.snapshot_dir = "./snapshots/database"
    snapshot.assert_match(result, "schema.sql")
