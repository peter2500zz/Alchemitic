import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)


class DragObject:
    def __init__(self, *, x, y, width, height, image=None, color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)  # 不太好翻译反正是自己的rect
        self.image = image  # 显示的图像
        self.color = color  # 没有图像时显示的色块
        self.visible = True  # 是否渲染
        self.active = True  # 是否更新逻辑

        self._holding = False


    def update(self, event: pygame.event.Event):
        if not self.active: return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._holding = self._mouse_on_me() and pygame.mouse.get_pressed()[0]
        elif event.type == pygame.MOUSEBUTTONUP:
            self._holding = False

        if self._holding:
            self.rect.center = pygame.mouse.get_pos()


    def _mouse_on_me(self):
        _mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(_mouse_pos):
            return True
        return False

    def draw(self):
        if image := self.image:
            screen.blit(image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

# 初始化 Pygame
pygame.init()

# 创建固定大小的窗口（不可调整）
screen = pygame.display.set_mode((800, 450), flags=0)
pygame.display.set_caption("基础窗口")

# 创建时钟对象控制帧率
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


solt = DragObject(x=10, y=10, width=64, height=64)
objects = [solt]

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        solt.update(event)

        if event.type == pygame.QUIT:
            running = False



    # 填充背景色
    screen.fill(WHITE)


    mouse_pos = pygame.mouse.get_pos()
    solt.draw()

    # 更新显示
    pygame.display.flip()

    # 控制帧率为 60 FPS
    clock.tick(60)

# 退出 Pygame
pygame.quit()