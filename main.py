from gui.base_objects import *
from gui.config import *
from gui.game_objects import InventoryManager
from gui.ui_mgr import UIManager
from gui.debug import GUIDebug

from core.main import *

logger = logging.getLogger("GUI")


# ==== 测试用的类 ====


# 初始化及使用示例
logger.info(f'初始化GUI')
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# 我自己的变量
inv = Inventory(FlameFlower(10), Stone(5), WaterLotus(3), StoneBrick(1))
inv_mgr = InventoryManager((20, 20, 256, 256), inv)
debug_info = GUIDebug()
ui = UIManager(clock)
ui.add(inv_mgr, debug_info)

# 我的变量定义结束

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

    # ==== 绘制部分 ====
    screen.fill(BLACK)
    # 开始绘制
    ui.draw(screen)

    # 绘制结束
    pygame.display.flip()

    clock.tick(60)

pygame.quit()