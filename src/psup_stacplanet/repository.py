import json
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

from psup_stacplanet import MANIFEST_FILES
from psup_stacplanet.compat.stac_pydantic import (
    Asset,
    Band,
    Catalog,
    Collection,
    Item,
    Link,
    Links,
)
from psup_stacplanet.io import load_item

I = TypeVar("I", bound=Catalog | Collection | Item)
M = TypeVar("M", bound=Asset | Band)
S = TypeVar("S", bound=Catalog | Collection | Item | Asset | Band)


class BaseRepository[I: Catalog | Collection | Item](ABC):
    """Repository structure for STAC objects"""

    @abstractmethod
    def __init__(self, parent: I, parent_path: Path):
        if not parent_path.exists():
            raise FileNotFoundError(f"{parent_path} not found.")
        self._parent = parent
        self._parent_path = parent_path

    @abstractmethod
    def add_item(self, item: S, item_path: Path): ...

    @abstractmethod
    def remove_item(self, item_path: Path) -> I: ...

    @abstractmethod
    def modify_item(self, item: S, item_path: Path) -> I: ...

    @abstractmethod
    def get_item(self, item_path: Path) -> I: ...

    def sanity_check(self):
        if len([link for link in self._parent.links if link.rel == "parent"]) > 1:
            raise ValueError("No more than one parent per link")

        # Remove duplicate links
        seen = set()
        clean_links = []
        for link in self._parent.links:
            key = (link.rel, link.href)
            if key not in seen:
                seen.add(key)
                clean_links.append(link)

        self._parent.links = Links(clean_links)

    def refresh(self):
        """Rewrites parent when child is added"""
        self._parent_path.write_text(json.dumps(self._parent.model_dump(), indent=2))

    @property
    def namespace(self) -> Path:
        """Returns the namespace of the repository minus the file

        Returns:
            Path: Path of the namespace, used as a base
        """
        return self._parent_path.parent

    @property
    def children(self) -> list[Path]:
        """Retrieves the absolute path of the repository's direct children

        Returns:
            list[Path]: _description_
        """
        return [
            self.namespace / Path(link.href)
            for link in self._parent.links
            if link.rel == "child"
        ]


class RootCatalogRepository(BaseRepository):
    def _generate_catalog(self, root_catalog: Path, base_url: str | None = None):
        """If no catalog is present, generates one

        Args:
            root_catalog (Path): _description_
            base_url (str | None, optional): _description_. Defaults to None.
        """
        catalog_obj = json.loads((MANIFEST_FILES / "catalog.json").read_text("utf-8"))
        catalog_obj["type"] = "Catalog"
        catalog_obj["stac_version"] = "1.1.0"
        catalog = Catalog.model_validate(catalog_obj)
        catalog.links.append(
            Link.model_validate(
                {"rel": "root", "href": "./catalog.json", "type": "application/json"}
            )
        )
        # Absolute URL
        if base_url is not None:
            catalog.links.append(
                Link.model_validate(
                    {
                        "rel": "self",
                        "href": base_url + "/catalog.json",
                        "type": "application/json",
                    }
                )
            )

        root_catalog.write_text(json.dumps(catalog.model_dump(), indent=2))

    def __init__(
        self,
        root_catalog_path: Path,
        catalog: Catalog | None = None,
        base_url: str | None = None,
    ):
        if catalog is None:
            catalog = self._generate_catalog(
                root_catalog=root_catalog_path, base_url=base_url
            )
        super().__init__(catalog, root_catalog_path)
        self.sanity_check()

    @property
    def catalog(self) -> Catalog:
        return self._parent

    @catalog.setter
    def catalog(self, v: Catalog):
        self._parent = v

    def add_item(self, item: S, item_path: Path):
        # Mutual linking
        if isinstance(item, (Catalog, Collection, Item)) and not any(
            link.rel == "parent" for link in item.links
        ):
            # Item has no parent
            item.links.append(
                Link(
                    rel="parent",
                    href=self._parent_path.relative_to(item_path).as_posix(),
                    type="application/json",
                )
            )

        # Register item as child
        item_id = item_path.relative_to(self._parent_path.parent).as_posix()
        # Add item to links
        if item_id not in self.catalog.links.unique_links():
            if isinstance(item, (Catalog, Collection, Item)):
                title = item.title
            else:
                title = None
            self.catalog.links.append(
                Link(
                    rel="child",
                    href=item_path.relative_to(self._parent_path.parent).as_posix(),
                    type="application/json",
                    title=title,
                )
            )

        # Write item
        item_path.touch(exist_ok=True)
        item_path.write_text(json.dumps(item.model_dump(), indent=2))

        self.refresh()

    def get_item(self, item_path: Path) -> I:
        if not item_path.exists():
            raise ValueError()

        return load_item(item_path=item_path)  # ty: ignore[invalid-return-type]

    def remove_item(self, item_path: Path) -> I:
        item_to_delete = self.get_item(item_path)
        # Unlink from catalog
        self.catalog.links = Links(
            [link for link in self.catalog.links if link.href != item_path.as_posix()]
        )

        # Delete the namespace
        shutil.rmtree(item_path.parent)

        self.refresh()

        return item_to_delete

    def modify_item(self, item: S, item_path: Path) -> I:
        item_to_modify = load_item(item_path)
        modified = item_to_modify.model_copy(update=item.model_dump())
        item_path.write_text(json.dumps(modified.model_dump(), indent=2))
        return modified  # ty: ignore[invalid-return-type]


class CatalogRepository(BaseRepository):
    def __init__(self, catalog_path: Path, catalog: Catalog | None = None):
        super().__init__(catalog, catalog_path)
        self.sanity_check()

    def add_item(self, item: S, item_path: Path):
        pass


class CollectionRepository(BaseRepository):
    def __init__(self):
        pass
