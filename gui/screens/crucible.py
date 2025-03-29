from __future__ import annotations

import pygame

from gui.base import PgObject, BtnObject
from gui.screens.item import ItemObject
from gui.config import *
from gui.managers.ui import UIManager
from gui.screens.popup import ConfirmBox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.alchemy.crucible import Crucible

class CrucibleObject(PgObject):
    """
    GUI的坩埚
    """

    def __init__(self, crucible: Crucible):
        self.rect = pygame.Rect((330, 110, 128, 128))
        self.color = YELLOW

        self.crucible = crucible

        self._init_btn()

    def _init_btn(self):
        """
        初始化自己的按钮
        """

        # 分解按钮
        self._dealch_btn = BtnObject(
            pygame.Rect((330, 240, 64, 32)),
            UIManager.int_new,
            args=[ConfirmBox(yes_func=self._dealch, text="分解锅里所有的物品？")],
            color=RED,
            text='加热'
        )
        # 加热按钮
        self._reaction_btn = BtnObject(
            pygame.Rect((394, 240, 64, 32)), UIManager.int_new,
            args=[ConfirmBox(yes_func=self._reaction, text="用锅里的东西制作新的东西？")],
            color=BLUE,
            text='搅拌'
        )

        self._btns = [self._dealch_btn, self._reaction_btn]

    def _on_create(self):
        UIManager.add(*self._btns)

    def _on_remove(self):
        UIManager.remove(*self._btns)

    def _handle_event(self, event: pygame.event.Event):
        # 如果鼠标左键抬起
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # 查询所有被拖拽出的物品
            for item_obj in UIManager.query(ItemObject):
                item_obj: ItemObject
                # 如果鼠标同时位于自身和这个物品实例内
                if item_obj.rect.collidepoint(event.pos) and self.rect.collidepoint(event.pos):
                    # 向坩埚内添加这个物品
                    self.crucible.add(item_obj.item)
                    # 从UI中移除这个物品
                    UIManager.remove(item_obj)
                    # 一次只操作一个物品
                    break

    def _dealch(self):
        """
        调用自身坩埚的分解
        """
        self.crucible.dealch()

    def _reaction(self):
        """调用自身坩埚的反应"""
        new_aspect_created, item_created = self.crucible.reaction()
        if new_aspect_created:
            UIManager.int_new(ConfirmBox(text='产生了新的要素！', single=True))
        for i, item in enumerate(item_created):
            UIManager.add(ItemObject(pygame.Rect((330 + 50 * i, 34, 48, 48)), item, color=CYAN))




