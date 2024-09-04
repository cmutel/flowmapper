import bw_simapro_csv
from pathlib import Path
from loguru import logger
import json


def is_simapro_csv_file(fp: Path) -> bool:
    if not fp.is_file() or not fp.suffix.lower() == ".csv":
        return False
    try:
        bw_simapro_csv.header.parse_header(open(fp, encoding="sloppy-windows-1252"))[
            0
        ].project
        return True
    except:
        logger.critical("Skipping {a} as we can't read it as a SimaPro file", a=fp.name)
        return False


def simapro_csv_biosphere_extractor(dirpath: Path, output_fp: Path) -> None:
    """Load all simapro files in directory `dirpath`, and extract all biosphere flows"""
    simapro_files = [fp for fp in sorted(dirpath.iterdir()) if is_simapro_csv_file(fp)]

    flows = set()

    for fp in simapro_files:
        sp = bw_simapro_csv.SimaProCSV(
            fp, stderr_logs=False, write_logs=False, copy_logs=False
        )
        for process in filter(
            lambda x: isinstance(x, bw_simapro_csv.blocks.Process),
            sp.blocks,
        ):
            for block in filter(
                lambda x: isinstance(x, bw_simapro_csv.blocks.GenericUncertainBiosphere),
                process.blocks.values(),
            ):
                for line in block.parsed:
                    flows.add((line["context"], line["name"], line["unit"]))

    with open(output_fp, "w") as f:
        json.dump(
            [{"context": c, "name": n, "unit": u} for c, n, u in sorted(flows)],
            f,
            indent=2,
            ensure_ascii=False,
        )
