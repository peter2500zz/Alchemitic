from core.resources.config import *


class Resource(object):
    name = 'unknown'
    description = 'unknown'
    category = ResourceCategory.Undefined

    def __init__(self, num: int = 1):
        self.num: int = num  # 当前物品数量


# ==== 内置类型定义 ====
class Aspect(Resource):
    category = ResourceCategory.Aspect


class Item(Resource):
    category = ResourceCategory.Item
    aspects: list[Aspect]


# ==== 内置元素定义 ====
class Ignis(Aspect):
    """火"""
    name = 'Ignis'
    description = '火'


class Aqua(Aspect):
    """水"""
    name = 'Aqua'
    description = '水'


class Aer(Aspect):
    """风"""
    name = 'Aer'
    description = '风'


class Terra(Aspect):
    """大地"""
    name = 'Terra'
    description = '大地'


class Ordo(Aspect):
    """秩序"""
    name = 'Ordo'
    description = '秩序'


class Perditio(Aspect):
    """混沌"""
    name = 'Perditio'
    description = '混沌'


class Gelum(Aspect):
    """寒冰"""
    name = 'Gelum'
    description = '寒冰'


class Lux(Aspect):
    """光明"""
    name = 'Lux'
    description = '光明'


class Motus(Aspect):
    """运动"""
    name = 'Motus'
    description = '运动'


class Potentia(Aspect):
    """能量"""
    name = 'Potentia'
    description = '能量'


class Vacuos(Aspect):
    """虚空"""
    name = 'Vacuos'
    description = '虚空'


class Victus(Aspect):
    """生命"""
    name = 'Victus'
    description = '生命'


# ==== 内置物品定义 ====
class FlameFlower(Item):
    name = '火焰花'
    description = '被踩到就会自己烧起来的奇怪花朵'
    aspects: list[Aspect] = [Ignis(1)]


class WaterLotus(Item):
    name = '水莲'
    description = '一种生长在水面的莲花'
    aspects: list[Aspect] = [Aqua(1)]


class Feather(Item):
    name = '羽毛'
    description = '从鸟身上拔下的羽毛'
    aspects: list[Aspect] = [Aer(1)]


class Stone(Item):
    name = '石块'
    description = '一块普通的石头'
    aspects: list[Aspect] = [Terra(1)]


class StoneBrick(Item):
    name = '石砖'
    description = '打磨过的石头'
    aspects: list[Aspect] = [Terra(1), Ordo(1)]


class Gravel(Item):
    name = '砾石'
    description = '一堆完全碎掉的石头'
    aspects: list[Aspect] = [Terra(1), Perditio(1)]

