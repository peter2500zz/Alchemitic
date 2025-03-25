import pygame

from gui.base import PgObject, BtnObject
from gui.config import *
from gui.managers.ui import UIManager


class ConfirmBox(PgObject):
    rect = pygame.Rect(0, 0, 0, 0)

    def _on_create(self):
        UIManager.interrupt([
            BtnObject(pygame.Rect(WINDOW_SIZE[0] / 2 - 74, WINDOW_SIZE[1] - 128, 64, 64), self.end, z_index=ZIndex.int_ui, color=RED, text='取消'),
            BtnObject(pygame.Rect(WINDOW_SIZE[0] / 2 + 10, WINDOW_SIZE[1] - 128, 64, 64), self.end, z_index=ZIndex.int_ui, color=BLUE, text='确定')
        ])

    def end(self):
        UIManager.pop_int()
        UIManager.remove(self)
