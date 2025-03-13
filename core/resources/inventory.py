from copy import deepcopy

from core.resources.resource_error import *
from core.resources.resource import Resource


class Inventory:
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
        if not isinstance(other, self.__class__):
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
        if not isinstance(other, self.__class__):
            return NotImplemented

        new_inventory = Inventory(*self._inventory.values())
        new_inventory.remove(*other._inventory.values())

        return new_inventory

    """
    def sub(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        fused_essentia = {**self._essentia}
        for aspect, concentration in other._essentia.items():
            if aspect not in fused_essentia:
                AspectNotFound(aspect)
            elif fused_essentia[aspect] - concentration < 0:
                fused_essentia[aspect] = 0
            else:
                fused_essentia[aspect] -= concentration

        return Essentia(**fused_essentia)

        # 以类变量形式获取要素

    def __getattr__(self, aspect):
        if aspect in self._essentia:
            return self._essentia[aspect]
        else:
            return None

    def __str__(self):
        return str(self._essentia)

        # 要素的比较

    def __lt__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素的浓度比右侧小或者干脆没有这个要素则为真
        # 如果有一个等于或比右边大就False
        for right_essentia, right_concentration in other._essentia.items():
            left_concentration = self._essentia.get(right_essentia, None)
            if left_concentration is None or left_concentration < right_concentration:
                break
        else:
            return False
        return True

    def __le__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素的浓度小于等于右侧或者干脆没有这个要素则为真
        # 如果有一个比右边大就False
        for right_essentia, right_concentration in other._essentia.items():
            left_concentration = self._essentia.get(right_essentia, None)
            if left_concentration is None or left_concentration <= right_concentration:
                break
        else:
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        # 对于右边拥有的变量，左边有一个对应的不一样就False
        for right_essentia, right_concentration in other._essentia.items():
            left_concentration = self._essentia.get(right_essentia, None)
            if left_concentration != right_concentration:
                break
        else:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        # 对于右边拥有的变量，左边对应全部一样就False
        for right_essentia, right_concentration in other._essentia.items():
            left_concentration = self._essentia.get(right_essentia, None)
            if left_concentration != right_concentration:
                break
        else:
            return False
        return True

    def __gt__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素存在且要素的浓度大于右侧则为真
        # 如果不存在或者有一个等于或比右边小就False
        for right_essentia, right_concentration in other._essentia.items():
            left_concentration = self._essentia.get(right_essentia, None)
            if left_concentration is None or left_concentration <= right_concentration:
                break
        else:
            return True
        return False

    def __ge__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素存在且要素的浓度大于等于右侧则为真
        # 如果不存在或者有一个比右边小就False
        for right_essentia, right_concentration in other._essentia.items():
            left_concentration = self._essentia.get(right_essentia, None)
            if left_concentration is None or left_concentration < right_concentration:
                break
        else:
            return True
        return False

    def same_with(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        if self._essentia != other._essentia:
            return False
        return True

    def diff_with(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented
        if self._essentia == other._essentia:
            return False
        return True
    """


if __name__ == '__main__':
    class sub1(Resource):
        pass
    class sub2(Resource):
        pass

    res1 = sub1(5)
    res2 = sub2()

    inv1 = Inventory(res1, res2)

    inv2 = Inventory(res1, res2, res2)
    for i in inv2._inventory.values():
        print(i.__class__.__name__, i.num)
    inv2 -= inv1
    print(inv2._inventory)
    for i in inv2._inventory.values():
        print(i.__class__.__name__, i.num)
