from pathlib import Path

from psup_stacplanet.compat.stac_pydantic import Item
from psup_stacplanet.entities import InventoryLine


class OmegaItem:
    def __init__(self, data: InventoryLine):
        self.data = data

    def get_item(self, root_catalog_file: Path) -> Item: ...
