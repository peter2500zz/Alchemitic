from __future__ import annotations
from abc import ABC, abstractmethod
import pygame

from gui.colors import *
from gui.config import ZIndex

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from gui.ui_mgr import UIManager


class PgObject(ABC):
    """
    此抽象基类定义了所有游戏内object
    所有物体在主循环的每一帧都会调用:
        handle_event()
        update()
        draw()
    """
    def __init__(self, rect=pygame.Rect(0, 0, 0, 0), *, color=BLACK):
        self.rect = pygame.Rect(rect)  # 自身的rect
        self.color = color  # 无图片时绘制的纯色色块
        self.active = True  # 是否更新逻辑
        self.visible = True  # 是否可见

        self.z_index = ZIndex.objects

    def on_create(self, manager: UIManager):
        pass

    def handle_event(self, event: pygame.event.Event, manager: UIManager) -> bool:
        """
        pygame接收到用户输入时将event提交给obj处理
        有些obj会直接消费这个event，以防止其他obj处理之后冲突

        :param event: 游戏事件
        :param manager: UIManager实例，用于查询或者操作其他obj
        :return: 如果为真则会消费此事件，其他obj无法继续响应
        """
        if not self.active:
            return False
        return self._handle_event(event, manager)

    @abstractmethod
    def _handle_event(self, event: pygame.event.Event, manager: UIManager) -> bool | bool:
        """
        不与handle_event合并是因为希望省略一些重复的判断代码，这样子类只需要专注处理自己的逻辑

        :param event: 游戏事件
        :param manager: UIManager实例，用于查询或者操作其他obj
        :return: 如果为真则会消费此事件，其他obj无法继续响应
        """
        pass

    def update(self, manager: UIManager) -> None:
        """
        游戏更新时obj需要处理一些事情
        比如物理obj可以趁机用加速度更新自己的速度
        """
        if not self.active:
            return
        return self._update(manager)

    @abstractmethod
    def _update(self, manager: UIManager) -> None:
        pass

    def draw(self, surface: pygame.Surface, manager: UIManager) -> None:
        """
        将自己绘制在屏幕上的方法
        """
        if not self.visible:  # todo! 不确定是否要一起判断 active
            return
        return self._draw(surface, manager)

    @abstractmethod
    def _draw(self, surface: pygame.Surface, manager: UIManager) -> None:
        pygame.draw.rect(surface, self.color, self.rect)


class DraggableObject(PgObject):
    """
    可拖动物体类
    设想情况下鼠标点击实例开始拖动，松开则停止
    """
    def __init__(self, rect, *, color=BLACK):
        super().__init__(rect, color=color)

        # 有关拖拽的判定
        self._drag_tigger_key: int = 1  # 触发拖拽与释放的鼠标按钮 todo! 可能需要区分开始和结束拖拽的按键
        self.can_be_dragged = True  # 是否可以被拖拽
        self.holding = False  # 是否正在被拖拽
        self._mouse_offset = (0, 0)  # 拖拽相对鼠标的偏移

    def _handle_event(self, event, manager):
        """
        不强制子类重写，简化代码，转而调用 drag 的两个 hook 方法

        :return: 是否消费这一次 event
        """
        # 这两个if处理鼠标按下和抬起的事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检测 鼠标是否放在自身范围内 and 能被拖动 and 按下的是设定的键
            if self.rect.collidepoint(event.pos) and self.can_be_dragged and event.button == self._drag_tigger_key:
                self.holding = True
                # 设定一下点击位置与自身位置的偏移，这样拖动起来美观一点
                self._mouse_offset = (
                    event.pos[0] - self.rect.centerx,
                    event.pos[1] - self.rect.centery
                )
                self._on_drag_start(manager)
                return True  # 如果确认可以开始被拖拽，则消费这一次event防止多个物品被拖拽

        elif event.type == pygame.MOUSEBUTTONUP:
            # 当正在被拖动且松开设定的键时释放
            if self.holding and event.button == self._drag_tigger_key:
                self.holding = False
                self._on_drag_end(manager)

    @abstractmethod
    def _on_drag_start(self, manager: UIManager) -> None:
        """
        在开始拖拽时触发
        """
        pass

    @abstractmethod
    def _on_drag_end(self, manager: UIManager) -> None:
        """
        在结束拖拽时触发
        """
        pass

    def _update(self, manager):
        """
        默认跟随鼠标拖动，子类如果重写想要复用逻辑也许可以直接 super()._update(self, manager)
        """
        # 如果正在被拖拽则更新自己的位置到鼠标（还有偏移）
        if self.holding:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.center = (
                mouse_pos[0] - self._mouse_offset[0],
                mouse_pos[1] - self._mouse_offset[1]
            )

    def _draw(self, surface: pygame.Surface, manager: UIManager) -> None:
        super()._draw(surface, manager)


class BtnObject(PgObject):
    """
    按钮obj类
    """
    def __init__(self, rect, *, color=BLACK):
        super().__init__(rect, color=color)

        self.pressed = False

    def _handle_event(self, event, manager):
        """
        当按下时候调用 _on_clicked hook 方法
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == 1:
                # 如果鼠标左键按下时在自身范围内则设定按住为 True
                self.pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed:
                # 如果被按住先释放
                self.pressed = False
                if self.rect.collidepoint(event.pos):
                    # 如果在自身范围内释放则调用 _on_clicked
                    self._on_clicked(manager)

    @abstractmethod
    def _on_clicked(self, manager: UIManager) -> None:
        """
        当按下时触发
        按下的定义在 _handle_event 里
        """
        pass
    
    def _update(self, manager):
        pass

    def _draw(self, surface: pygame.Surface, manager: UIManager) -> None:
        super()._draw(surface, manager)

