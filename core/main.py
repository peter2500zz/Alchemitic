from core.alchemy.crucible import Crucible
from core.resources.inventory import Inventory
from core.recipes.recipe import standard_normal_recipes, standard_alchemy_recipes
from core.resources.resource import *


# 初始化检测所有物品的合规性
show_debug_info = True
for item in standard_items:  # 遍历所有注册的物品
    recipe_requires: list[list[Resource]] = []
    for recipe_name, recipe in {**standard_normal_recipes, **standard_alchemy_recipes}.items():
        for resource in recipe.provides:  # 尝试在所有配方中寻找作为产物的此物品
            if isinstance(resource, item):
                # 物品可以在配方中被找到
                recipe_requires.append(recipe.requires)
    if not recipe_requires:
        if show_debug_info: print(f'警告 {item} 没有有效的合成配方')

    # 递归检测物品要素合集
    def cycle_def(_item, _num=1):
        if _num > 99:  # 防止出现循环配方时有过深的递归
            raise RecursionError('错误 检测到未定义要素的循环合成，无法自动设定')
        if not recipe_requires:  # 没有有效的配方可以提供要素参考
            if show_debug_info: print(f'错误 {_item} 没有任何有效的配方可以为其设定要素')
        elif len(recipe_requires) > 1:  # 有多个可能的配方，无法判定
            if show_debug_info: print(f'错误 {_item} 在没有设定要素的情况下有多个不同的配方')
        else:
            _recipe = recipe_requires[0]  # 单个配方
            aspects = Inventory()  # 创建临时的物品用于储存，使用背包类是因为可以直接合并同类项
            for _resource in _recipe:  # 遍历配方需求
                if isinstance(_resource, Item):  # 如果是物品则尝试获取物品要素
                    try:
                        aspects.add(*_resource.aspects)
                    except AttributeError:  # 如果物品没有定义要素则递归查找要素
                        cycle_def(_resource, _num + 1)
                elif isinstance(_resource, Aspect):  # 是要素则直接添加
                    aspects.add(_resource)
            _item.aspects = aspects.export()  # 导出储存的要素
            del aspects  # 清理内存
            if show_debug_info: print(f'信息 {_item} 的要素被自动设定为 {", ".join([f"{aspect.num}*{aspect.name}" for aspect in _item.aspects])}')
    try:
        item.aspects
    except AttributeError:  # 如果物品没有设定要素
        try:
            if show_debug_info: print(f'警告 {item} 没有设定所包含的要素，正在尝试根据配方自动设定')
            cycle_def(item)
        except RecursionError as e:  # 递归过深
            if show_debug_info: print(e)


