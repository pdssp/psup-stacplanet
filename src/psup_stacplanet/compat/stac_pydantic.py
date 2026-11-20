from collections.abc import Iterator
from enum import auto
from typing import Any, Self

from pydantic import ConfigDict, PrivateAttr, RootModel, model_validator
from stac_pydantic import Collection as OldCollection
from stac_pydantic import Item as OldItem
from stac_pydantic.catalog import Catalog as OldCatalog
from stac_pydantic.item import ItemProperties as OldItemProperties
from stac_pydantic.links import Link as OldLink
from stac_pydantic.shared import Asset as OldAsset
from stac_pydantic.shared import StacBaseModel
from stac_pydantic.shared import StacCommonMetadata as OldStacCommonMetadata
from stac_pydantic.utils import AutoValueEnum

STAC_VERSION = "1.1.0"


class NoDataTypes(str, AutoValueEnum):
    nan = auto()
    inf = auto()
    minus_inf = "-inf"


class DataTypes(str, AutoValueEnum):
    int8 = auto()
    int16 = auto()
    int32 = auto()
    int64 = auto()
    uint8 = auto()
    uint16 = auto()
    uint32 = auto()
    uint64 = auto()
    float16 = auto()
    float32 = auto()
    float64 = auto()
    cint16 = auto()
    cint32 = auto()
    cfloat32 = auto()
    cfloat64 = auto()
    other = auto()


class Band(StacBaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/commons/common-metadata.md#band-object
    """

    name: str | None = None
    description: str | None = None
    # For extensions related to bands
    model_config = ConfigDict(use_enum_values=True, extra="allow")


class Statistics(StacBaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/commons/common-metadata.md#statistics-object
    """

    minimum: float | None = None
    maximum: float | None = None
    mean: float | None = None
    stddev: float | None = None
    count: int | None = None
    valid_percent: float | None = None


class StacCommonMetadata(OldStacCommonMetadata):
    keywords: list[str] | None = None
    roles: list[str] | None = None
    # Bands
    bands: list[Band] | None = None
    # Data
    nodata: float | str | None = None
    data_type: str | None = None
    statistics: Statistics | None = None
    unit: str | None = None


class Link(OldLink):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/commons/links.md
    """

    method: str = "GET"
    headers: dict[str, str | list[str]] | None = None
    body: Any | None = None


class Links(RootModel[list[Link]]):
    root: list[Link]

    def link_iterator(self) -> Iterator[Link]:
        """Produce iterator to iterate through links"""
        return iter(self.root)

    def __iter__(self) -> Iterator[Link]:  # ty: ignore[invalid-method-override]
        return iter(self.root)

    def resolve(self, base_url: str) -> None:
        """resolve all links to the given base URL"""
        for link in self.link_iterator():
            link.resolve(base_url)

    def append(self, link: Link) -> None:
        self.root.append(link)

    def __len__(self) -> int:
        return len(self.root)

    def __getitem__(self, idx: int) -> Link:
        return self.root[idx]

    def unique_links(self) -> set[str]:
        return {link.href for link in self.root}


class ItemAsset(StacBaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/collection-spec/collection-spec.md#item-asset-definition-object
    """

    type: str | None = None
    title: str | None = None
    description: str | None = None
    roles: list[str] | None = None

    model_config = ConfigDict(
        populate_by_name=True, use_enum_values=True, extra="allow"
    )


class Catalog(OldCatalog):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/catalog-spec/catalog-spec.md
    """

    links: Links  # ty: ignore[invalid-attribute-override]


class Collection(OldCollection):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/collection-spec/collection-spec.md
    """

    item_assets: dict[str, ItemAsset] | None = None
    links: Links  # ty: ignore[invalid-attribute-override]


class ItemProperties(StacCommonMetadata, OldItemProperties):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/item-spec/item-spec.md#properties-object
    """

    model_config = ConfigDict(extra="allow")


class Asset(OldAsset):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/commons/assets.md#asset-object
    """

    _additional_fields: dict[str, Any] = PrivateAttr(default={})

    @model_validator(mode="after")
    def detect_additional_fields(self) -> Self:
        extra = self.__pydantic_extra__
        if extra is None:
            return self

        if extra.get("bands") is not None:
            extra["bands"] = [Band.model_validate(band) for band in extra["bands"]]

        self._additional_fields = extra

        return self


class Item(OldItem):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.1.0/item-spec/item-spec.md
    """

    properties: ItemProperties  # ty: ignore[invalid-mutable-override]
    assets: dict[str, Asset]  # ty: ignore[invalid-attribute-override]
    links: Links  # ty: ignore[invalid-attribute-override]
