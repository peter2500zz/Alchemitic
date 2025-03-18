from core.recipes.recipe import AlchemyRecipe
from core.resources.inventory import Inventory
from core.alchemy.config import CrucibleBase
from core.resources.resource import *


class Crucible:
    def __init__(self, recipes: dict[str, AlchemyRecipe]):
        self.inventory = Inventory()
        self.temperature = 24
        self.base = CrucibleBase.water
        self._recipes = recipes

    def add(self, *resources: Item | Aspect) -> list[Item]:
        results = []
        for resource in resources:
            # 不管是要素还是物品先直接加到锅里再说
            self.inventory.add(resource)
            # results.extend(self.create())
        return results

    def dealch(self) -> bool:
        """
        分解锅里的物品为要素

        :return: 是否有元素被分解
        """
        de_ed = False
        for resource in self.inventory.export():
            if isinstance(resource, Item):  # 如果是物品才进行分解
                for _ in range(resource.num):
                    # 添加 n = 物品数量 次要素
                    self.inventory.add(*resource.aspects)
                self.inventory.remove(resource)  # 把物品从锅里去掉
                de_ed = True

        return de_ed


    def reaction(self) -> tuple[bool, list[Item]]:
        """
        坩埚的合成与背包合成不同
        会自动判断锅内可以合成的配方，由配方的tier排序

        :return: 是否产生任何东西，以及包含结果物品的列表。
        """
        recipes: list[AlchemyRecipe] = sorted(self._recipes.values(), key=lambda x: x.tier, reverse=True)
        results = []  # 存储结果的列表
        new_aspect_created = False
        for recipe in recipes:
            # 这两个判断用于检测炼金配方的额外条件限制
            if recipe.temp_range:  # 温度限制
                if not (recipe.temp_range[0] <= self.temperature <= recipe.temp_range[1]):
                    continue

            if recipe.base:  # 坩埚基底限制
                if self.base.value != recipe.base.value:
                    continue

            while self.inventory.include(*recipe.requires):  # 循环判断是否满足配方条件直到不可制作
                for result in self.inventory.create(recipe):
                    if isinstance(result, Aspect):  # 如果是要素则添加到自身物品内并设定产生新物品为 True
                        self.inventory.add(result)
                        new_aspect_created = True
                    elif isinstance(result, Item):  # 如果是物品则添加到结果
                        results.append(result)

        return new_aspect_created, results

