import pygame

from gui.base import TextObject, PgObject
from gui.screens.item import InventoryObject
from gui.screens.crucible import CrucibleObject
from gui.managers.ui import UIManager
from gui.config import *

class InfoDebug(TextObject, DebugMark):
    def __init__(self):
        self.text = ""
        super().__init__(self.text, reverse_v=True)

    def _on_create(self):
        self.rect.bottomleft = (0, WINDOW_SIZE[1])

    def _update(self) -> None:
        this_frame = UIManager._frames[UIManager._current_frame]

        text = [
            f'objects: {len([i for i in this_frame if not isinstance(i, DebugMark)])} -> {", ".join([i.__class__.__name__ for i in this_frame if i.rect.collidepoint(pygame.mouse.get_pos()) and not isinstance(i, DebugMark)])}',
            f'inv: {[{res.name: res.num for res in inv.inv.export()} for inv in UIManager.query(InventoryObject)]}',
            f'cru: {[{res.name: res.num for res in cru.crucible.inventory.export()} for cru in UIManager.query(CrucibleObject)]}',
            f'mouse_pos: {pygame.mouse.get_pos()}',
            f'fps: {UIManager.clock.get_fps():.2f}',
            # f'pages: {[inv._current_page for inv in UIManager.query(InventoryObject)]}',
        ]
        self.text = '\n'.join(text)

    def _draw(self, surface: pygame.Surface) -> None:
        super()._draw(surface)

        for o in UIManager.query():
            if 'debug' not in o.__class__.__name__.lower():
                pygame.draw.rect(surface, MAGENTA, o.rect, 1)
                if o.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(surface, GREEN, o.rect, 1)

class ObjectDebug(TextObject, DebugMark):
    def __init__(self):
        self.text = ""
        super().__init__(self.text, reverse_h=True, reverse_v=True)

    def _on_create(self):
        self.rect.bottomright = WINDOW_SIZE

    def _update(self) -> None:
        text = [f'{x}, z-index: {x.z_index.value}' for x in UIManager._frames[UIManager._current_frame]]
        self.text = '\n'.join(text)


class GUIDebug(PgObject, DebugMark):
    def __init__(self):
        super().__init__()
        self.debug = [InfoDebug()]#, ObjectDebug()]

        self._is_debugging = False

    def _on_create(self):
        for debug in self.debug:
            debug.z_index = ZIndex.debug
            UIManager.add(debug)

    def _on_remove(self):
        for debug in self.debug:
            UIManager.remove(debug)

    def _handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self._is_debugging = not self._is_debugging

    def _update(self):
        for debugger in self.debug:
            debugger.active = self._is_debugging
            debugger.visible = self._is_debugging
