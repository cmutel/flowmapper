import typer
from typing_extensions import Annotated
from pathlib import Path
import logging
from typing import Optional
from typing_extensions import Annotated
import importlib.metadata
import logging
import json
from pathlib import Path
from enum import Enum
from randonneur import migrate_datasets
from .flow import Flow
from .utils import read_field_mapping, read_flowlist, read_migration_files
from .flowmap import Flowmap
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

logger = logging.getLogger(__name__)

app = typer.Typer()

def version_callback(value: bool):
    if value:
        print(f"flowmapper, version {importlib.metadata.version('flowmapper')}")
        raise typer.Exit()

class OutputFormat(str, Enum):
    all = 'all'
    glad = 'glad'
    randonneur = 'randonneur'

@app.callback()
def main(version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,):
    """
    Generate mappings between elementary flows lists
    """

@app.command()
def map(
    source: Annotated[Path, typer.Argument(help='Path to source flowlist')],
    target: Annotated[Path, typer.Argument(help='Path to target flowlist')],
    fields: Annotated[Path, typer.Option(help='Relationship between fields in source and target flowlists')],
    output_dir: Annotated[Path, typer.Option(help='Directory to save mapping and diagnostics files')] = Path('.'),
    format: Annotated[OutputFormat, typer.Option(help='Mapping file output format', case_sensitive=False)] = 'all',
    transformations: Annotated[list[Path], typer.Option("--transformations", "-t", help='Randonneur data migration file with changes to be applied to source flows before matching')] = None,
    unmatched_source: Annotated[bool, typer.Option(help='Write original source unmatched flows into separate file?')] = True,
    unmatched_target: Annotated[bool, typer.Option(help='Write original target unmatched flows into separate file?')] = True,
    matched_source: Annotated[bool, typer.Option(help='Write original source matched flows into separate file?')] = False,
    matched_target: Annotated[bool, typer.Option(help='Write original target matched flows into separate file?')] = False,
):
    """
    Generate mappings between elementary flows lists
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    field_mapping = read_field_mapping(fields)
    if transformations:
            transformations = read_migration_files(*transformations)
    source_flows = [Flow(flow, field_mapping['source'], transformations) for flow in read_flowlist(source)]
    target_flows = [Flow(flow, field_mapping['target']) for flow in read_flowlist(target)]

    flowmap = Flowmap(source_flows, target_flows)
    flowmap.statistics()

    stem = f'{source.stem}-{target.stem}'

    if matched_source:
        with open(output_dir / f'{stem}-matched-source.json', 'w') as fs:
            json.dump([flow.raw for flow in flowmap.matched_source], fs, indent=True)

    if unmatched_source:
        with open(output_dir / f'{stem}-unmatched-source.json', 'w') as fs:
            json.dump([flow.raw for flow in flowmap.unmatched_source], fs, indent=True)

    if matched_target:
        with open(output_dir / f'{stem}-matched-target.json', 'w') as fs:
            json.dump([flow.raw for flow in flowmap.matched_target], fs, indent=True)

    if unmatched_target:
        with open(output_dir / f'{stem}-unmatched-target.json', 'w') as fs:
            json.dump([flow.raw for flow in flowmap.unmatched_target], fs, indent=True)

    if format.value == 'randonneur':
        flowmap.to_randonneur(output_dir / f'{stem}.json')
    elif format.value == 'glad':
        flowmap.to_glad(output_dir / f'{stem}.xlsx')
    else:
        flowmap.to_randonneur(output_dir / f'{stem}.json')
        flowmap.to_glad(output_dir / f'{stem}.xlsx')
