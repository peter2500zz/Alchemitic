import pygame

from gui.base import PgObject, BtnObject, TextObject
from gui.config import *
from gui.managers.ui import UIManager


class ConfirmBox(PgObject):
    def __init__(self, pos: tuple[int, int], refer: list[bool], text: str = ''):
        self.rect = pygame.Rect(pos[0], pos[1], 250, 125)
        self.color = WHITE
        self.refer = refer
        self.text = text
        self.z_index = ZIndex.int_ui

    def _on_create(self):
        nobtn = BtnObject(pygame.Rect(0, 0, 95, 40), self.end, args=[False],
                  z_index=ZIndex.int_ui, color=RED, text='取消')
        yesbtn = BtnObject(pygame.Rect(0, 0, 95, 40), self.end, args=[True],
                  z_index=ZIndex.int_ui, color=BLUE, text='确定')
        text = TextObject(self.text, self.rect, 20)
        nobtn.rect.bottom = self.rect.bottom - 5
        nobtn.rect.left = self.rect.left + 20
        yesbtn.rect.bottom = self.rect.bottom - 5
        yesbtn.rect.right = self.rect.right - 20
        text.rect.topleft = self.rect.topleft
        text.color = BLACK
        text.z_index = ZIndex.int_ui
        UIManager.interrupt([
            nobtn, yesbtn, text
            ])

    def end(self, result: bool):
        self.refer[0] = True
        self.refer[1] = result
        UIManager.pop_int()
        UIManager.remove(self)
