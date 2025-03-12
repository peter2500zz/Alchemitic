from abc import ABC, abstractmethod
import pygame

from gui.colors import *
from gui.ui_mgr import UIManager


class PgObject(ABC):
    """
    此抽象基类定义了所有游戏内object
    所有物体在主循环的每一帧都会调用:
        handle_event()
        update()
        draw()
    """
    def __init__(self, rect, color=BLACK):
        self.rect = pygame.Rect(rect)  # 自身的rect
        self.color = color  # 无图片时绘制的纯色色块
        self.active = True  # 是否更新逻辑
        self.visible = True  # 是否可见

    def handle_event(self, event: pygame.event.Event, manager: UIManager):
        """
        pygame接收到用户输入时将event提交给obj处理
        有些obj会直接消费这个event，以防止其他obj处理之后冲突
        """
        if not self.active:
            return
        self._handle_event(event, manager)

    @abstractmethod
    def _handle_event(self, event: pygame.event.Event, manager: UIManager):
        pass

    def update(self, manager: UIManager):
        """
        游戏更新时obj需要处理一些事情
        比如物理obj可以趁机用加速度更新自己的速度
        """
        if not self.active:
            return
        self._update(manager)

    @abstractmethod
    def _update(self, manager: UIManager):
        pass

    def draw(self, surface: pygame.Surface, manager: UIManager):
        """
        将自己绘制在屏幕上的方法
        """
        if not self.visible:  # todo! 不确定是否要一起判断 active
            return
        self._draw(surface, manager)

    @abstractmethod
    def _draw(self, surface: pygame.Surface, manager: UIManager):
        pass


class TestObject(PgObject):
    """
    测试类别管它
    """
    def _handle_event(self, event, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(f'Button 1 pressed')

    def _update(self, manager):
        pass

    def _draw(self, surface, manager):
        pygame.draw.rect(surface, self.color, self.rect)

class DraggableObject(PgObject):
    """
    可拖动物体类
    设想情况下鼠标点击实例开始拖动，松开则停止
    """
    def __init__(self, rect, color=BLACK):
        super().__init__(rect, color)

        # 有关拖拽的判定
        self._drag_tigger_key: int = 1  # 触发拖拽与释放的鼠标按钮 todo! 可能需要区分开始和结束拖拽的按键
        self.can_be_dragged = True  # 是否可以被拖拽
        self.holding = False  # 是否正在被拖拽
        self._mouse_offset = (0, 0)  # 拖拽相对鼠标的偏移

    def _handle_event(self, event, manager):
        # 这两个if处理鼠标按下和抬起的事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检测 鼠标是否放在自身范围内 and 能被拖动 and 按下的是设定的键
            if self.rect.collidepoint(event.pos) and self.can_be_dragged and event.button == self._drag_tigger_key:
                self.holding = True
                # 设定一下点击位置与自身位置的偏移，这样拖动起来美观一点
                self._mouse_offset = (
                    event.pos[0] - self.rect.left,
                    event.pos[1] - self.rect.top
                )
                print(f"I'm holding")
                return True  # 如果确认可以开始被拖拽，则消费这一次event防止多个物品被拖拽
        elif event.type == pygame.MOUSEBUTTONUP:
            # 当正在被拖动且松开设定的键时释放
            if self.holding and event.button == self._drag_tigger_key:
                print(f"I'm released")
                self.holding = False

    def _update(self, manager):
        # 如果正在被拖拽则更新自己的位置到鼠标（还有偏移）
        if self.holding:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.topleft = (
                mouse_pos[0] - self._mouse_offset[0],
                mouse_pos[1] - self._mouse_offset[1]
            )

    def _draw(self, surface, manager):
        pygame.draw.rect(surface, self.color, self.rect)
