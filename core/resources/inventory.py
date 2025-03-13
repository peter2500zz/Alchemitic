from copy import deepcopy

from core.resources.resource_error import *
from core.resources.resource import Resource


class Inventory:
    # todo! 将字典存储结构改为 类: 数量
    # todo! 可能的问题： 对于有耐久度的实例来说无法保存数据
    # todo! 总之就是取舍运行效率
    def __init__(self, *resources: Resource):
        self._inventory: dict[type[Resource], Resource] = {}

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
                    raise ResourceBelowZeroError(resource)
            elif not just_do_it:  # 根本就不存在又没启用 just_do_it
                raise ResourceBelowZeroError(resource)
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

    def list(self, order: str = '') -> list[Resource]:
        match order:
            case 'name':
                pass  # todo! 按照名字排序
            case 'type':
                pass  # todo! 按照种类排序
            case 'num':
                pass  # todo! 按照数量排序
            case _:
                # 不排序
                pass
        return list(self._inventory.values())

    def include(self, other) -> bool:
        """
        我比他多，对的对的。我没他多，错的错的。一样多？对喽！

        :param other: 可以是 Inventory 或者 Resource，如果是 Inventory 则会比较每一项
        """
        if not isinstance(other, (Inventory, Resource)):
            return NotImplemented

        resources = []
        if isinstance(other, Inventory):
            resources = [*other.list()]
        elif isinstance(other, Resource):
            resources = [other]

        for resource in resources:
            res_type = type(resource)
            self_resource = self._inventory.get(res_type, res_type(0))
            if self_resource.num < resource.num:
                return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Inventory):
            return NotImplemented

        return self.include(other) and other.include(self)

    def __ne__(self, other):
        eq_result = self.__eq__(other)
        return NotImplemented if eq_result is NotImplemented else not eq_result


if __name__ == '__main__':
    class sub1(Resource):
        pass
    class sub2(Resource):
        pass

    res1 = sub1(5)
    res2 = sub2()
    res3 = sub1(5)
    res4 = sub2()

    inv1 = Inventory(res1, res2)
    inv2 = Inventory(res3, res2)
    print(inv1 != inv2)

