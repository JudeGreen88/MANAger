import pytest

from manager.catalogue import load_catalogue
from manager.filters import (
    Restrictions,
    allowed_ingredients,
    filter_recipes,
    recipe_violations,
)

CAT = load_catalogue()  # test data (labelled is_test_data)


def test_allergen_removes_ingredients():
    ok = allowed_ingredients(CAT, Restrictions(allergens=frozenset({"gluten", "nuts"})))
    assert "pasta" not in ok and "peanut_butter" not in ok
    assert "rice" in ok


def test_every_allergen_filter_leaves_no_conflict():
    for a in ["gluten", "dairy", "nuts", "eggs", "soy"]:
        ok = allowed_ingredients(CAT, Restrictions(allergens=frozenset({a})))
        assert all(a not in ing.allergens for ing in ok.values())


def test_vegetarian_and_vegan():
    veg = allowed_ingredients(CAT, Restrictions(vegetarian=True))
    assert "chicken_breast" not in veg and "tuna_can" not in veg
    assert "eggs" in veg and "milk" in veg
    vegan = allowed_ingredients(CAT, Restrictions(vegan=True))
    assert all(not i.is_animal_product for i in vegan.values())
    assert "tofu" in vegan


def test_kosher_rejects_meat_plus_dairy_recipe():
    r = Restrictions(kosher=True)
    assert "kashrut:meat_and_dairy" in recipe_violations(
        ["chicken_breast", "milk"], CAT, r
    )
    # Same recipe is fine when kashrut is not requested.
    assert recipe_violations(["chicken_breast", "milk"], CAT, Restrictions()) == []
    # Meat + pareve and dairy + pareve are fine.
    assert recipe_violations(["chicken_breast", "rice"], CAT, r) == []
    assert recipe_violations(["cottage", "bread"], CAT, r) == []


def test_unknown_ingredient_is_reported():
    assert recipe_violations(["unicorn"], CAT, Restrictions()) == ["unknown:unicorn"]


def test_invalid_allergen_rejected():
    with pytest.raises(ValueError):
        Restrictions(allergens=frozenset({"pollen"}))


def test_filter_recipes_has_no_conflicts_over_combinations():
    recipes = {
        "pasta_chicken": ["pasta", "chicken_breast", "tomato"],
        "omelette": ["eggs", "onion", "tomato"],
        "chicken_milk": ["chicken_breast", "milk"],
        "tofu_rice": ["tofu", "rice", "cucumber"],
        "hummus_bread": ["chickpeas_can", "tahini", "bread"],
    }
    combos = [
        Restrictions(allergens=frozenset({"gluten"})),
        Restrictions(allergens=frozenset({"eggs", "soy"})),
        Restrictions(vegetarian=True),
        Restrictions(vegan=True),
        Restrictions(kosher=True),
        Restrictions(vegan=True, allergens=frozenset({"gluten"}), kosher=True),
    ]
    for r in combos:
        for name, ids in filter_recipes(recipes, CAT, r).items():
            assert recipe_violations(ids, CAT, r) == [], (name, r)
    assert set(filter_recipes(recipes, CAT, Restrictions(vegan=True))) == {
        "tofu_rice",
        "hummus_bread",
    }
    assert "chicken_milk" not in filter_recipes(recipes, CAT, Restrictions(kosher=True))
