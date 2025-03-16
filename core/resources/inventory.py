from copy import deepcopy

from core.resources.resource_error import *
from core.resources.resource import Resource
from core.recipes.recipe import Recipe


class Inventory:
    def __init__(self, *resources: Resource):
        self._inventory: dict[type[Resource], Resource] = {}

        # 用 add 方法添加解包的参数
        self.add(*resources)

    def add(self, *resources: Resource):
        """
        当有同类时同类的数量会加上传入 Resource 的数量
        如果没有则新增传入 Resource 到库存
        """
        for resource in resources:
            if type(resource) in self._inventory:
                self._inventory[type(resource)].num += resource.num

            else:
                self._inventory[type(resource)] = deepcopy(resource)

    def __add__(self, other):
        """
        Inventory 类之间的加法
        """
        if not isinstance(other, Inventory):
            return NotImplemented

        new_inventory = Inventory(*self._inventory.values())
        new_inventory.add(*other._inventory.values())

        return new_inventory

    def remove(self, *resources: Resource, just_do_it: bool = False):
        """
        接受多个 Resource 实例作为参数，并且从库存中减去它们
        如果有一项的数量不足以减去则抛出 ResourceBelowZeroError 错误
        正好减到 0 会移除那一项

        :param just_do_it: 当为真时不再抛出错误而是将不足以减去的项移除
        """
        for resource in resources:
            if type(resource) in self._inventory:  # 先看看库存里有没有这一项
                if self._inventory[type(resource)].num - resource.num > 0:
                    self._inventory[type(resource)].num -= resource.num  # 正常减去
                elif self._inventory[type(resource)].num - resource.num == 0 or just_do_it:
                    self._inventory.pop(type(resource))  # 等于 0 或者启用了 just_do_it 则移除这一项
                else:  # 小于 0 且未启用 just_do_it
                    raise ResourceNotEnoughError(resource)
            elif not just_do_it:  # 根本就不存在又没启用 just_do_it
                raise ResourceNotEnoughError(resource)
            # else 不做任何处理因为本就不存在无需移除

    def __sub__(self, other):
        """
        Inventory 类之间的减法
        不会启用 self.remove 的 just_do_it
        """
        if not isinstance(other, Inventory):
            return NotImplemented

        new_inventory = Inventory(*self._inventory.values())
        new_inventory.remove(*other._inventory.values())

        return new_inventory

    def export(self, order: str = '') -> list[Resource]:
        """
        返回由自身库存组成的列表

        :param order: 可选值 (name/type/num)。分别按照 名称 0-9A-Za-z / 种类 0-9A-Za-z / 数量 高-低 排序
        :return: 由自身库存组成的列表
        """
        resource_list: list = list(self._inventory.values())
        match order:
            case 'name':
                pass  # todo! 按照名字排序
            case 'type':
                resource_list.sort(key=lambda resource: resource.category.value)
            case 'num':
                resource_list.sort(key=lambda x: x.num)
                resource_list = list(reversed(resource_list))

        # print([(x.__class__.__name__, x.num) for x in resource_list])
        return resource_list

    def keys(self):
        return self._inventory.keys()

    def check_num(self):
        for resource in self._inventory.copy().values():
            if resource.num <= 0:
                self.remove(resource)

    def include(self, *others) -> bool:
        """
        我比他多，对的对的。我没他多，错的错的。一样多？对喽！

        :param others: 可以是 Inventory 或者 Resource，如果是 Inventory 则会比较每一项
        :return: other 是否是自身的子集
        """

        resources = []
        for other in others:
            if not isinstance(other, (Inventory, Resource)):
                raise TypeError(other)

            if isinstance(other, Inventory):
                resources.extend(other.export())
            elif isinstance(other, Resource):
                resources.append(other)

        for resource in resources:
            res_type = type(resource)
            self_resource = self._inventory.get(res_type, res_type(0))
            if self_resource.num < resource.num:
                return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Inventory):
            return NotImplemented

        # 以互为子集的方式判断相等
        return self.include(other) and other.include(self)

    def __ne__(self, other):
        eq_result = self.__eq__(other)
        return NotImplemented if eq_result is NotImplemented else not eq_result

    def create(self, recipe: Recipe) -> list[Resource]:
        """
        通过传入的配方制作。不检测配方条件是否满足

        :param recipe: 传入的配方
        :return: 返回由合成结果组成的列表
        """
        self.remove(*recipe.requires)
        return recipe.provides

    def take_out(self, *resources: Resource):
        self.remove(*resources)
        return resources



if __name__ == '__main__':
    class sub1(Resource):
        pass
    class sub2(Resource):
        pass

    res1 = sub1(5)
    res2 = sub2(99)
    res3 = sub1(5)
    res4 = sub2()

    inv1 = Inventory(res1, res2)
    inv2 = Inventory(res3, res2)
    print([(x.__class__.__name__, x.num) for x in inv1.export('num')])

