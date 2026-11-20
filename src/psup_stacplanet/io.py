import json
from pathlib import Path

from psup_stacplanet.compat.stac_pydantic import Catalog, Collection, Item


def load_item(item_path: Path) -> Catalog | Collection | Item:
    item_obj = json.loads(item_path.read_text())

    item_obj_type = item_obj.get("type", "")

    if item_obj_type == "Feature":
        return Item.model_validate(item_obj)
    elif item_obj_type == "Collection":
        return Collection.model_validate(item_obj)
    elif item_obj_type == "Catalog":
        return Catalog.model_validate(item_obj)

    raise ValueError(
        "Couldn't recognize `type` from the item JSON. Must be either 'Feature', 'Collection' or 'Catalog'"
    )
