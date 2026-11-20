from pathlib import Path

from psup_stacplanet.inventory import PsupInventory
from psup_stacplanet.repository import RootCatalogRepository


def read_inventory(inventory_file: Path):
    inventory = PsupInventory(inventory_file)
    inventory.read_all()


def create_catalog(inventory_file: Path, root_catalog: Path):
    generator = RootCatalogRepository(PsupInventory(inventory_file), root_catalog)
    print(generator)
