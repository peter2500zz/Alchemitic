from __future__ import annotations

from gui.base import *
from gui.config import *
from gui.managers.tooltip import ToolTipManager
from gui.managers.ui import UIManager

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from core.resources.resource import Resource
    from core.resources.inventory import Inventory


class InventoryObject(PgObject):
    """
    背包模块
    """
    ITEM_SLOT_SIZE: int = 64

    def __init__(self, rect, inv: Inventory):
        super().__init__(rect, color=GREY)
        self.z_index = ZIndex.ui
        self._open = False
        self.inv = inv
        self.item_slot_rect = (-99999, -99999, self.ITEM_SLOT_SIZE, self.ITEM_SLOT_SIZE)  # 物品的大小

        self._slot_gap = 10  # px
        self._max_item_row = 4
        self._max_item_col = 3

        #  背包的所有槽位，根据自己的物品栏设定，物品栏必然是动态的
        self._solt_render_clip = self.rect.copy()
        self._solt_render_clip.top += self._slot_gap
        self._solt_render_clip.height -= self._slot_gap * 2
        self.item_slots = {type(res): ItemSlotObject(self.item_slot_rect, res, render_clip=self._solt_render_clip) for res in inv.export()}

        self._item_page = self._calc_item_table()
        self._rolling_offset = 0

        self.rect.left -= self.rect.width

        self._init_btn()


    def _init_btn(self):
        self._open_switch_btn = BtnObject((-99999, -99999, 16, 64), self._switch_open, color=RED)
        self._open_switch_btn.z_index = ZIndex.ui

        self._btns = [self._open_switch_btn]

    def _switch_open(self):
        if not self._open:
            self.rect.left += self.rect.width
            self._open = True
        else:
            self.rect.left -= self.rect.width
            self._open = False

    def on_create(self):
        #  当自身被创建的时候将所有物品槽位加入管理器，初始化
        UIManager.add(*self.item_slots.values())
        UIManager.add(*self._btns)

    def on_remove(self):
        UIManager.remove(*self.item_slots.values())
        UIManager.remove(*self._btns)

    def _handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            #  当鼠标左键抬起的时
            #  查询所有被拿出来的实体
            for item_obj in UIManager.query(ItemObject):
                if item_obj.z_index == ZIndex.static_item:
                    continue
                #  如果中心与自身相交
                if self.rect.collidepoint(event.pos) and item_obj.rect.collidepoint(event.pos):
                    #  自身物品槽位的显示数量添加
                    for item_slot in self.item_slots.values():
                        if type(item_slot.item) == type(item_obj.item):
                            item_slot.num += item_obj.item.num
                    #  自身物品栏添加（相当于放回去）
                    self.inv.add(item_obj.item)
                    UIManager.remove(item_obj)
                else:
                    item_obj.z_index = ZIndex.static_item
        elif event.type == pygame.MOUSEWHEEL:
            # print(event.y)
            if event.y != 0 and self.rect.collidepoint(pygame.mouse.get_pos()) and len(self._item_page) > self._max_item_row:
                self._rolling_offset += -event.y * 5  # 简易滚轮系统

        return False

    def _update(self):
        self.inv.check_num()  # 检查有没有无效物品
        # 如果物品种类变化
        if set(self.inv.keys()) != set(self.item_slots.keys()):
            # 先移除已经实例化的物品槽
            for item_slot in self.item_slots.values():
                UIManager.remove(item_slot)
            # 重新初始化新的物品槽
            self.item_slots = {type(res): ItemSlotObject(self.item_slot_rect, res, render_clip=self._solt_render_clip) for res in self.inv.export()}
            for item_slot in self.item_slots.values():
                UIManager.add(item_slot)
        # 重新计算物品的显示位置
        self._item_page = self._calc_item_table()

        # 归零过大滚动偏移
        if self._rolling_offset < 0:
            self._rolling_offset = 0
        elif self._rolling_offset > self._slot_gap + (self._slot_gap + self.ITEM_SLOT_SIZE) * len(self._item_page) - self.rect.height and len(self._item_page) >= self._max_item_row:
            self._rolling_offset = self._slot_gap + (self._slot_gap + self.ITEM_SLOT_SIZE) * len(self._item_page) - self.rect.height

        self._open_switch_btn.rect.centery = self.rect.top + self.rect.height / 2
        self._open_switch_btn.rect.left = self.rect.right

    def _draw(self, surface):
        """
        绘制物品槽位
        """
        super()._draw(surface)

        for row, row_list in enumerate(self._item_page):
            for col, item_slot in enumerate(row_list):
                item_slot.rect.topleft = (
                    self.rect.left + (item_slot.rect.width + self._slot_gap) * col + self._slot_gap,
                    self.rect.top + (item_slot.rect.height + self._slot_gap) * row + self._slot_gap - self._rolling_offset
                )

    def _calc_item_table(self):
        """
        按照定义的最大行列数制表
        """
        col = 0
        row = 0
        col_list = []
        render_list = []

        for item_slot in self.item_slots.values():
            col_list.append(item_slot)
            col += 1

            if row >= self._max_item_row:
                row = 0
            if col >= self._max_item_col:
                render_list.append(col_list)
                col_list = []
                col = 0
                row += 1

        if col_list:
            render_list.append(col_list)

        return render_list


