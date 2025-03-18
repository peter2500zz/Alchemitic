from __future__ import annotations
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # 可能有一些耦合度问题
    from gui.base import PgObject


class UIManager:
    """
    用于统一管理obj的类
    todo? 也许之后要改个名字？ 或者设置一个父类来分别 manage 物体和 UI？
    """
    def __init__(self, clock: pygame.time.Clock):
        self._frames: dict[str, list[PgObject]] = {
            'main': []
        }
        self._current_frame = 'main'
        self.clock = clock

    def add(self, *objs: PgObject, frame: str = 'main'):
        for obj in objs:
            self._frames[frame].append(obj)
            obj.on_create(self)


    def remove(self, *objs: PgObject, frame: str = 'main'):
        for obj in objs:
            obj.on_remove(self)
            self._frames[frame].remove(obj)  # todo! 如果输入的类实例不存在的话那将会出错

    def handle_event(self, event: pygame.event.Event):
        """
        用于将pg接收到的事件下发处理
        """
        for obj in reversed(self._frames.get(self._current_frame, [])):  # 倒序来确保最新添加的最先处理输入
            if obj.handle_event(event, self):  # 若消费了这个输入事件则中断
                break

    def update(self):
        """
        遍历更新，目前来讲先加入的先更新
        """
        for obj in self._frames.get(self._current_frame, []):  # 目前按照顺序更新逻辑
            obj.update(self)

    def draw(self, screen: pygame.Surface) -> None:
        objs = self._frames.get(self._current_frame, [])
        objs.sort(key=lambda x: x.z_index.value)
        # print(objs)
        for obj in objs:
            obj.draw(screen, self)

    def query(self, *query_class: object, frame: str = 'main') -> list:
        """
        参考bevy的query，这样的搜索机制看起来不错
        """
        result = []
        if query_class:
            for obj in self._frames.get(frame, []):
                if isinstance(obj, query_class):
                    result.append(obj)
        return result

