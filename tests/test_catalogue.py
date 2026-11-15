import pytest

from manager.catalogue import CatalogueError, load_catalogue, unmatched_ids, DEFAULT_PATH


def test_default_catalogue_loads_and_is_labelled_test():
    cat = load_catalogue()
    assert len(cat) >= 10
    # Non-negotiable rule: test data is always labelled.
    assert all(i.is_test_data for i in cat.values())


def test_all_entries_have_nutrition_and_packages():
    for ing in load_catalogue().values():
        assert ing.package_size > 0
        assert ing.kcal_100g >= 0 and ing.protein_100g >= 0


def test_allergen_and_kashrut_tags_are_consistent():
    cat = load_catalogue()
    assert "dairy" in cat["milk"].allergens and cat["milk"].kashrut == "dairy"
    assert cat["chicken_breast"].kashrut == "meat"
    assert "gluten" in cat["pasta"].allergens


def test_unmatched_ids():
    cat = load_catalogue()
    assert unmatched_ids(["pasta", "unicorn"], cat) == ["unicorn"]


def test_duplicate_id_rejected(tmp_path):
    lines = DEFAULT_PATH.read_text(encoding="utf-8").splitlines()
    p = tmp_path / "c.csv"
    p.write_text("\n".join(lines + [lines[1]]), encoding="utf-8")
    with pytest.raises(CatalogueError):
        load_catalogue(p)


def test_unknown_allergen_rejected(tmp_path):
    lines = DEFAULT_PATH.read_text(encoding="utf-8").splitlines()
    p = tmp_path / "c.csv"
    p.write_text("\n".join([lines[0], lines[1].replace("gluten", "sesame")]), encoding="utf-8")
    with pytest.raises(CatalogueError):
        load_catalogue(p)
