from __future__ import annotations

from gui.base import *
from gui.screens.item import InventoryObject

if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from gui.manager import UIManager


class InfoDebug(TextObject):
    def __init__(self):
        self.text = ""
        super().__init__(self.text, reverse_v=True)

    def _on_create(self, manager: UIManager):
        self.rect.bottomleft = (0, WINDOW_SIZE[1])

    def _update(self, manager: UIManager) -> None:
        text = [
            f'objects: {len(manager._frames[manager._current_frame])}',
            f'inv: {[{res.name: res.num for res in inv.inv.export()} for inv in manager.query(InventoryObject)]}',
            f'mouse_pos: {pygame.mouse.get_pos()}',
            f'fps: {manager.clock.get_fps():.2f}',
            f'pages: {[inv._current_page for inv in manager.query(InventoryObject)]}',
        ]
        self.text = '\n'.join(text)

class ObjectDebug(TextObject):
    def __init__(self):
        self.text = ""
        super().__init__(self.text, reverse_h=True, reverse_v=True)

    def _on_create(self, manager: UIManager):
        self.rect.bottomright = WINDOW_SIZE

    def _update(self, manager: UIManager) -> None:
        text = [f'{x}, z-index: {x.z_index.value}' for x in manager._frames[manager._current_frame]]
        self.text = '\n'.join(text)


class GUIDebug(PgObject):
    def __init__(self):
        super().__init__()
        self.debug = [InfoDebug(), ObjectDebug()]

    def _on_create(self, manager: UIManager):
        for debug in self.debug:
            debug.z_index = ZIndex.debug
            manager.add(debug)

    def _on_remove(self, manager: UIManager):
        for debug in self.debug:
            manager.remove(debug)
