from __future__ import annotations
from gui.base_objects import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from gui.ui_mgr import UIManager


class ItemObject(DraggableObject):
    def __init__(self, rect, *, color=BLACK, name="unknown"):
        super().__init__(rect, color=color)

        self.name = name

    def _on_drag_start(self, manager: UIManager) -> None:
        pass

    def _on_drag_end(self, manager: UIManager) -> None:
        pass

    def _update(self, manager):
        super()._update(manager)

    def _draw(self, surface, manager):
        super()._draw(surface, manager)


class ItemSoltObject(DraggableObject):
    def __init__(self, rect, item_color: tuple[int, int, int] = RED, *, color=BLACK):
        super().__init__(rect, color=color)

        self.item_color = item_color

    def _on_drag_start(self, manager: UIManager) -> None:
        take_out_item = ItemObject((0, 0, 48, 48), color=self.item_color)
        take_out_item.holding = True
        manager.add(take_out_item)
        print(f'从 {self.color} 获取了 {take_out_item.color}')

    def _on_drag_end(self, manager: UIManager) -> None:
        pass

    def _update(self, manager):
        pass

    def _draw(self, surface, manager):
        super()._draw(surface, manager)


class ItemDestroyObject(PgObject):
    def __init__(self, rect, *, color=BLACK):
        self.mix_color = [WHITE for _ in range(5)]

        super().__init__(rect, color=blend_colors(self.mix_color))

        self.num = 0

    def _handle_event(self, event, manager):
        if event.type == pygame.MOUSEBUTTONUP:
            items: list[ItemObject] = manager.query(ItemObject)

            for item in items:
                if self.rect.collidepoint(item.rect.center):
                    self.num += 1
                    self.mix_color.append(item.color)
                    print(f'我销毁了 {item.color}')
                    manager.remove(item)

    def _update(self, manager):
        self.mix_color = self.mix_color[-5:]
        self.color = blend_colors(self.mix_color)
    
    def _draw(self, surface, manager):
        super()._draw(surface, manager)

# AI 代码
def blend_colors(rgb_list):
    if not rgb_list:
        raise ValueError("输入的RGB列表不能为空")

    n = len(rgb_list)
    sum_r = sum(rgb[0] for rgb in rgb_list)
    sum_g = sum(rgb[1] for rgb in rgb_list)
    sum_b = sum(rgb[2] for rgb in rgb_list)

    avg_r = round(sum_r / n)
    avg_g = round(sum_g / n)
    avg_b = round(sum_b / n)

    # 确保结果在0-255范围内
    avg_r = max(0, min(255, avg_r))
    avg_g = max(0, min(255, avg_g))
    avg_b = max(0, min(255, avg_b))

    return (avg_r, avg_g, avg_b)
