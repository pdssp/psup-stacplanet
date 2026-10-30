from pathlib import Path

from psup_stacplanet.generator import CatalogGenerator
from psup_stacplanet.inventory import PsupInventory


def read_inventory(inventory_file: Path):
    inventory = PsupInventory(inventory_file)
    inventory.read_all()


def create_catalog(inventory_file: Path, root_catalog: Path):
    generator = CatalogGenerator(PsupInventory(inventory_file), root_catalog)
    print(generator)
