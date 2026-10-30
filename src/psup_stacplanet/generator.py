import json
from pathlib import Path

from stac_pydantic import Catalog

from psup_stacplanet import MANIFEST_FILES
from psup_stacplanet.inventory import PsupInventory


class CatalogGenerator:
    def _generate_catalog(self, root_catalog: Path):
        catalog_obj = json.loads((MANIFEST_FILES / "catalog.json").read_text("utf-8"))
        catalog_obj["type"] = "Catalog"
        catalog_obj["stac_version"] = "1.1.0"
        catalog = Catalog.model_validate(catalog_obj)

        root_catalog.write_text(json.dumps(catalog.model_dump(), indent=2))

    def __init__(self, inventory: PsupInventory, root_catalog: Path):
        self.inventory = inventory
        if not root_catalog.exists():
            self._generate_catalog(root_catalog)
        self.root_catalog = root_catalog
