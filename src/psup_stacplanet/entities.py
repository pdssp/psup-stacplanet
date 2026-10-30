from pathlib import Path

from pydantic import BaseModel
from pydantic_core import Url


class InventoryLine(BaseModel):
    file_name: Path
    href: Url
    rel_path: Path
    total_size: int

    @property
    def total_size_h(self) -> str:
        suffix: str = "B"
        num = float(self.total_size)
        for unit in ["", "Ki", "Mi", "Gi", "Ti"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f} {unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f} Ei{suffix}"

    @property
    def file_extension(self) -> str:
        return self.rel_path.suffix.lstrip(".")

    @property
    def category(self) -> str:
        return self.rel_path.as_posix().split("/")[0]

    @property
    def root(self) -> str:
        return self.rel_path.as_posix().split("/")[1]

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.file_name} ({self.total_size_h})"
