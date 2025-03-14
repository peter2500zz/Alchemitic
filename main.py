from core.resources.inventory import Inventory
from core.resources.resource import Resource
from gui.base_objects import *
from gui import config as gui_config
from gui.game_objects import InventoryManager
from gui.ui_mgr import UIManager


# ==== 测试用的类 ====
class TestRes1(Resource):
    def __init__(self, num: int = 10):
        super().__init__(num)
        self.name = '灵感菇'
        self.description = '灵感菇力菇力菇力刮擦\n灵感菇 灵感菇'

class TestRes2(Resource):
    def __init__(self, num: int = 3):
        super().__init__(num)
        self.name = '叮咚鸡'
        self.description = '叮\n咚鸡\n叮咚鸡'


# 初始化及使用示例
pygame.init()
screen = pygame.display.set_mode(gui_config.WINDOW_SIZE)
clock = pygame.time.Clock()

# 我自己的变量
res1 = TestRes1()
res2 = TestRes2()
inv = Inventory(res1, res2)
inv_mgr = InventoryManager((20, 20, 256, 256), inv)

ui = UIManager()
ui.add(inv_mgr)

print(ui.query(DraggableObject))  # 测试query功能
# 我都变量定义结束

running = True
while running:
    # print(ui._frames)
    # ==== 按键输入 ====
    for event in pygame.event.get():
        ui.handle_event(event)

        if event.type == pygame.QUIT:
            running = False

    # ==== 逻辑更新 ====
    ui.update()
    print(ui._frames[ui._current_frame])

    # ==== 绘制部分 ====
    screen.fill(BLACK)
    # 开始绘制
    ui.draw(screen)

    # 绘制结束
    pygame.display.flip()

    clock.tick(60)

pygame.quit()