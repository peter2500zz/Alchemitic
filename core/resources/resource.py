from core.resources.config import *


class Resource(object):
    """
    统一的资源父类
    """
    name = 'unknown'
    description = 'unknown'
    img = 'unknown'
    category = ResourceCategory.Undefined

    def __init__(self, num: int = 1):
        self.num: int = num  # 当前物品数量


# ==== 内置类型定义 ====
class Aspect(Resource):
    """
    要素类
    """
    category = ResourceCategory.Aspect


class Item(Resource):
    """
    物品父类
    """
    category = ResourceCategory.Item
    aspects: list[Aspect]


# 定义能用的资源，也就是加了注册装饰器的
standard_aspects: list[type(Aspect)] = []
standard_items: list[type(Item)] = []

def resource_register(cls):  # 资源注册装饰器
    # 判断资源类型
    if issubclass(cls, Aspect):
        standard_aspects.append(cls)
    elif issubclass(cls, Item):
        standard_items.append(cls)
    return cls


# ==== 内置元素定义 ====
@resource_register
class Ignis(Aspect):
    """火"""
    name = 'Ignis'
    description = '火'


@resource_register
class Aqua(Aspect):
    """水"""
    name = 'Aqua'
    description = '水'


@resource_register
class Aer(Aspect):
    """风"""
    name = 'Aer'
    description = '风'


@resource_register
class Terra(Aspect):
    """大地"""
    name = 'Terra'
    description = '大地'


@resource_register
class Ordo(Aspect):
    """秩序"""
    name = 'Ordo'
    description = '秩序'


@resource_register
class Perditio(Aspect):
    """混沌"""
    name = 'Perditio'
    description = '混沌'


@resource_register
class Gelum(Aspect):
    """寒冰"""
    name = 'Gelum'
    description = '寒冰'


@resource_register
class Lux(Aspect):
    """光明"""
    name = 'Lux'
    description = '光明'


@resource_register
class Motus(Aspect):
    """运动"""
    name = 'Motus'
    description = '运动'


@resource_register
class Potentia(Aspect):
    """能量"""
    name = 'Potentia'
    description = '能量'


@resource_register
class Vacuos(Aspect):
    """虚空"""
    name = 'Vacuos'
    description = '虚空'


@resource_register
class Victus(Aspect):
    """生命"""
    name = 'Victus'
    description = '生命'


# ==== 内置物品定义 ====
@resource_register
class FlameFlower(Item):
    name = '火焰花'
    description = '被踩到就会自己烧起来的奇怪花朵'
    aspects: list[Aspect] = [Ignis(1)]
    combustible = True
    temperature_beilv = 1.5
    time_beilv = 0.25


@resource_register
class WaterLotus(Item):
    name = '水莲'
    description = '一种生长在水面的莲花'
    aspects: list[Aspect] = [Aqua(1)]


@resource_register
class Feather(Item):
    name = '羽毛'
    description = '从鸟身上拔下的羽毛'
    img = 'feather'
    aspects: list[Aspect] = [Aer(1)]


@resource_register
class Stone(Item):
    name = '石块'
    description = '一块普通的石头'
    aspects: list[Aspect] = [Terra(1)]


@resource_register
class StoneBrick(Item):
    name = '石砖'
    description = '打磨过的石头'
    aspects: list[Aspect] = [Terra(1), Ordo(1)]


@resource_register
class Gravel(Item):
    name = '砾石'
    description = '一堆完全碎掉的石头'
    aspects: list[Aspect] = [Terra(1), Perditio(1)]


@resource_register
class Coal(Item):
    name = '煤炭'
    description = '普通的煤炭，可以当作燃料来用'
    img = 'coal'
    aspects: list[Aspect] = [Potentia(1)]
    combustible = True
    temperature_beilv = 1
    time_beilv = 1


@resource_register
class AlchemyCoal(Item):
    name = '炼金煤炭'
    description = '注入了火元素的煤炭，可以燃烧相当长的时间'

