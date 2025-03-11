from AlchemyError import *
from abc import abstractmethod, ABC


class Essentia:
    """
    这里是源质类，可以将输入的要素打包为一组源质
    也可以参与比较
    """

    def __init__(self, **kwargs):
        self._essentia = {}
        for aspect, concentration in kwargs.items():
            if concentration < 0:
                raise AspectBelowZero(aspect)
            if aspect in valid_essentia:
                self._essentia[aspect] = round(concentration, 2)
            else:
                raise AspectInvalid(aspect)

    def __add__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        fused_essentia = {**self._essentia}
        for aspect, concentration in other._essentia.items():
            if aspect in fused_essentia:
                fused_essentia[aspect] += concentration
            else:
                fused_essentia[aspect] = concentration

        return Essentia(**fused_essentia)

    # 减法小于0会抛出错误，强制锁定为0需要使用sub
    def __sub__(self, other):
        if not isinstance(other, Essentia):
            return NotImplemented

        fused_essentia = {**self._essentia}
        for aspect, concentration in other._essentia.items():
            if aspect not in fused_essentia:
                AspectNotFound(aspect)
            elif fused_essentia[aspect] - concentration < 0:
                AspectBelowZero(aspect)
            else:
                fused_essentia[aspect] -= concentration

        return Essentia(**fused_essentia)

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


class Aspects(ABC):
    """
    这里是要素基类，用于定义各个要素
    """
    name = 'unknown'  # 物品名词
    desc = 'unknown'  # 物品描述

    _creatable = False
    _create_cost = Essentia()

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def can_be_created(self, essentia: Essentia):
        """
        在没有重载的情况下简单判断是否大于
        """
        if essentia >= self._create_cost and self._creatable:
            return True
        return False


valid_essentia = {}


def essentia_register(cls: Aspects):
    """
    将源质要素注册为可用
    """
    valid_essentia[cls.__name__] = cls()  # 不要管pycharm的注释，单例cls就是要实例化
    return cls


@essentia_register
class Ignis(Aspects):
    name = '火'


@essentia_register
class Aqua(Aspects):
    name = '水'


@essentia_register
class Aer(Aspects):
    name = '风'


@essentia_register
class Terra(Aspects):
    name = '地'


@essentia_register
class Lux(Aspects):
    name = '光明'
    _creatable = True
    _create_cost = Essentia(Ignis=1, Aer=1)


if __name__ == '__main__':
    test_asp = Essentia(Ignis=1, Aer=1)
    test_asp2 = Essentia(Ignis=1, Lux=1)
    print(test_asp < test_asp2 + test_asp)
    for name, aspect in valid_essentia.items():
        if aspect.can_be_created(test_asp):
            print(f'You can create {name}')
