import csv
import re
from pathlib import Path
from typing import Literal

from psup_stacplanet.entities import InventoryLine
from psup_stacplanet.filters import FileExtension, InventoryLineFilter


class PsupInventory:
    """Data Loader for PSUP items"""

    def __init__(self, csv_file: Path):
        self.csv_file = csv_file

    def __str__(self) -> str:
        return f"PsupInventory - source: {self.csv_file}"

    def read_all(self):
        with open(self.csv_file, newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)

            for row in reader:
                print(
                    InventoryLine.model_validate({k: v for k, v in zip(headers, row)})
                )

    def find(
        self,
        file_match: str | re.Pattern,
        category: Literal["omegacubes", "marsdata"] | None = None,
        file_extension: FileExtension | None = None,
    ) -> InventoryLine | set[InventoryLine]:
        inventory_lines = set()
        line_filter = InventoryLineFilter(
            file_match, category=category, file_extension=file_extension
        )

        with open(self.csv_file, newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)

            for row in reader:
                curr_line = InventoryLine.model_validate(
                    {k: v for k, v in zip(headers, row)}
                )
                if line_filter(curr_line) is not None:
                    inventory_lines.add(curr_line)

        if len(inventory_lines) == 1:
            return inventory_lines.pop()

        return inventory_lines
