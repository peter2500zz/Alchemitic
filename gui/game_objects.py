from __future__ import annotations

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
                    if self.rect.collidepoint(item_obj.rect.center):
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
            item_slot.draw(surface, manager)

            col += 1


class ItemObject(DraggableObject):
    """
    被拿出来的物品
    """
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

        self.item: Resource = item
        self.num = item.num
        self.tooltip = ToolTipObject(self.item.name, self.item.description, color=WHITE)
        print(self.tooltip)

        self._font_size = 24
        self.font = pygame.font.SysFont("microsoftyahei", self._font_size)

        self._takeable = True
        self._take_out_num = 1  # 除非调试不然不要改这个！！！

    def on_create(self, manager: UIManager):
        manager.add(self.tooltip)

    def on_remove(self, manager: UIManager):
        manager.remove(self.tooltip)

    def _on_drag_start(self, manager: UIManager) -> None:
        if self._takeable:
            take_out_item = ItemObject((0, 0, 48, 48), type(self.item)(self._take_out_num), color=CYAN)
            take_out_item.holding = True
            manager.add(take_out_item)
            self.num -= self._take_out_num
            print(f'从 {self.color} 获取了 {take_out_item.color}')

    def _on_drag_end(self, manager: UIManager) -> None:
        # todo! 话又说回来了，我觉得应该加一个滚轮来应对物品很多的情况，其他例如文本在超出self.rect时候也可以用这个滚轮，mixin？遮罩？

        if self.item.num - self._take_out_num >= 0:
            self.item.num -= self._take_out_num
        else:
            raise ValueError("物品数量不足")

    def _update(self, manager):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
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



def blend_colors(rgb_list):
    """
    AI 代码 每次调用时候偏移RGB
    """
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