if __name__ == '__main__':
    items = standard_items
    inv = Inventory(Stone(2))
    pot = Crucible(standard_alchemy_recipes)


    # 嵌套地狱 仅作概念性游戏用
    while choose := input(f'\n请选择要进行的操作:\n1. 打开背包\n2. 走向锅\n3. (debug)向背包里添加物品\n0/回车. 结束\n'):
        try: choose = int(choose)
        except ValueError: choose = 0

        match choose:
            case 1:  # 打开背包
                while choose := input(f'\n请选择要进行的操作:\n1. 查看背包\n2. 合成物品\n3. 检查合成手册\n0/回车. 离开\n'):
                    try: choose = int(choose)
                    except ValueError: choose = 0

                    match choose:
                        case 1:  # 查看背包
                            print(f'\n你的背包里现在有:\n{"\n".join(f"{item.num}*{item.name}" for item in inv.export())}')

                        case 2:  # 合成物品
                            can_create = []
                            for recipe_name, recipe in standard_normal_recipes.items():  # 遍历标准配方
                                if inv.include(*recipe.requires):  # 找出现在能制作的
                                    can_create.append({"name": recipe_name, "recipe": recipe})

                            if choose := input(f'\n你现在可以进行以下合成:\n{"\n".join(f"{index + 1}. {recipe['name']}: {' + '.join([f'{res.num}*{res.name}' for res in recipe['recipe'].requires])} = {', '.join([f'{res.num}*{res.name}' for res in recipe['recipe'].provides])}" for index, recipe in enumerate(can_create))}\n0. 不合成\n'):
                                # todo! 制作n次功能
                                try: choose = int(choose)
                                except ValueError: choose = 0
                                if choose > len(can_create): choose = 0

                                if choose != 0:
                                    result = inv.create(can_create[choose - 1]['recipe'])
                                    inv.add(*result)
                                    print(f'\n你制作了:\n{", ".join([f"{result.num}*{result.name}" for result in result])}')

                        case 3:  # 检查合成手册
                            print(f'你的书里记载了一些合成配方:\n{"\n".join([f"{recipe_name}: {' + '.join([f'{res.num}*{res.name}' for res in recipe.requires])} = {', '.join([f'{res.num}*{res.name}' for res in recipe.provides])}" for recipe_name, recipe in standard_normal_recipes.items()])}')
                            input(f'按回车以继续...')

            case 2:  # 走向锅
                while choose := input(f'\n请选择要进行的操作:\n1. 检查锅里的东西\n2. 往锅里扔东西\n3. 加热锅(分解锅里的物品)\n4. 搅拌锅(合成物品)\n5. 检查炼金手册\n0/回车. 离开\n'):
                    # todo! 加入从锅里把没反应的东西捞出来的功能
                    # todo! 改变温度 基底功能
                    try: choose = int(choose)
                    except ValueError: choose = 0

                    match choose:
                        case 1:  # 检查锅里的东西
                            print(f'\n锅里现在有:\n{", ".join([f'{res.num}*{res.name}' for res in pot.inventory.export()])}')

                        case 2:  # 往锅里扔东西
                            inv_list = inv.export()
                            while choose := input(f'\n选择要扔到锅里的东西:\n{"\n".join(f"{index + 1}. {item.name}" for index, item in enumerate(inv_list))}\n0. 取消\n'):
                                try: choose = int(choose)
                                except ValueError: choose = 0
                                if choose > len(inv_list): choose = 0

                                if choose != 0:
                                    num = input(f'要添加的数量(1, 最大 {inv_list[choose - 1].num}): ')
                                    try: num = int(num)
                                    except ValueError: num = 1

                                    if 1 <= num <= inv_list[choose - 1].num:
                                        pot.add(*inv.take_out(type(inv_list[choose - 1])(num)))
                                        print(f'你往锅里加了 {num}*{type(inv_list[choose - 1]).name}')
                                    elif num >= inv_list[choose - 1].num:
                                        print(f'你只有 {inv_list[choose - 1].num} 个 {inv_list[choose - 1].name}')
                                    else:
                                        print(f'这不是一个有效的数字')

                                inv_list = inv.export()

                        case 3:  # 加热锅
                            print(f'\n你往锅底加了点柴火')
                            if pot.dealch():
                                print(f'锅里似乎发生了一些变化(物品被分解)')

                        case 4:  # 搅拌锅
                            print(f'\n你搅拌了一会锅')
                            if result := pot.reaction():
                                item = result[1]
                                if result[0]:
                                    print(f'锅里冒出了一点气泡(产生新元素)')
                                if item:
                                    inv.add(*item)
                                    print(f'锅里浮现出了:\n{", ".join([f"{res.num}*{res.name}" for res in item])}\n你将这些东西放进了背包')

                        case 5:  # 检查炼金手册
                            print(f'你的笔记上记载了一些炼金配方:\n{"\n".join([f"{recipe_name}: {' + '.join([f'{res.num}*{res.name}' for res in recipe.requires])} = {', '.join([f'{res.num}*{res.name}' for res in recipe.provides])}" for recipe_name, recipe in standard_alchemy_recipes.items()])}')
                            input(f'按回车以继续...')

            case 3:  # 向背包里添加物品
                while choose := input(f'\n选择要添加的物品:\n{"\n".join([f"{index + 1}. {item.name}" for index, item in enumerate(items)])}\n0. 取消\n'):
                    try: choose = int(choose)
                    except ValueError: choose = 0
                    if choose > len(items): choose = 0

                    if choose != 0:
                        num = input('要添加的数量(1): ')
                        try: num = int(num)
                        except ValueError: num = 1

                        inv.add(items[choose - 1](num))
                        print(f'\n你往背包里加入了 {num}*{items[choose - 1].name}')