class ItemObject(DraggableObject):
    """
    被拿出来的物品
    """
    def __init__(self, rect, item: Resource, *, color=BLACK):
        super().__init__(rect, color=color)

        self.item = item
        self.z_index = ZIndex.dragging_item

    def on_create(self):
        ToolTipManager.register(self, self.item.name, self.item.description)

    def on_remove(self):
        ToolTipManager.unregister(self)
    
    def _on_drag_start(self) -> bool:
        self.z_index = ZIndex.dragging_item
        return super()._on_drag_start()

    def _on_drag_end(self):
        super()._on_drag_end()

    def _handle_event(self, event):
        for inv in UIManager.query(InventoryObject):
            if self.z_index == ZIndex.static_item and inv.rect.collidepoint(pygame.mouse.get_pos()):
                return False
        return super()._handle_event(event)


class ItemSlotObject(DraggableObject):
    """
    单个物品的库存位
    可以用于展示物品或者从中拖拽出物品实例
    """
    def __init__(self, rect, item: Resource, *, color=WHITE, render_clip: pygame.Rect = None):
        super().__init__(rect, color=color, render_clip=render_clip)

        self.z_index = ZIndex.item_slot
        self.item: Resource = item
        self.num = item.num
        # self.tooltip = ToolTipObject(self.item.name, self.item.description, color=WHITE)
        # print(self.tooltip)

        self._font_size = 24
        self.font = pygame.font.SysFont(FONTS, self._font_size)

        self._takeable = True
        self._take_out_num = 1  # 除非调试不然不要改这个！！！

    def on_create(self):
        ToolTipManager.register(self, self.item.name, self.item.description)

    def on_remove(self):
        ToolTipManager.unregister(self)

    def _on_drag_start(self) -> bool:
        if self._takeable and (self.render_clip is None or self.render_clip.collidepoint(pygame.mouse.get_pos())):
            take_out_item = ItemObject(
                (0, 0, 48, 48),
                type(self.item)(self._take_out_num),
                color=CYAN
            )
            take_out_item.holding = True
            UIManager.add(take_out_item)
            self.num -= self._take_out_num
            # print(f'从 {self.color} 获取了 {take_out_item.color}')
            return True

        return False  # 否则不允许开始拖拽

    def _handle_event(self, event):
        if self.render_clip.collidepoint(pygame.mouse.get_pos()) or self.holding:
            return super()._handle_event(event)
        return False

    def _on_drag_end(self) -> None:
        # todo! 话又说回来了，我觉得应该加一个滚轮来应对物品很多的情况，其他例如文本在超出self.rect时候也可以用这个滚轮，mixin？遮罩？
        if self.holding:
            if self.item.num - self._take_out_num >= 0:
                self.item.num -= self._take_out_num
            else:
                raise ValueError("物品数量不足")

    def _update(self):
        # 只有不被拖动以及鼠标在自身时才显示 tooltip
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # self.tooltip.visible = (
        #         self.rect.collidepoint(mouse_pos)
        #         and not self.holding
        #         and not mouse_pressed
        #         and (self.render_clip is None or self.render_clip.collidepoint(mouse_pos))
        # )

    def _draw(self, surface):
        super()._draw(surface)
        font_s = self.font.render(str(self.num), True, BLACK)
        font_rect = font_s.get_rect()
        font_rect.bottomleft = self.rect.bottomleft
        surface.blit(font_s, font_rect)
        font_s = self.font.render(str(self.item.name), True, BLACK)
        font_rect = font_s.get_rect()
        font_rect.topleft = self.rect.topleft
        surface.blit(font_s, font_rect)

