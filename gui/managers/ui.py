import pygame

from gui.config import DebugMark
from gui.base import PgObject


class UIManager:
    """
    用于统一管理obj的类
    """

    _instance = None

    _frames: dict[str, list[PgObject]] = {
        'main': []
    }
    _current_frame = 'main'
    clock: pygame.time.Clock = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    @classmethod
    def init(cls, clock: pygame.time.Clock):
        cls.clock = clock

    @classmethod
    def add(cls, *objs: PgObject, frame: str = 'main'):
        """向管理器中添加实例"""
        for obj in objs:
            cls._frames[frame].append(obj)
            obj.on_create()

    @classmethod
    def remove(cls, *objs: PgObject, frame: str = 'main'):
        """从管理器中移除实例"""
        for obj in objs:
            obj.on_remove()
            cls._frames[frame].remove(obj)
            del obj

    @classmethod
    def handle_event(cls, event: pygame.event.Event):
        """
        用于将pg接收到的事件下发处理
        """
        for obj in reversed(cls._frames.get(cls._current_frame, [])):  # 倒序来确保最新添加的最先处理输入
            if obj.handle_event(event):  # 若消费了这个输入事件则中断
                break

    @classmethod
    def update(cls):
        """
        遍历更新，目前来讲先加入的先更新
        """
        for obj in cls._frames.get(cls._current_frame, []):  # 目前按照顺序更新逻辑
            obj.update()

    @classmethod
    def draw(cls, screen: pygame.Surface) -> None:
        objs = cls._frames.get(cls._current_frame, [])
        objs.sort(key=lambda x: x.z_index.value)
        # print(objs)
        for obj in objs:
            obj.draw(screen)

    @classmethod
    def query(cls, *query_class: object, frame: str = 'main') -> list:
        """
        参考bevy的query，这样的搜索机制看起来不错
        """
        result = []
        if not query_class:
            query_class = PgObject

        for obj in cls._frames.get(frame, []):
            if isinstance(obj, query_class) and not isinstance(obj, DebugMark):
                result.append(obj)
        return result

