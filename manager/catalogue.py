"""Ingredient catalogue: loading and validation.

The catalogue is the single source of truth for ingredients, tags, nutrition
and package sizes. The AI may only reference ingredient ids from here.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, FrozenSet, List

ALLERGENS = {"gluten", "dairy", "nuts", "eggs", "soy"}
KASHRUT_KINDS = {"meat", "dairy", "pareve"}
CHAINS = ("shufersal", "rami_levy", "osher_ad")

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "catalogue.csv"


class CatalogueError(ValueError):
    pass


@dataclass(frozen=True)
class Ingredient:
    id: str
    name_en: str
    name_he: str
    category: str
    allergens: FrozenSet[str]
    kashrut: str  # meat / dairy / pareve
    non_kosher: bool  # e.g. pork, seafood
    is_meat_or_fish: bool  # for vegetarian / vegan filtering
    is_animal_product: bool  # for vegan filtering
    kcal_100g: float
    protein_100g: float
    carbs_100g: float
    fat_100g: float
    package_size: float
    package_unit: str  # g / ml / unit
    pantry_staple: bool  # excluded from shopping list
    product_codes: Dict[str, str]  # chain -> barcode/item code ("" = unmapped)
    is_test_data: bool


def _bool(v: str) -> bool:
    return v.strip().lower() in {"1", "true", "yes"}


def _parse_row(row: Dict[str, str]) -> Ingredient:
    allergens = frozenset(a for a in row["allergens"].split("|") if a)
    unknown = allergens - ALLERGENS
    if unknown:
        raise CatalogueError(f"{row['id']}: unknown allergen tags {sorted(unknown)}")
    if row["kashrut"] not in KASHRUT_KINDS:
        raise CatalogueError(f"{row['id']}: kashrut must be one of {sorted(KASHRUT_KINDS)}")
    try:
        ing = Ingredient(
            id=row["id"],
            name_en=row["name_en"],
            name_he=row["name_he"],
            category=row["category"],
            allergens=allergens,
            kashrut=row["kashrut"],
            non_kosher=_bool(row["non_kosher"]),
            is_meat_or_fish=_bool(row["is_meat_or_fish"]),
            is_animal_product=_bool(row["is_animal_product"]),
            kcal_100g=float(row["kcal_100g"]),
            protein_100g=float(row["protein_100g"]),
            carbs_100g=float(row["carbs_100g"]),
            fat_100g=float(row["fat_100g"]),
            package_size=float(row["package_size"]),
            package_unit=row["package_unit"],
            pantry_staple=_bool(row["pantry_staple"]),
            product_codes={c: row.get(f"code_{c}", "").strip() for c in CHAINS},
            is_test_data=_bool(row["is_test_data"]),
        )
    except (KeyError, ValueError) as e:
        raise CatalogueError(f"{row.get('id', '?')}: bad or missing field ({e})") from e
    if ing.package_size <= 0:
        raise CatalogueError(f"{ing.id}: package_size must be > 0")
    if ing.package_unit not in {"g", "ml", "unit"}:
        raise CatalogueError(f"{ing.id}: package_unit must be g, ml or unit")
    return ing


def load_catalogue(path: Path = DEFAULT_PATH) -> Dict[str, Ingredient]:
    """Load and validate the catalogue, returning {id: Ingredient}."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    catalogue: Dict[str, Ingredient] = {}
    for row in rows:
        ing = _parse_row(row)
        if ing.id in catalogue:
            raise CatalogueError(f"duplicate id {ing.id}")
        catalogue[ing.id] = ing
    if not catalogue:
        raise CatalogueError("catalogue is empty")
    return catalogue


def unmatched_ids(ids: List[str], catalogue: Dict[str, Ingredient]) -> List[str]:
    """Ids not in the catalogue (completion criterion 2: must be empty)."""
    return [i for i in ids if i not in catalogue]
