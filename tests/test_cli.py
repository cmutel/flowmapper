from typer.testing import CliRunner
from flowmapper.cli import app
import json
import pandas as pd

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.output.startswith("flowmapper, version")


def test_format_glad(tmp_path):
    result = runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei-3.7.json",
            "--format",
            "glad",
            "--fields",
            "tests/data/field_mapping-sp-ei.py",
            "--output-dir",
            str(tmp_path),
        ],
    )
    expected_files = sorted(
        [
            tmp_path / "sp-ei-3.7.xlsx",
            tmp_path / "sp-ei-3.7-unmatched-source.json",
            tmp_path / "sp-ei-3.7-unmatched-target.json",
        ]
    )

    files = sorted(tmp_path.glob("**/*"))

    assert result.exit_code == 0
    assert expected_files == files


def test_format_randonneur(tmp_path):
    result = runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei-3.7.json",
            "--format",
            "randonneur",
            "--fields",
            "tests/data/field_mapping-sp-ei.py",
            "--output-dir",
            str(tmp_path),
        ],
    )
    expected_files = sorted(
        [
            tmp_path / "sp-ei-3.7.json",
            tmp_path / "sp-ei-3.7-unmatched-source.json",
            tmp_path / "sp-ei-3.7-unmatched-target.json",
        ]
    )

    files = sorted(tmp_path.glob("**/*"))

    assert result.exit_code == 0
    assert expected_files == files


def test_matched_flows(tmp_path, snapshot):
    runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei-3.7.json",
            "--matched-source",
            "--matched-target",
            "--fields",
            "tests/data/field_mapping-sp-ei.py",
            "--output-dir",
            str(tmp_path),
        ],
    )

    with open(tmp_path / "sp-ei-3.7-matched-source.json") as fs:
        actual = json.load(fs)

    assert actual == snapshot


def test_matched_flows_with_randonneur_transformations(tmp_path, snapshot):
    runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei-3.7.json",
            "--transformations",
            "tests/data/transformations.json",
            "--matched-source",
            "--matched-target",
            "--fields",
            "tests/data/field_mapping-sp-ei.py",
            "--output-dir",
            str(tmp_path),
        ],
    )

    with open(tmp_path / "sp-ei-3.7-matched-source.json") as fs:
        actual = json.load(fs)

    assert actual == snapshot


def test_matched_flows_with_multiple_randonneur_transformations(tmp_path, snapshot):
    runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei-3.7.json",
            "--transformations",
            "tests/data/transformations.json",
            "--transformations",
            "tests/data/migrations.json",
            "--matched-source",
            "--matched-target",
            "--fields",
            "tests/data/field_mapping-sp-ei.py",
            "--output-dir",
            str(tmp_path),
        ],
    )

    with open(tmp_path / "sp-ei-3.7-matched-source.json") as fs:
        actual = json.load(fs)

    assert actual == snapshot
