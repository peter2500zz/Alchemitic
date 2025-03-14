from __future__ import annotations

import pygame

from gui.base_objects import *
from gui import config as gui_config

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
        self.tooltip = ToolTipObject('物品', '描述第一行\n描述第二行\n第三行\n我去这第四行这么长', color=WHITE)

    def _on_drag_start(self, manager: UIManager) -> None:
        take_out_item = ItemObject((0, 0, 48, 48), color=self.item_color)
        take_out_item.holding = True
        manager.add(take_out_item)
        print(f'从 {self.color} 获取了 {take_out_item.color}')

    def _on_drag_end(self, manager: UIManager) -> None:
        pass

    def _update(self, manager):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.tooltip.visible = True
        else:
            self.tooltip.visible = False

    def _draw(self, surface, manager):
        super()._draw(surface, manager)
        self.tooltip.draw(surface, manager)


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


class ToolTipObject(PgObject):
    def __init__(self, title: str = '标题',desc: str = '描述', *, color=BLACK):
        super().__init__(color=color)
        self.title = title
        self.desc: list[str] = desc.split('\n')
        self._font_size = 16
        self.font = pygame.font.SysFont("microsoftyahei", self._font_size)

        self.visible = False

    def _handle_event(self, event, manager):
        pass

    def _update(self, manager):
        pass

    def _draw(self, surface, manager):
        title = self.font.render(self.title, True, RED)

        desc = [self.font.render(desc, True, BLUE) for desc in self.desc]

        self.rect.width = max(surface.get_rect().width for surface in [title] + desc)
        self.rect.height = sum(surface.get_rect().height for surface in [title] + desc)

        self.rect.topleft = pygame.mouse.get_pos()
        self.rect.top -= self._font_size
        self.rect.left += self._font_size

        if self.rect.right > gui_config.WINDOW_SIZE[0]:
            self.rect.right = gui_config.WINDOW_SIZE[0]
        if self.rect.bottom > gui_config.WINDOW_SIZE[1]:
            self.rect.bottom = gui_config.WINDOW_SIZE[1]

        pygame.draw.rect(surface, self.color, self.rect)
        text_offset = 0
        for text_surface in [title] + desc:
            text_rect = text_surface.get_rect()
            text_rect.topleft = self.rect.topleft
            text_rect.top += text_offset
            surface.blit(text_surface, text_rect)
            text_offset += text_rect.height


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
