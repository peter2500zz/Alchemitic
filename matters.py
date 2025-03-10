from AlchemyError import *

ARCHES = [
    'Ignis',
    'Aqua',
    'Aer',
    'Terra'
]


class Aspects:

    def __init__(self, **kwargs):
        self.aspects = {}
        for aspect, concentration in kwargs.items():
            if aspect in ARCHES:
                self.aspects[aspect] = concentration
            else:
                raise AspectInvalid(aspect)

    def __add__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        fused_aspect = {**self.aspects}
        for aspect, concentration in other.aspects.items():
            if aspect in fused_aspect:
                fused_aspect[aspect] += concentration
            else:
                fused_aspect[aspect] = concentration

        return Aspects(**fused_aspect)

    # 以类变量形式获取要素
    def __getattr__(self, aspect):
        if aspect in self.aspects:
            return self.aspects[aspect]
        else:
            raise AspectNotExist(aspect)

    # 要素的比较
    def __lt__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 遍历右侧的每一个要素，如果左侧对应要素的浓度比右侧小或者干脆没有这个要素则为真
        # 如果有一个等于或比右边大就False
        for right_aspect, right_concentration in other.aspects.items():
            left_concentration = self.aspects.get(right_aspect, None)
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
        for right_aspect, right_concentration in other.aspects.items():
            left_concentration = self.aspects.get(right_aspect, None)
            if left_concentration is None or left_concentration <= right_concentration:
                break
        else:
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 对于右边拥有的变量，左边有一个对应的不一样就False
        for right_aspect, right_concentration in other.aspects.items():
            left_concentration = self.aspects.get(right_aspect, None)
            if left_concentration != right_concentration:
                break
        else:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        # 对于右边拥有的变量，左边对应全部一样就False
        for right_aspect, right_concentration in other.aspects.items():
            left_concentration = self.aspects.get(right_aspect, None)
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
        for right_aspect, right_concentration in other.aspects.items():
            left_concentration = self.aspects.get(right_aspect, None)
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
        for right_aspect, right_concentration in other.aspects.items():
            left_concentration = self.aspects.get(right_aspect, None)
            if left_concentration is None or left_concentration < right_concentration:
                break
        else:
            return True
        return False

    def same_with(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented

        if self.aspects != other.aspects:
            return False
        return True

    def diff_with(self, other):
        if not isinstance(other, Aspects):
            return NotImplemented
        if self.aspects == other.aspects:
            return False
        return True

if __name__ == '__main__':
    test_asp = Aspects(Ignis=0.5, Terra=1, Aqua=1)
    test_asp2 = Aspects(Ignis=0.5)
    print(test_asp < test_asp2 + test_asp)


