from AlchemyError import *
from abc import ABC, abstractmethod
from matters import Aspects


class Item(ABC):
    name = 'unknown' # 物品名词
    desc = 'unknown' # 物品描述
    craft_cost = Aspects() # 制作花费
    aspect_provide = Aspects() # 分解返还

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @abstractmethod
    def can_be_crafted(self, aspects: Aspects):
        """
        用于判断是否可以制作该物品，与制作花费是分离的，更倾向于表示制作此物品需要达到的条件而非花费
        """
        pass

class FlamePoison(Item):
    name = 'Flame poison'
    desc = 'Burn them down.'
    craft_cost = Aspects(Ignis=1)
    aspect_provide = Aspects(Ignis=0.3)

    def can_be_crafted(self, aspects: Aspects):
        craft_condition = aspects >= Aspects(Ignis=1) and aspects < Aspects(Aqua=1)
        if craft_condition:
            return True
        return False

class SpeedPoison(Item):
    name = 'Speed poison'
    desc = 'Run faster.'
    craft_cost = Aspects(Aer=0.7)
    aspect_provide = Aspects(Aer=0.1)

    def can_be_crafted(self, aspects: Aspects):
        craft_condition = aspects >= Aspects(Aer=1)
        if craft_condition:
            return True
        return False

def craft(aspects: Aspects, target: Item):
    if target.can_be_crafted(aspects):
        aspects -= target.craft_cost
        inventory[target.name] = inventory.get(target.name, 0) + 1
        print(f'Crafted {target.name}')
    else:
        print(f'Can not craft {target.name}')
    return aspects

valid_recipe = [
    FlamePoison(),
    SpeedPoison(),
]

inventory = {

}

if __name__ == '__main__':
    test_asp = Aspects(Ignis=1.5, Aer=1, Aqua=0.2)
    print(f'You have {test_asp}')

    for recipe in valid_recipe:
        if recipe.can_be_crafted(test_asp):
            print(f'You can craft {recipe.name}')

    test_asp = craft(test_asp, FlamePoison())
    print(f'You have {test_asp}')
    print(f'Your inventory is {inventory}')
    test_asp = craft(test_asp, FlamePoison())
    print(f'You have {test_asp}')
    print(f'Your inventory is {inventory}')
    test_asp = craft(test_asp, SpeedPoison())
    print(f'You have {test_asp}')
    print(f'Your inventory is {inventory}')



