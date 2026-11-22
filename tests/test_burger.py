import pytest

from data import BUN_DATA, INGREDIENTS_DATA


class TestBurger:

    def test_burger_without_ingredients_costs_only_two_buns(self, make_burger):
        burger = make_burger()

        assert burger.get_price() == 2 * BUN_DATA["price"]

    def test_set_buns_displays_bun_in_receipt(self, new_burger, bun_in_burger):
        new_burger.set_buns(bun_in_burger)

        bun_line = f'(==== {BUN_DATA["name"]} ====)'
        assert new_burger.get_receipt().splitlines()[:2] == [bun_line, bun_line]

    def test_add_ingredient_displays_both_ingredients_in_receipt(
        self, make_burger, ingredients_in_burger
    ):
        burger = make_burger()
        burger.add_ingredient(ingredients_in_burger[0])
        burger.add_ingredient(ingredients_in_burger[1])

        ingredient_lines = burger.get_receipt().splitlines()[1:-3]
        assert ingredient_lines == ["= sauce hot sauce =", "= filling cutlet ="]

    def test_remove_ingredient_leaves_other_ingredients_in_receipt(self, make_burger):
        burger = make_burger((0, 1, 2))
        burger.remove_ingredient(0)

        ingredient_lines = burger.get_receipt().splitlines()[1:-3]
        assert ingredient_lines == ["= filling cutlet =", "= filling shaverma ="]

    def test_move_ingredient_changes_order_in_receipt(self, make_burger):
        burger = make_burger((0, 1, 2))
        burger.move_ingredient(0, 1)

        ingredient_lines = burger.get_receipt().splitlines()[1:-3]
        assert ingredient_lines == [
            "= filling cutlet =",
            "= sauce hot sauce =",
            "= filling shaverma =",
        ]

    @pytest.mark.parametrize(
        "ingredient_indices, expected_price",
        [
            ((0, 1), 3024),
            ((1, 2), 3448),
            ((0, 2), 3114),
            ((0, 1, 2), 3538),
        ],
    )
    def test_get_price_matches_expected_total(self, make_burger, ingredient_indices, expected_price):
        burger = make_burger(ingredient_indices)

        assert burger.get_price() == expected_price

    @pytest.mark.parametrize("ingredient_indices", [(0, 1), (1, 2), (0, 2), (0, 1, 2)])
    def test_get_receipt_displays_ingredients_and_total(self, make_burger, ingredient_indices):
        burger = make_burger(ingredient_indices)
        bun_line = f'(==== {BUN_DATA["name"]} ====)'
        ingredients = [INGREDIENTS_DATA[index] for index in ingredient_indices]
        expected_price = 2 * BUN_DATA["price"] + sum(ingredient["price"] for ingredient in ingredients)
        ingredient_lines = [
            f'= {ingredient["type"].lower()} {ingredient["name"]} ='
            for ingredient in ingredients
        ]
        expected_receipt = "\n".join([bun_line, *ingredient_lines, bun_line, "", f"Price: {expected_price}"])

        assert burger.get_receipt() == expected_receipt
    