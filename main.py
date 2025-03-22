from core.main import *

from gui.base import *
from gui.config import *
from gui.managers.tooltip import ToolTipManager
from gui.managers.ui import UIManager
from gui.screens.item import InventoryObject
from gui.screens.crucible import CrucibleObject
from gui.screens.debug import GUIDebug
from gui.assets import AssetsLoader, standard_assets

logger = new_logger('GUI')


# 初始化及使用示例
logger.info(f'初始化 GUI')
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# 我自己的变量
inv = Inventory(
    FlameFlower(10),
    Stone(5),
    WaterLotus(3),
    StoneBrick(1),
    Feather(2),
    Gravel(1),
    Coal(1),
    Ignis(1),
    Aqua(1),
    Aer(1),
    Ordo(1),
    Perditio(1),
    Lux(1),
    AlchemyCoal(1),
    Victus(1),
    Motus(1),
    Vacuos(1),
)
inv_mgr = InventoryObject(pygame.Rect((0, 64, 232, 306)), inv)
crucible = CrucibleObject(Crucible(standard_alchemy_recipes))
debug_info = GUIDebug()

UIManager.init(clock)
ToolTipManager.init()
AssetsLoader.init(standard_assets)

UIManager.add(inv_mgr, debug_info, crucible)

# 我的变量定义结束

running = True
while running:
    # print(ui._frames)
    # ==== 按键输入 ====
    for event in pygame.event.get():
        UIManager.handle_event(event)

        if event.type == pygame.QUIT:
            logger.info(f'GUI 终止')
            running = False

    # ==== 逻辑更新 ====
    ToolTipManager.update()
    UIManager.update()

    # ==== 绘制部分 ====
    screen.fill(BLACK)
    # 开始绘制
    UIManager.draw(screen)

    # 绘制结束
    pygame.display.flip()

    clock.tick(60)

pygame.quit()