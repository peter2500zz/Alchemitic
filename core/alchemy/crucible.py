from core.recipes.recipe import AlchemyRecipe
from core.resources.inventory import Inventory
from core.alchemy.bases import CrucibleBase
from core.resources.resource import *


class Crucible:
    def __init__(self, recipes: dict[str, AlchemyRecipe]):
        self._inv = Inventory()
        self.temperature = 24
        self.base = CrucibleBase.water
        self._recipes = recipes

    def add(self, *resources: Item | Aspect) -> list[Item]:
        results = []
        for resource in resources:
            # 不管是要素还是物品先直接加到锅里再说
            self._inv.add(resource)
            # results.extend(self.create())
        return results

    def dealch(self):
        for resource in self._inv.export():
            if isinstance(resource, Item):
                self._inv.add(*resource.aspects)
                self._inv.remove(resource)

    def reaction(self) -> list[Item]:
        """
        坩埚的合成与背包合成不同，应该每隔一段时间调用一次判定
        会自动判断锅内可以合成的配方，由配方的tier排序
        如果
        """
        recipes: list[AlchemyRecipe] = sorted(self._recipes.values(), key=lambda x: x.tier, reverse=True)
        results = []  # 存储结果的列表
        for recipe in recipes:
            # 这两个判断用于检测炼金配方的额外条件限制
            if recipe.temp_range:  # 温度限制
                if not (recipe.temp_range[0] <= self.temperature <= recipe.temp_range[1]):
                    continue

            if recipe.base:  # 坩埚基底限制
                if self.base.value != recipe.base.value:
                    continue

            while self._inv.include(*recipe.requires):  # 判断是否满足配方条件
                for result in self._inv.create(recipe):
                    if isinstance(result, Aspect):
                        self._inv.add(result)
                    elif isinstance(result, Item):
                        results.append(result)

        return results


if __name__ == '__main__':
    class Ignis(Aspect):
        pass

    class Aer(Aspect):
        pass

    class Lux(Aspect):
        pass

    class Candle(Item):
        aspects = [Ignis(1)]

    class WindFlower(Item):
        aspects = [Aer(1)]

    class Lantern(Item):
        aspects = [Lux(1)]

    alch_recipes = {
        'Lux': AlchemyRecipe([Ignis(1), Aer(1)], [Lux(1)]),
        'lantern': AlchemyRecipe([Candle(1), Lux(1)], [Lantern(1)])
    }

    pot = Crucible(alch_recipes)

    while choose := int(input("配方: (Ignis:1 + Aer:1 = Lux:1) (Candle:1 + Lux:1 = Lantern:1)\n1. 添加\n2. 制作\n3. 分解\n")):
        match choose:
            case 1:
                if choose := int(input("可选物品\n1. Candle(Ignis: 1)\
                \n2. WindFlower(Aer: 1)\
                \n3. Lantern(Lux: 1)\
                \n4. Ignis: 1\
                \n5. Aer: 1\
                \n6. Lux: 1\
                \n")):
                    match choose:
                        case 1:
                            pot.add(Candle())
                        case 2:
                            pot.add(WindFlower())
                        case 3:
                            pot.add(Lantern())
                        case 4:
                            pot.add(Ignis())
                        case 5:
                            pot.add(Aer())
                        case 6:
                            pot.add(Lux())

            case 2:
                if result := pot.reaction():
                    print(f'反应产生了 {", ".join([f"{res.__class__.__name__}({res.category._name_}): {res.num}" for res in result])}')

            case 3:
                pot.dealch()
        print(f'锅里有 {", ".join([f"{res.__class__.__name__}: {res.num}" for res in pot._inv.export()])}')