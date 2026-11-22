from unittest.mock import Mock

import pytest

from bun import Bun
from burger import Burger
from data import BUN_DATA, INGREDIENTS_DATA
from ingredient import Ingredient


@pytest.fixture
def new_burger():
    return Burger()


@pytest.fixture
def bun_in_burger():
    bun = Mock(spec_set=Bun)
    bun.get_price.return_value = BUN_DATA["price"]
    bun.get_name.return_value = BUN_DATA["name"]
    return bun


@pytest.fixture
def ingredients_in_burger():
    ingredients = []
    for data in INGREDIENTS_DATA:
        ingredient = Mock(spec_set=Ingredient)
        ingredient.get_type.return_value = data["type"]
        ingredient.get_name.return_value = data["name"]
        ingredient.get_price.return_value = data["price"]
        ingredients.append(ingredient)
    return ingredients


@pytest.fixture
def make_burger(bun_in_burger, ingredients_in_burger):
    def create(ingredient_indices=()):
        burger = Burger()
        burger.set_buns(bun_in_burger)
        for index in ingredient_indices:
            burger.add_ingredient(ingredients_in_burger[index])
        return burger

    return create
