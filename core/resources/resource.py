from core.resources.config import *


class Resource(object):
    category = ResourceCategory.Undefined
    def __init__(self, num: int = 1):
        self.name = 'unknown'
        self.description = 'unknown'
        self.type = 'unknown'
        self.num: int = num  # 当前物品数量


class Aspect(Resource):
    category = ResourceCategory.Aspect


class Item(Resource):
    category = ResourceCategory.Item
    aspects: list[Aspect]

    def __init__(self, num: int = 1):
        super().__init__(num)


