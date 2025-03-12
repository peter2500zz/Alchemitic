from gui.base_object import *
from gui.ui_mgr import UIManager

# 初始化及使用示例
pygame.init()
screen = pygame.display.set_mode((800, 450))
clock = pygame.time.Clock()

# 我自己的变量
test_block = DraggableObject((10, 10, 32, 32), RED)
ui = UIManager()
ui.add(test_block)

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