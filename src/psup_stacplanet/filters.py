import re
from typing import Literal

from psup_stacplanet.entities import InventoryLine

type FileExtension = Literal[
    "",
    "nc",
    "bat",
    "xml",
    "cpp",
    "hdr",
    "sh",
    "c",
    "cfg",
    "png",
    "fits",
    "shx",
    "shp",
    "ptif",
    "cub",
    "patch",
    "dox",
    "DS_Store",
    "txt",
    "tif",
    "ORIG",
    "bad",
    "conf",
    "prj",
    "orig",
    "py",
    "old",
    "dbf",
    "sav",
    "json",
    "sql",
    "lbl",
    "img",
]


class InventoryLineFilter:
    def __init__(
        self,
        name_pattern: str | re.Pattern | None = None,
        category: Literal["omegacubes", "marsdata"] | None = None,
        file_extension: FileExtension | None = None,
    ):
        if isinstance(name_pattern, str):
            name_pattern = re.compile(re.escape(name_pattern))

        self.name_pattern = name_pattern
        self.category = category
        self.file_extension = file_extension

    def __call__(self, line: InventoryLine) -> InventoryLine | None:
        if (
            self.name_pattern is not None
            and self.name_pattern.search(line.file_name) is None
        ):
            return None

        # Filter by category
        if self.category is not None and self.category != line.category:
            return None

        # Filter by file extension
        if (
            self.file_extension is not None
            and self.file_extension != line.file_extension
        ):
            return None

        return line
