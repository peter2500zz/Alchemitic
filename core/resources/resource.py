

class Resource(object):
    def __init__(self, num: int = 1):
        self.name = 'unknown'
        self.description = 'unknown'
        self.type = 'unknown'
        self.num: int = num  # 当前物品数量


class Aspect(Resource):
    pass


class Item(Resource):
    pass

