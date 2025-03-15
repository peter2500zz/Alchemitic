from core.recipes.recipe import AlchemyRecipe, Recipe
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
            if isinstance(resource, Aspect):
                self._inv.add(resource)
            else:
                self._inv.add(*resource.aspects)
            results.extend(self.create())
        return results

    # todo! 需要分离要素融合和炼金配方，要素融合应该要在不断的tick中缓慢合成，tick数量可以固定？

    def create(self) -> list[Item]:
        recipes: list[AlchemyRecipe] = sorted(self._recipes.values(), key=lambda x: x.tier, reverse=True)
        results = []
        for recipe in recipes:
            if recipe.temp_range:
                if not (recipe.temp_range[0] <= self.temperature <= recipe.temp_range[1]):
                    continue

            if recipe.base:
                if self.base.value != recipe.base.value:
                    continue

            if self._inv.include(*recipe.requires):
                for result in self._inv.create(recipe):
                    if isinstance(result, Aspect):
                        self._inv.add(result)
                    else:
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

    alch_recipes = {
        'Lux': AlchemyRecipe([Ignis(1), Aer(1)], [Lux(1)])
    }

    pot = Crucible(alch_recipes)
    print(pot._inv.list())
    pot.add(Candle(1))
    print(pot._inv.list())
    pot.add(WindFlower(1))
    print(pot._inv.list())

