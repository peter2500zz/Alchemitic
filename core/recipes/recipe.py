from core.resources.resource import Resource


class Recipe:
    def __init__(self, requires: list[Resource], provides: list[Resource]):
        self.requires = requires
        self.provides = provides


if __name__ == '__main__':
    from core.resources.inventory import Inventory


    class Lingangu(Resource):
        pass

    class Doggo(Resource):
        pass

    class Booooom(Resource):
        pass

    test_recipe = {
        'Booooom': Recipe([Doggo(3), Lingangu(1)], [Booooom(1)]),
    }

    inv = Inventory(Lingangu(1), Doggo(3))

    print(inv.list())
    for recipe in test_recipe.values():
        if inv.include(*recipe.requires):
            inv.create(recipe)
            print(inv.list())
