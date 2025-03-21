import pygame

from gui.base import PgObject
from gui.config import *
from gui.managers.ui import UIManager


class ToolTipObject(PgObject):
    def __init__(self, title: str = '标题',desc: str = '描述', *, color=BLACK):
        self.color = color
        self.title = title
        self.desc: list[str] = desc.split('\n')
        self._font_size = 16
        self.font = pygame.font.SysFont(FONTS, self._font_size)

        self.z_index = ZIndex.tooltip
        self.visible = False

    def _draw(self, surface):
        for tooltip in UIManager.query(ToolTipObject):
            if tooltip is self:
                continue
            if tooltip.visible:
                return

        title = self.font.render(self.title, True, RED)

        desc = [self.font.render(desc, True, BLUE) for desc in self.desc]

        self.rect.width = max(surface.get_rect().width for surface in [title] + desc)
        self.rect.height = sum(surface.get_rect().height for surface in [title] + desc)

        self.rect.topleft = pygame.mouse.get_pos()
        self.rect.top -= self._font_size
        self.rect.left += self._font_size

        if self.rect.right > WINDOW_SIZE[0]:
            self.rect.right = WINDOW_SIZE[0]
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > WINDOW_SIZE[1]:
            self.rect.bottom = WINDOW_SIZE[1]
        elif self.rect.top < 0:
            self.rect.top = 0

        pygame.draw.rect(surface, self.color, self.rect)
        text_offset = 0
        for text_surface in [title] + desc:
            text_rect = text_surface.get_rect()
            text_rect.topleft = self.rect.topleft
            text_rect.top += text_offset
            surface.blit(text_surface, text_rect)
            text_offset += text_rect.height


class ToolTipManager:
    _instance = None

    registered_objects = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def init(cls):
        cls.tooltip = ToolTipObject('', '', color=WHITE)
        cls.tooltip.visible = False
        cls.active_tooltip_owner = None
        UIManager.add(cls.tooltip)

    @classmethod
    def register(cls, obj, title: str, desc: str):
        """注册一个对象及其tooltip内容"""
        cls.registered_objects[id(obj)] = {
            'object': obj,
            'title': title,
            'desc': desc
        }

    @classmethod
    def unregister(cls, obj):
        """取消注册一个对象"""
        if id(obj) in cls.registered_objects:
            del cls.registered_objects[id(obj)]
            if cls.active_tooltip_owner == obj:
                cls.hide_tooltip()

    @classmethod
    def update(cls):
        """更新tooltip状态（在游戏主循环中调用）"""
        # 获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # 如果鼠标按下，不显示tooltip
        if mouse_pressed:
            cls.hide_tooltip()
            return

        # 查找鼠标下方的最高Z-index对象
        highest_z_object = None
        highest_z = -1

        for obj in UIManager.query():
            # 检查对象是否可见且包含鼠标
            if obj is cls.tooltip:
                continue

            if not obj.visible:
                continue

            if obj.rect.collidepoint(mouse_pos):
                # 检查是否在render_clip内（如果有）
                if hasattr(obj, 'render_clip') and obj.render_clip and not obj.render_clip.collidepoint(mouse_pos):
                    continue

                if obj.z_index.value >= highest_z:
                    highest_z = obj.z_index.value
                    highest_z_object = obj

        # 如果找到对象，显示其tooltip
        if highest_z_object and id(highest_z_object) in cls.registered_objects:
            cls.show_tooltip(highest_z_object)
        else:
            cls.hide_tooltip()

    @classmethod
    def show_tooltip(cls, obj):
        """显示指定对象的tooltip"""
        if cls.active_tooltip_owner == obj:
            return

        if id(obj) in cls.registered_objects:
            data = cls.registered_objects[id(obj)]
            cls.tooltip.title = data['title']
            cls.tooltip.desc = data['desc'].split('\n')
            cls.tooltip.visible = True
            cls.tooltip.active = True
            cls.active_tooltip_owner = obj

    @classmethod
    def hide_tooltip(cls):
        """隐藏当前tooltip"""
        if cls.tooltip:
            cls.tooltip.visible = False
            cls.tooltip.active = False
            cls.tooltip.rect.topleft = (-999, -999)
            cls.active_tooltip_owner = None
