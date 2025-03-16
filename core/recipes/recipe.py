from core.alchemy.bases import CrucibleBase
from core.resources.resource_error import *
from core.resources.resource import *

class Recipe:
    def __init__(self, requires: list[Resource], provides: list[Resource]):
        self.requires = requires
        self.provides = provides


class NormalRecipe(Recipe):
    """
    标准配方类，可直接合成
    """
    def __init__(self, requires: list[Resource], provides: list[Resource]):
        has_asp = []
        for provide in provides:
            if isinstance(provide, Aspect):
                has_asp.append(provide)
        if has_asp:
            raise NormalRecipeCannotCreateAspectsError(has_asp)

        super().__init__(requires, provides)


class AlchemyRecipe(Recipe):
    """
    炼金配方类，需要坩埚
    """
    def __init__(self, requires: list[Resource], provides: list[Resource], tier: int = 1, *, temp_range: tuple[int, int] | None = None, base: CrucibleBase = None):
        super().__init__(requires, provides)
        if temp_range and temp_range[0] > temp_range[1]:
            raise ValueError("无效的温度范围")
        self.temp_range = temp_range
        self.base = base
        self.tier = tier


# todo! 可能需要加入合成耗时系统

standard_normal_recipes = {
    '打磨石头': NormalRecipe([Stone(2)], [StoneBrick(1)]),
    '粉碎石头': NormalRecipe([Stone(2)], [Gravel(1)]),
}

standard_alchemy_recipes = {
    # ==== 要素部分 ==== 注意 tier temp_range base 哦
    '寒冰': AlchemyRecipe([Aqua(1), Ordo(1)], [Gelum(1)]),
    '光明': AlchemyRecipe([Aer(1), Ignis(1)], [Lux(1)]),
    '运动': AlchemyRecipe([Aer(1), Aqua(1)], [Motus(1)]),
    '能量': AlchemyRecipe([Ignis(1), Ordo(1)], [Potentia(1)]),
    '虚空': AlchemyRecipe([Aer(1), Perditio(1)], [Vacuos(1)]),
    '生命': AlchemyRecipe([Aqua(1), Terra(1)], [Victus(1)]),

    # ==== 物品部分 ====
}


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

    print(inv.export())
    for recipe in test_recipe.values():
        if inv.include(*recipe.requires):
            result = inv.create(recipe)
            inv.add(*result)
            print(inv.export())
