import csv
import re
from pathlib import Path

from psup_stacplanet.entities import InventoryLine


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

    def find(self, file_match: str | re.Pattern) -> InventoryLine | set[InventoryLine]:
        inventory_lines = set()

        with open(self.csv_file, newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)

            for row in reader:
                curr_line = InventoryLine.model_validate(
                    {k: v for k, v in zip(headers, row)}
                )
                if (
                    (
                        isinstance(file_match, re.Pattern)
                        and file_match.search(curr_line.file_name) is not None
                    )
                    or isinstance(file_match, str)
                    and curr_line.file_name == file_match
                ):
                    inventory_lines.add(curr_line)

        if len(inventory_lines) == 1:
            return inventory_lines.pop()

        return inventory_lines
