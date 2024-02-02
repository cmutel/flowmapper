from flowmapper.utils import read_migration_files

def test_read_single_migration_file(snapshot):
    actual = read_migration_files("tests/data/migrations.json")
    assert actual == snapshot

def test_read_multiple_migration_files(snapshot):
    actual = read_migration_files(
        "tests/data/migrations.json", "tests/data/transformations.json"
    )
    expected = snapshot
    assert actual == expected
