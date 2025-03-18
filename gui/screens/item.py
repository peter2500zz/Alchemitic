from __future__ import annotations

from gui.base import *
from gui.config import *
from gui.screens.tooltip import ToolTipObject

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from gui.manager import UIManager
    from core.resources.resource import Resource
    from core.resources.inventory import Inventory


class InventoryObject(PgObject):
    """
    背包模块
    """
    def __init__(self, rect, inv: Inventory):
        super().__init__(rect, color=GREY)
        self.inv = inv
        self.item_slot_rect = (96, 96, 64, 64)  # 背包的大小
        #  背包的所有槽位，根据自己的物品栏设定，物品栏必然是动态的
        self.item_slots = {type(res): ItemSlotObject(self.item_slot_rect, res) for res in inv.export()}

    def on_create(self, manager: UIManager):
        #  当自身被创建的时候将所有物品槽位加入管理器，初始化
        for item_slot in self.item_slots.values():
            manager.add(item_slot)

    def _handle_event(self, event: pygame.event.Event, manager: UIManager) -> bool:
        if event.type == pygame.MOUSEBUTTONUP:
            #  当鼠标左键抬起的时
            if event.button == 1:
                #  查询所有被拿出来的实体
                for item_obj in manager.query(ItemObject):
                    #  如果中心与自身相交
                    if self.rect.collidepoint(item_obj.rect.center) and item_obj.rect.collidepoint(event.pos):
                        #  自身物品槽位的显示数量添加
                        for item_slot in self.item_slots.values():
                            if type(item_slot.item) == type(item_obj.item):
                                item_slot.num += item_obj.item.num
                        #  自身物品栏添加（相当于放回去）
                        self.inv.add(item_obj.item)
                        manager.remove(item_obj)
        return False

    def _update(self, manager):
        self.inv.check_num()  # 检查有没有无效物品
        # 如果物品种类变化
        if set(self.inv.keys()) != set(self.item_slots.keys()):
            # 先移除已经实例化的物品槽
            for item_slot in self.item_slots.values():
                manager.remove(item_slot)
            # 重新初始化新的物品槽
            self.item_slots = {type(res): ItemSlotObject(self.item_slot_rect, res) for res in self.inv.export()}
            for item_slot in self.item_slots.values():
                manager.add(item_slot)

    def _draw(self, surface, manager):
        """
        AI 代码 绘制物品槽位
        """
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

            col += 1


class ItemObject(DraggableObject):
    """
    被拿出来的物品
    """
    def __init__(self, rect, item: Resource, tooltip: ToolTipObject, *, color=BLACK):
        super().__init__(rect, color=color)

        self.item = item
        self.tooltip = tooltip
        self.z_index = ZIndex.dragging_item

    def on_create(self, manager: UIManager):
        manager.add(self.tooltip)

    def on_remove(self, manager: UIManager):
        manager.remove(self.tooltip)

    def _update(self, manager):
        super()._update(manager)

        # 只有不被拖动以及鼠标在自身时才显示 tooltip
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.holding and not pygame.mouse.get_pressed()[0]:
            self.tooltip.visible = True
        else:
            self.tooltip.visible = False
        # if self.rect.bottom < WINDOW_SIZE[1]:
        #     if self.rect.bottom + 5 >= WINDOW_SIZE[1]:
        #         self.rect.bottom = WINDOW_SIZE[1]
        #     else:
        #         self.rect.bottom += 5
        # else:
        #     self.rect.bottom = WINDOW_SIZE[1]


class ItemSlotObject(DraggableObject):
    """
    单个物品的库存位
    可以用于展示物品或者从中拖拽出物品实例
    """
    def __init__(self, rect, item: Resource, *, color=WHITE):
        super().__init__(rect, color=color)

        self.item: Resource = item
        self.num = item.num
        self.tooltip = ToolTipObject(self.item.name, self.item.description, color=WHITE)
        # print(self.tooltip)

        self._font_size = 24
        self.font = pygame.font.SysFont(FONTS, self._font_size)

        self._takeable = True
        self._take_out_num = 1  # 除非调试不然不要改这个！！！

    def on_create(self, manager: UIManager):
        manager.add(self.tooltip)

    def on_remove(self, manager: UIManager):
        manager.remove(self.tooltip)

    def _on_drag_start(self, manager: UIManager) -> None:
        if self._takeable:
            take_out_item = ItemObject(
                (0, 0, 48, 48),
                type(self.item)(self._take_out_num),
                ToolTipObject(self.item.name, self.item.description, color=WHITE),
                color=CYAN
            )
            take_out_item.holding = True
            manager.add(take_out_item)
            self.num -= self._take_out_num
            # print(f'从 {self.color} 获取了 {take_out_item.color}')

    def _on_drag_end(self, manager: UIManager) -> None:
        # todo! 话又说回来了，我觉得应该加一个滚轮来应对物品很多的情况，其他例如文本在超出self.rect时候也可以用这个滚轮，mixin？遮罩？

        if self.item.num - self._take_out_num >= 0:
            self.item.num -= self._take_out_num
        else:
            raise ValueError("物品数量不足")

    def _update(self, manager):
        # 只有不被拖动以及鼠标在自身时才显示 tooltip
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.holding and not pygame.mouse.get_pressed()[0]:
            self.tooltip.visible = True
        else:
            self.tooltip.visible = False

    def _draw(self, surface, manager):
        super()._draw(surface, manager)
        font_s = self.font.render(str(self.num), True, BLACK)
        font_rect = font_s.get_rect()
        font_rect.bottomleft = self.rect.bottomleft
        surface.blit(font_s, font_rect)
        font_s = self.font.render(str(self.item.name), True, BLACK)
        font_rect = font_s.get_rect()
        font_rect.topleft = self.rect.topleft
        surface.blit(font_s, font_rect)


class ItemDestroyObject(PgObject):
    def __init__(self, rect, *, color=RED):

        super().__init__(rect, color=color)

        self.num = 0

    def _handle_event(self, event, manager):
        if event.type == pygame.MOUSEBUTTONUP:
            items: list[ItemObject] = manager.query(ItemObject)

            for item in items:
                if self.rect.collidepoint(item.rect.center):
                    self.num += 1
                    print(f'我销毁了 {item.color}')
                    manager.remove(item)

