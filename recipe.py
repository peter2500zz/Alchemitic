from AlchemyError import *
from abc import ABC, abstractmethod
from matters import Essentia


class Item(ABC):
    name = 'unknown'  # 物品名词
    desc = 'unknown'  # 物品描述
    craft_cost = Essentia()  # 制作花费
    aspect_provide = Essentia()  # 分解返还

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def can_be_crafted(self, aspects: Essentia) -> bool:
        """
        用于判断是否可以制作该物品，与制作花费是分离的，更倾向于表示制作此物品需要达到的条件而非花费
        """
        return False


class FlamePoison(Item):
    name = 'Flame poison'
    desc = 'Burn them down.'
    craft_cost = Essentia(Ignis=1)
    aspect_provide = Essentia(Ignis=0.3)

    def can_be_crafted(self, aspects: Essentia) -> bool:
        craft_condition = aspects >= Essentia(Ignis=1) and aspects < Essentia(Aqua=1)
        if craft_condition:
            return True
        return False


class SpeedPoison(Item):
    name = 'Speed poison'
    desc = 'Run faster.'
    craft_cost = Essentia(Aer=0.7)
    aspect_provide = Essentia(Aer=0.1)

    def can_be_crafted(self, aspects: Essentia) -> bool:
        craft_condition = aspects >= Essentia(Aer=1)
        if craft_condition:
            return True
        return False


class FlameFlower(Item):
    name = 'Flame flower'
    desc = 'A burning flower.'
    aspect_provide = Essentia(Ignis=0.5)

class Rinkangu(Item):
    name = 'Rinkangu'
    desc = 'Rinkangurigurigurikuacya...'
    aspect_provide = Essentia(Ignis=1, Aqua=1, Aer=1, Terra=1)

def craft(aspects: Essentia, target: Item):
    if target.can_be_crafted(aspects):
        aspects -= target.craft_cost
        inventory[target.name] = inventory.get(target.name, 0) + 1
        print(f'Crafted {target.name}')
    else:
        print(f'Can not craft {target.name}')
    return aspects


valid_item = [item() for item in Item.__subclasses__()]

inventory = {

}

if __name__ == '__main__':
    test_asp = Essentia(Ignis=1.5, Aer=1, Aqua=0.2)
    print(f'You have {test_asp}')

    for recipe in valid_item:
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
