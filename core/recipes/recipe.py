from core.alchemy.bases import CrucibleBase
from core.resources.resource import *
from core.resources.resource_error import *


class Recipe:
    def __init__(self, requires: list[Resource], provides: list[Resource]):
        self.requires = requires
        self.provides = provides


class NormalRecipe(Recipe):
    def __init__(self, requires: list[Resource], provides: list[Resource]):
        has_asp = []
        for provide in provides:
            if isinstance(provide, Aspect):
                has_asp.append(provide)
        if has_asp:
            raise NormalRecipeCannotCreateAspectsError(has_asp)

        super().__init__(requires, provides)


class AlchemyRecipe(Recipe):
    def __init__(self, requires: list[Resource], provides: list[Resource], tier: int = 1, *, temp_range: tuple[int, int] | None = None, base: CrucibleBase = None):
        super().__init__(requires, provides)
        self.temp_range = temp_range
        self.base = base
        self.tier = tier


if __name__ == '__main__':
    from core.resources.inventory import Inventory


    class Lingangu(Item):
        pass

    class Doggo(Item):
        pass

    class Booooom(Item):
        pass

    test_recipe = {
        'Booooom': Recipe([Doggo(3), Lingangu(1)], [Booooom(1)]),
    }

    inv = Inventory(Lingangu(1), Doggo(3))

    print(inv.list())
    for recipe in test_recipe.values():
        if inv.include(*recipe.requires):
            result = inv.create(recipe)
            inv.add(*result)
            print(inv.list())
