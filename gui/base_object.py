from abc import ABC, abstractmethod
from gui.colors import *
import pygame

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



class TestObject(PgObject):
    def handle_event(self, event, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(f'Button 1 pressed')


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class DraggableObject(PgObject):
    def __init__(self, rect, color=BLACK):
        super().__init__(rect, color)

        # 有关拖拽的判定
        self.can_be_dragged = True
        self.holding = False
        self._mouse_offset = (0, 0)

    def handle_event(self, event, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and self.can_be_dragged:
                self.holding = True
                mouse_pos = pygame.mouse.get_pos()
                self._mouse_offset = (self.rect.centerx - mouse_pos[0], self.rect.centery - mouse_pos[1])
                print(f"I'm holding")
                return True  # 如果确认可以开始被拖拽，则消费这一次event防止多个物品被拖拽
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.holding:
                print(f"I'm released")
                self.holding = False

    def update(self, manager):
        if self.holding:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.center = (mouse_pos[0] + self._mouse_offset[0], mouse_pos[1] + self._mouse_offset[1])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
