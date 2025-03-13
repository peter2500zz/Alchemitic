from gui.game_objects import *
from gui.base_objects import *
from gui.ui_mgr import UIManager


# ==== 测试用的类 ====
class DragTestObject(DraggableObject):
    def _on_drag_start(self, manager: UIManager) -> None:
        print(f'{self.color} 被拖拽')

    def _on_drag_end(self, manager: UIManager) -> None:
        print(f'{self.color} 被释放')

class BtnTestObject(BtnObject):
    def _on_clicked(self, manager: UIManager) -> None:
        print(f'{self.color} 被点击')

# 初始化及使用示例
pygame.init()
screen = pygame.display.set_mode((800, 450))
clock = pygame.time.Clock()

# 我自己的变量
test_block = BtnTestObject((20, 20, 64, 64), color=RED)
test_block2 = DragTestObject((96, 20, 64, 64), color=BLUE)
test_block3 = ItemSoltObject((96, 96, 64, 64), color=YELLOW, storage=ItemObject((0, 0, 48, 48), color=CYAN))
ui = UIManager()
ui.add(test_block, test_block2, test_block3)

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

    # ==== 绘制部分 ====
    screen.fill(WHITE)
    # 开始绘制
    ui.draw(screen)

    # 绘制结束
    pygame.display.flip()

    clock.tick(60)

pygame.quit()