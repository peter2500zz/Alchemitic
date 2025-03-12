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