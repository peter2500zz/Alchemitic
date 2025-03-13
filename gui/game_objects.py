from __future__ import annotations
from gui.base_objects import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from gui.ui_mgr import UIManager


class ItemObject(PgObject):
    def __init__(self, rect, *, color=BLACK, name="unknown"):
        super().__init__(rect, color=color)

        self.name = name

    def _handle_event(self, event, manager):
        pass

    def _update(self, manager):
        pass

    def _draw(self, surface, manager):
        super()._draw(surface, manager)


class ItemSoltObject(DraggableObject):
    def __init__(self, rect, storage: ItemObject, *, color=BLACK):
        super().__init__(rect, color=color)

        self.storage = storage

    def _on_drag_start(self, manager: UIManager) -> None:
        manager.add(self.storage)
        print(f'从 {self.color} 获取了 {self.storage.color}')

    def _on_drag_end(self, manager: UIManager) -> None:
        manager.remove(self.storage)
        print(f'{self.storage.color} 被释放')

    def _update(self, manager):
        if self.holding:
            self.storage.rect.center = pygame.mouse.get_pos()

    def _draw(self, surface, manager):
        super()._draw(surface, manager)

