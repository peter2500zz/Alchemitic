from __future__ import annotations

import pygame

from gui.base_objects import *
from gui import config as gui_config
from gui.config import ZIndex

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from gui.ui_mgr import UIManager
    from core.resources.resource import Resource
    from core.resources.inventory import Inventory


class InventoryManager(PgObject):
    def __init__(self, rect, inv: Inventory):
        super().__init__(rect, color=GREY)
        self.inv = inv
        self.item_slot_rect = (96, 96, 64, 64)
        self.item_slots = {type(res): ItemSlotObject(self.item_slot_rect, res) for res in inv.list()}

    def on_create(self, manager: UIManager):
        for item_slot in self.item_slots.values():
            manager.add(item_slot)

    def _update(self, manager):
        self.inv.check_num()
        if set(self.inv.keys()) != set(self.item_slots.keys()):
            for item_slot in self.item_slots.values():
                manager.remove(item_slot)
            self.item_slots = {type(res): ItemSlotObject(self.item_slot_rect, res) for res in self.inv.list()}
            for item_slot in self.item_slots.values():
                manager.add(item_slot)

        # print(self.item_slots)

    # AI 代码
    def _draw(self, surface, manager):
        super()._draw(surface, manager)
        start_x = self.rect.left  # 从容器左边界开始
        start_y = self.rect.top  # 从容器上边界开始
        col = 0
        row = 0

        for item_slot in self.item_slots.values():
            # 计算当前预估宽度
            total_width = (item_slot.rect.width + 20) * (col + 1) - 20

            # 换行判断（包含间隔的总宽度是否超出容器）
            if total_width > self.rect.width:
                row += 1
                col = 0

            # 计算实际坐标
            x = start_x + col * (item_slot.rect.width + 20)
            y = start_y + row * (item_slot.rect.height + 20)

            # 更新位置
            item_slot.rect.topleft = (x, y)
            item_slot.draw(surface, manager)

            col += 1


class ItemObject(DraggableObject):
    def __init__(self, rect, item: Resource, *, color=BLACK):
        super().__init__(rect, color=color)

        self.item = item


class ItemSlotObject(DraggableObject):
    """
    单个物品的库存位
    可以用于展示物品或者从中拖拽出物品实例
    """
    def __init__(self, rect, item: Resource, *, color=WHITE):
        super().__init__(rect, color=color)

        self.item = item
        self._num = item.num
        self.tooltip = ToolTipObject(self.item.name, self.item.description, color=WHITE)
        print(self.tooltip)

        self._font_size = 24
        self.font = pygame.font.SysFont("microsoftyahei", self._font_size)

        self._takeable = True

    def on_create(self, manager: UIManager):
        manager.add(self.tooltip)

    def on_remove(self, manager: UIManager):
        manager.remove(self.tooltip)

    def _on_drag_start(self, manager: UIManager) -> None:
        if self._takeable:
            take_out_item = ItemObject((0, 0, 48, 48), type(self.item)(1), color=CYAN)
            take_out_item.holding = True
            manager.add(take_out_item)
            self._num -= 1
            print(f'从 {self.color} 获取了 {take_out_item.color}')

    def _on_drag_end(self, manager: UIManager) -> None:
        # todo! 应该设置为在背包范围内都能放回去
        # todo! 话又说回来了，我觉得应该加一个滚轮来应对物品很多的情况，其他例如文本在超出self.rect时候也可以用这个滚轮，mixin？遮罩？

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            items: list[ItemObject] = list(reversed(manager.query(ItemObject)))
            for item_obj in items:
                if isinstance(item_obj.item, type(self.item)) and self.rect.collidepoint(item_obj.rect.center):
                    manager.remove(item_obj)
                    break
            self._num += 1
        else:
            self.item.num -= 1

    def _update(self, manager):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.tooltip.visible = True
        else:
            self.tooltip.visible = False

    def _draw(self, surface, manager):
        super()._draw(surface, manager)
        font_s = self.font.render(str(self._num), True, BLACK)
        font_rect = font_s.get_rect()
        font_rect.bottomleft = self.rect.bottomleft
        surface.blit(font_s, font_rect)
        font_s = self.font.render(str(self.item.name), True, BLACK)
        font_rect = font_s.get_rect()
        font_rect.topleft = self.rect.topleft
        surface.blit(font_s, font_rect)


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


class ToolTipObject(PgObject):
    def __init__(self, title: str = '标题',desc: str = '描述', *, color=BLACK):
        super().__init__(color=color)
        self.title = title
        self.desc: list[str] = desc.split('\n')
        self._font_size = 16
        self.font = pygame.font.SysFont("microsoftyahei", self._font_size)

        self.z_index = ZIndex.tooltip
        self.visible = False

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
