from gui.base_object import *
from gui.ui_mgr import UIManager


# ==== 测试用的类 ====
class TestObject(PgObject):
    """
    测试类别管它
    """
    def _handle_event(self, event, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(f'Button 1 pressed')

    def _update(self, manager):
        pass

    def _draw(self, surface, manager):
        pygame.draw.rect(surface, self.color, self.rect)

class DragTestObject(DraggableObject):
    def _on_drag_start(self, manager: UIManager) -> None:
        print(f'{self} was dragged')

    def _on_drag_end(self, manager: UIManager) -> None:
        print(f'{self} was released')

# 初始化及使用示例
pygame.init()
screen = pygame.display.set_mode((800, 450))
clock = pygame.time.Clock()

# 我自己的变量
test_block = DragTestObject((20, 20, 64, 64), RED)
test_block2 = DragTestObject((96, 20, 64, 64), BLUE)
ui = UIManager()
ui.add(test_block, test_block2)

print(ui.query(DraggableObject))  # 测试query功能
# 我都变量定义结束

running = True
while running:

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