from pubtransdb.graphql.schema import schema


def test_schema_snapshot(snapshot):
    snapshot.snapshot_dir = "./snapshots/graphql"
    snapshot.assert_match(f"{schema}\n", "schema.gql")
