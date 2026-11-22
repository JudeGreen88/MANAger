"""Sensitivity, diet and kashrut filters (completion criterion 6).

Pure code, no AI: filtering happens before recipes ever reach the AI.
Product certification is not verified; the UI must tell the user to check
the product label.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, List

from .catalogue import ALLERGENS, Ingredient


@dataclass(frozen=True)
class Restrictions:
    allergens: FrozenSet[str] = frozenset()  # subset of catalogue.ALLERGENS
    vegetarian: bool = False
    vegan: bool = False
    kosher: bool = False

    def __post_init__(self) -> None:
        unknown = set(self.allergens) - ALLERGENS
        if unknown:
            raise ValueError(f"unknown allergens {sorted(unknown)}")


def ingredient_violations(ing: Ingredient, r: Restrictions) -> List[str]:
    """Reasons this single ingredient conflicts with the restrictions."""
    reasons: List[str] = []
    for a in sorted(ing.allergens & r.allergens):
        reasons.append(f"allergen:{a}")
    if (r.vegetarian or r.vegan) and ing.is_meat_or_fish:
        reasons.append("diet:vegetarian")
    if r.vegan and ing.is_animal_product:
        reasons.append("diet:vegan")
    if r.kosher and ing.non_kosher:
        reasons.append("kashrut:non_kosher")
    return reasons


def allowed_ingredients(
    catalogue: Dict[str, Ingredient], r: Restrictions
) -> Dict[str, Ingredient]:
    """Catalogue subset that conflicts with nothing in the restrictions."""
    return {i: ing for i, ing in catalogue.items() if not ingredient_violations(ing, r)}


def recipe_violations(
    ingredient_ids: Iterable[str],
    catalogue: Dict[str, Ingredient],
    r: Restrictions,
) -> List[str]:
    """Reasons a recipe (list of ingredient ids) conflicts with the restrictions.

    Unknown ids are reported too (criterion 2: 0 unmatched). With kosher=True
    a recipe mixing a meat and a dairy ingredient is rejected.
    """
    ids = list(ingredient_ids)
    reasons: List[str] = []
    for i in ids:
        ing = catalogue.get(i)
        if ing is None:
            reasons.append(f"unknown:{i}")
            continue
        reasons.extend(f"{i}:{v}" for v in ingredient_violations(ing, r))
    if r.kosher:
        kinds = {catalogue[i].kashrut for i in ids if i in catalogue}
        if {"meat", "dairy"} <= kinds:
            reasons.append("kashrut:meat_and_dairy")
    return reasons


def filter_recipes(
    recipes: Dict[str, List[str]],
    catalogue: Dict[str, Ingredient],
    r: Restrictions,
) -> Dict[str, List[str]]:
    """Keep only recipes ({name: [ingredient ids]}) with no violation."""
    return {
        name: ids
        for name, ids in recipes.items()
        if not recipe_violations(ids, catalogue, r)
    }
