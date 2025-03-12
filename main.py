import pygame
from abc import ABC, abstractmethod
import item

# 颜色常量
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


class PgObject(ABC):
    def __init__(self, rect, color=BLACK):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.active = True
        self.visible = True

    @abstractmethod
    def handle_event(self, event, manager):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def collide_point(self, point):
        return self.rect.collidepoint(point)



# 初始化及使用示例
pygame.init()
screen = pygame.display.set_mode((800, 450))
clock = pygame.time.Clock()

# 我自己的变量



running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # ui.handle_event(event)

    screen.fill(WHITE)
    # 开始绘制

    # 绘制结束
    pygame.display.flip()

    # ui.update(screen)
    clock.tick(60)

pygame.quit()