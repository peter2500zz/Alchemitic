from AlchemyError import *
from abc import abstractmethod, ABC

ARCHES = [
    'Ignis',
    'Aqua',
    'Aer',
    'Terra'
]

class Aspects:

    def __init__(self, **kwargs):
        self._aspects = {}
        for aspect, concentration in kwargs.items():
            if concentration < 0:
                raise AspectBelowZero(aspect)
            if aspect in essentia:
                self._aspects[aspect] = round(concentration, 2)
            else:
                raise AspectInvalid(aspect)

    def __add__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        fused_aspect = {**self._aspects}
        for aspect, concentration in other._aspects.items():
            if aspect in fused_aspect:
                fused_aspect[aspect] += concentration
            else:
                fused_aspect[aspect] = concentration

        return Aspects(**fused_aspect)

    # 减法小于0会抛出错误，强制锁定为0需要使用sub
    def __sub__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        fused_aspect = {**self._aspects}
        for aspect, concentration in other._aspects.items():
            if aspect not in fused_aspect:
                AspectNotFound(aspect)
            elif fused_aspect[aspect] - concentration < 0:
                AspectBelowZero(aspect)
            else:
                fused_aspect[aspect] -= concentration

        return Aspects(**fused_aspect)

    def sub(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        fused_aspect = {**self._aspects}
        for aspect, concentration in other._aspects.items():
            if aspect not in fused_aspect:
                AspectNotFound(aspect)
            elif fused_aspect[aspect] - concentration < 0:
                fused_aspect[aspect] = 0
            else:
                fused_aspect[aspect] -= concentration

        return Aspects(**fused_aspect)

    # 以类变量形式获取要素
    def __getattr__(self, aspect):
        if aspect in self._aspects:
            return self._aspects[aspect]
        else:
            return None

    def __str__(self):
        return str(self._aspects)

    # 要素的比较
    def __lt__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素的浓度比右侧小或者干脆没有这个要素则为真
        # 如果有一个等于或比右边大就False
        for right_aspect, right_concentration in other._aspects.items():
            left_concentration = self._aspects.get(right_aspect, None)
            if left_concentration is None or left_concentration < right_concentration:
                break
        else:
            return False
        return True

    def __le__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素的浓度小于等于右侧或者干脆没有这个要素则为真
        # 如果有一个比右边大就False
        for right_aspect, right_concentration in other._aspects.items():
            left_concentration = self._aspects.get(right_aspect, None)
            if left_concentration is None or left_concentration <= right_concentration:
                break
        else:
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 对于右边拥有的变量，左边有一个对应的不一样就False
        for right_aspect, right_concentration in other._aspects.items():
            left_concentration = self._aspects.get(right_aspect, None)
            if left_concentration != right_concentration:
                break
        else:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 对于右边拥有的变量，左边对应全部一样就False
        for right_aspect, right_concentration in other._aspects.items():
            left_concentration = self._aspects.get(right_aspect, None)
            if left_concentration != right_concentration:
                break
        else:
            return False
        return True

    def __gt__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素存在且要素的浓度大于右侧则为真
        # 如果不存在或者有一个等于或比右边小就False
        for right_aspect, right_concentration in other._aspects.items():
            left_concentration = self._aspects.get(right_aspect, None)
            if left_concentration is None or left_concentration <= right_concentration:
                break
        else:
            return True
        return False

    def __ge__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素存在且要素的浓度大于等于右侧则为真
        # 如果不存在或者有一个比右边小就False
        for right_aspect, right_concentration in other._aspects.items():
            left_concentration = self._aspects.get(right_aspect, None)
            if left_concentration is None or left_concentration < right_concentration:
                break
        else:
            return True
        return False

    def same_with(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        if self._aspects != other._aspects:
            return False
        return True

    def diff_with(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented
        if self._aspects == other._aspects:
            return False
        return True


class Essentia(ABC):
    name = 'unknown'  # 物品名词
    desc = 'unknown'  # 物品描述

    _creatable = False

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def can_be_crafted(self) -> bool:
        """
        用于判断是否可以制作该物品，与制作花费是分离的，更倾向于表示制作此物品需要达到的条件而非花费
        """
        return False

essentia = {}
def essentia_register(cls: Essentia):
    essentia[cls.__name__] = cls

@essentia_register
class Ignis(Essentia):
    name = '火'

@essentia_register
class Aqua(Essentia):
    name = '水'

@essentia_register
class Aer(Essentia):
    name = '风'

@essentia_register
class Terra(Essentia):
    name = '地'

@essentia_register
class Lux(Essentia):
    name = '光明'
    _creatable = True
    _need = Aspects(Ignis=1, Aer=1)


if __name__ == '__main__':
    test_asp = Aspects(Ignis=1)
    test_asp2 = Aspects(Ignis=1, Lux=1)
    print(test_asp < test_asp2 + test_asp)


