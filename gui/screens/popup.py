import pygame

from gui.base import PgObject, BtnObject, TextObject
from gui.config import *
from gui.managers.ui import UIManager


class ConfirmBox(PgObject):
    """
    确认弹框，会中断游戏，并且等待选择
    """
    def __init__(self, yes_func: callable = lambda: None, no_func: callable = lambda: None, text: str = '', single=False):
        """
        Args:
            yes_func: 选择确定时执行的函数
            no_func: 选择取消是执行的函数
            text: 弹框显示的文本
            single: 是否只显示确定
        """

        self.rect = pygame.Rect(0, 0, 250, 125)
        self.rect.center = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
        self.color = WHITE
        self.yes_func = yes_func
        self.no_func = no_func
        self.single = single
        self.text = text
        self.z_index = ZIndex.int_ui

    def _on_create(self):
        btn_list = []
        yesbtn = BtnObject(pygame.Rect(0, 0, 95, 40), self.end, args=[self.yes_func],
                  z_index=ZIndex.int_ui, color=BLUE, text='确定')
        btn_list.append(yesbtn)
        yesbtn.rect.bottom = self.rect.bottom - 5
        if not self.single:
            nobtn = BtnObject(pygame.Rect(0, 0, 95, 40), self.end, args=[self.no_func],
                              z_index=ZIndex.int_ui, color=RED, text='取消')
            btn_list.append(nobtn)
            nobtn.rect.bottom = self.rect.bottom - 5
            nobtn.rect.left = self.rect.left + 20
            yesbtn.rect.right = self.rect.right - 20
        else:
            yesbtn.rect.centerx = self.rect.centerx
        text = TextObject(self.text, self.rect, 20)
        btn_list.append(text)
        text.rect.topleft = self.rect.topleft
        text.color = BLACK
        text.z_index = ZIndex.int_ui
        # 创建中断
        UIManager.interrupt(btn_list)

    def end(self, func: callable):
        UIManager.pop_int()
        UIManager.remove(self)
        func()
