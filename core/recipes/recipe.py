from core.alchemy.config import CrucibleBase
from core.resources.error import *
from core.resources.resource import *

class Recipe:
    def __init__(self, requires: list[Resource], provides: list[Resource]):
        self.requires = requires
        self.provides = provides


class NormalRecipe(Recipe):
    """
    标准配方类，可直接合成
    无法合成要素
    """
    def __init__(self, requires: list[Resource], provides: list[Resource]):
        has_asp = []
        for provide in provides:
            if isinstance(provide, Aspect):
                has_asp.append(provide)
        if has_asp:  # 标准配方无法合成出要素
            raise NormalRecipeCannotCreateAspectsError(has_asp)

        super().__init__(requires, provides)


class AlchemyRecipe(Recipe):
    """
    炼金配方类，需要坩埚
    可以合成要素
    """
    def __init__(self, requires: list[Resource], provides: list[Resource], tier: int = 1, *, temp_range: tuple[int, int] | None = None, base: CrucibleBase = None):
        super().__init__(requires, provides)
        if temp_range and temp_range[0] > temp_range[1]:
            raise ValueError("无效的温度范围")
        self.temp_range = temp_range
        self.base = base
        self.tier = tier


# todo! 可能需要加入合成耗时系统

# 标准配方
standard_normal_recipes = {
    '打磨石头': NormalRecipe([Stone(2)], [StoneBrick(1)]),
    '粉碎石头': NormalRecipe([Stone(2)], [Gravel(1)]),
}
# 炼金配方
standard_alchemy_recipes = {
    # ==== 要素部分 ==== 注意 tier temp_range base 哦
    '寒冰': AlchemyRecipe([Aqua(1), Ordo(1)], [Gelum(1)]),
    '光明': AlchemyRecipe([Aer(1), Ignis(1)], [Lux(1)]),
    '运动': AlchemyRecipe([Aer(1), Aqua(1)], [Motus(1)]),
    '能量': AlchemyRecipe([Ignis(1), Ordo(1)], [Potentia(1)]),
    '虚空': AlchemyRecipe([Aer(1), Perditio(1)], [Vacuos(1)]),
    '生命': AlchemyRecipe([Aqua(1), Terra(1)], [Victus(1)]),

    # ==== 物品部分 ====
    '制作炼金煤炭': AlchemyRecipe([Coal(1), Ignis(1)], [AlchemyCoal(1)]),
}

