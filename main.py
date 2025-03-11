from matters import *
from recipe import *
from test import *


if __name__ == '__main__':
    for aspect in valid_essentia.values():
        print(aspect.name)
    pot = Pot()
    pot.check()
    pot.add(FlameFlower())
    pot.add(FlameFlower())
    pot.check()
    pot.check_recipe()
