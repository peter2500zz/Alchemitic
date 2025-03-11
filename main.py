from matters import *
from recipe import *
from test import *


if __name__ == '__main__':
    pot = Pot()
    pot.check()
    pot.add(FlameFlower())
    pot.add(FlameFlower())
    pot.check()
    pot.check_craftable()
