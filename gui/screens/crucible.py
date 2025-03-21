from __future__ import annotations

import pygame

from gui.base import PgObject, BtnObject
from gui.screens.item import ItemObject
from gui.config import *
from gui.managers.ui import UIManager

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.alchemy.crucible import Crucible

class CrucibleObject(PgObject):

    def __init__(self, crucible: Crucible):
        self.rect = pygame.Rect((330, 110, 128, 128))
        self.color = YELLOW

        self.crucible = crucible

        self._init_btn()

    def _init_btn(self):
        self._dealch_btn = BtnObject(pygame.Rect((330, 240, 64, 32)), self._dealch, color=RED, text='加热')
        self._reaction_btn = BtnObject(pygame.Rect((394, 240, 64, 32)), self._reaction, color=BLUE, text='搅拌')

        self._btns = [self._dealch_btn, self._reaction_btn]

    def on_create(self):
        UIManager.add(*self._btns)

    def on_remove(self):
        UIManager.remove(*self._btns)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for item_obj in UIManager.query(ItemObject):
                item_obj: ItemObject
                if item_obj.rect.collidepoint(event.pos) and self.rect.collidepoint(event.pos):
                    self.crucible.add(item_obj.item)
                    UIManager.remove(item_obj)
                    break

    def _dealch(self):
        self.crucible.dealch()

    def _reaction(self):
        new_aspect_createc, item_created = self.crucible.reaction()
        for i, item in enumerate(item_created):
            UIManager.add(ItemObject(pygame.Rect((330 + 50 * i, 34, 48, 48)), item, color=CYAN))




