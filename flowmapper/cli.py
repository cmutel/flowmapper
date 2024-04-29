import importlib.metadata
import json
import logging
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from .flow import Flow
from .flowmap import Flowmap
from .transformation_mapping import prepare_transformations
from .utils import load_standard_transformations, read_migration_files

logger = logging.getLogger(__name__)

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"flowmapper, version {importlib.metadata.version('flowmapper')}")
        raise typer.Exit()


class OutputFormat(str, Enum):
    all = "all"
    glad = "glad"
    randonneur = "randonneur"


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
):
    """
    Generate mappings between elementary flows lists
    """


@app.command()
def map(
    source: Annotated[Path, typer.Argument(help="Path to source flowlist")],
    target: Annotated[Path, typer.Argument(help="Path to target flowlist")],
    output_dir: Annotated[
        Path, typer.Option(help="Directory to save mapping and diagnostics files")
    ] = Path("."),
    format: Annotated[
        OutputFormat,
        typer.Option(help="Mapping file output format", case_sensitive=False),
    ] = "all",
    default_transformations: Annotated[
        bool, typer.Option(help="Include default context and unit transformations?")
    ] = True,
    transformations: Annotated[
        Optional[list[Path]],
        typer.Option(
            "--transformations",
            "-t",
            help="Randonneur data migration file with changes to be applied to source flows before matching. Can be included multiple times.",
        ),
    ] = None,
    unmatched_source: Annotated[
        bool,
        typer.Option(help="Write original source unmatched flows into separate file?"),
    ] = True,
    unmatched_target: Annotated[
        bool,
        typer.Option(help="Write original target unmatched flows into separate file?"),
    ] = True,
    matched_source: Annotated[
        bool,
        typer.Option(help="Write original source matched flows into separate file?"),
    ] = False,
    matched_target: Annotated[
        bool,
        typer.Option(help="Write original target matched flows into separate file?"),
    ] = False,
):
    """
    Generate mappings between elementary flows lists
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    loaded_transformations = []
    if default_transformations:
        loaded_transformations.extend(load_standard_transformations())
    if transformations:
        loaded_transformations.extend(read_migration_files(*transformations))

    prepared_transformations = prepare_transformations(loaded_transformations)

    source_flows = [
        Flow(flow, prepared_transformations) for flow in json.load(open(source))
    ]
    source_flows = [flow for flow in source_flows if not flow.missing]
    target_flows = [
        Flow(flow, prepared_transformations) for flow in json.load(open(target))
    ]

    flowmap = Flowmap(source_flows, target_flows)
    flowmap.statistics()

    stem = f"{source.stem}-{target.stem}"

    if matched_source:
        with open(output_dir / f"{stem}-matched-source.json", "w") as fs:
            json.dump([flow.export for flow in flowmap.matched_source], fs, indent=True)

    if unmatched_source:
        with open(output_dir / f"{stem}-unmatched-source.json", "w") as fs:
            json.dump(
                [flow.export for flow in flowmap.unmatched_source], fs, indent=True
            )

    if matched_target:
        with open(output_dir / f"{stem}-matched-target.json", "w") as fs:
            json.dump([flow.export for flow in flowmap.matched_target], fs, indent=True)

    if unmatched_target:
        with open(output_dir / f"{stem}-unmatched-target.json", "w") as fs:
            json.dump(
                [flow.export for flow in flowmap.unmatched_target], fs, indent=True
            )

    if format.value == "randonneur":
        flowmap.to_randonneur(output_dir / f"{stem}.json")
    elif format.value == "glad":
        flowmap.to_glad(output_dir / f"{stem}.xlsx", missing_source=True)
    else:
        flowmap.to_randonneur(output_dir / f"{stem}.json")
        flowmap.to_glad(output_dir / f"{stem}.xlsx", missing_source=True)
