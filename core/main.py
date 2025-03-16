from core.alchemy.crucible import Crucible
from core.resources.inventory import Inventory
from core.recipes.recipe import standard_normal_recipes, standard_alchemy_recipes
from core.resources.resource import *


items = Item.__subclasses__()
inv = Inventory(Stone(2))
pot = Crucible(standard_alchemy_recipes)

while choose := input(f'\n请选择要进行的操作:\n1. 打开背包\n2. 走向锅\n3. (debug)向背包里添加物品\n0/回车. 结束\n'):
    try: choose = int(choose)
    except ValueError: choose = 0

    match choose:
        case 1:
            while choose := input(f'\n请选择要进行的操作:\n1. 查看背包\n2. 合成物品\n3. 检查合成手册\n0/回车. 离开\n'):
                try: choose = int(choose)
                except ValueError: choose = 0

                match choose:
                    case 1:
                        print(f'\n你的背包里现在有:\n{"\n".join(f"{item.num}*{item.name}" for item in inv.export())}')

                    case 2:
                        can_create = []
                        for recipe_name, recipe in standard_normal_recipes.items():
                            if inv.include(*recipe.requires):
                                can_create.append({"name": recipe_name, "recipe": recipe})

                        if choose := input(f'\n你现在可以进行以下合成:\n{"\n".join(f"{index + 1}. {recipe['name']}: {' + '.join([f'{res.num}*{res.name}' for res in recipe['recipe'].requires])} = {', '.join([f'{res.num}*{res.name}' for res in recipe['recipe'].provides])}" for index, recipe in enumerate(can_create))}\n0. 不合成\n'):
                            try: choose = int(choose)
                            except ValueError: choose = 0
                            if choose > len(can_create): choose = 0

                            if choose != 0:
                                result = inv.create(can_create[choose - 1]['recipe'])
                                inv.add(*result)
                                print(f'\n你制作了:\n{", ".join([f"{result.num}*{result.name}" for result in result])}')

                    case 3:
                        print(f'你的书里记载了一些合成配方:\n{"\n".join([f"{recipe_name}: {' + '.join([f'{res.num}*{res.name}' for res in recipe.requires])} = {', '.join([f'{res.num}*{res.name}' for res in recipe.provides])}" for recipe_name, recipe in standard_normal_recipes.items()])}')
                        input(f'按回车以继续...')

        case 2:
            while choose := input(f'\n请选择要进行的操作:\n1. 检查锅里的东西\n2. 往锅里扔东西\n3. 加热锅(分解锅里的物品)\n4. 搅拌锅(合成物品)\n5. 检查炼金手册\n0/回车. 离开\n'):
                try: choose = int(choose)
                except ValueError: choose = 0

                match choose:
                    case 1:
                        print(f'\n锅里现在有:\n{", ".join([f'{res.num}*{res.name}' for res in pot.inventory.export()])}')

                    case 2:
                        inv_list = inv.export()
                        if choose := input(f'\n选择要扔到锅里的东西:\n{"\n".join(f"{index + 1}. {item.name}" for index, item in enumerate(inv_list))}\n0. 取消\n'):
                            try: choose = int(choose)
                            except ValueError: choose = 0
                            if choose > len(inv_list): choose = 0

                            if choose != 0:
                                num = input('要添加的数量(1): ')
                                try: num = int(num)
                                except ValueError: num = 1

                                pot.add(*inv.take_out(type(inv_list[choose - 1])(num)))
                                print(f'你往锅里加了 {num}*{type(inv_list[choose - 1]).name}')

                    case 3:
                        print(f'\n你往锅底加了点柴火')
                        if pot.dealch():
                            print(f'锅里似乎发生了一些变化')

                    case 4:
                        print(f'\n你搅拌了一会锅')
                        if result := pot.reaction():
                            print(f'锅里浮现出了:\n{", ".join([f"{res.num}*{res.name}" for res in result])}\n你将这些东西放进了背包\n')

                    case 5:
                        print(f'你的笔记上记载了一些炼金配方:\n{"\n".join([f"{recipe_name}: {' + '.join([f'{res.num}*{res.name}' for res in recipe.requires])} = {', '.join([f'{res.num}*{res.name}' for res in recipe.provides])}" for recipe_name, recipe in standard_alchemy_recipes.items()])}')
                        input(f'按回车以继续...')

        case 3:
            while choose := input(f'\n选择要添加的物品:\n{"\n".join([f"{index + 1}. {item.name}" for index, item in enumerate(items)])}\n0. 取消\n3'):
                try: choose = int(choose)
                except ValueError: choose = 0
                if choose > len(items): choose = 0

                if choose != 0:
                    num = input('要添加的数量(1): ')
                    try: num = int(num)
                    except ValueError: num = 1

                    inv.add(items[choose - 1](num))
                    print(f'\n你往背包里加入了 {num}*{items[choose - 1].name}')
