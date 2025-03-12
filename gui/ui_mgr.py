import pygame

from gui.base_object import PgObject, TestObject
from gui.colors import WHITE


class UIManager:
    def __init__(self):
        self._frames: dict[str: list[PgObject]] = {
            'main': []
        }
        self._current_frame = 'main'

    def add(self, *objs: PgObject, frame: str = 'main'):
        self._frames[frame].extend(objs)

    def remove(self, *objs: PgObject, frame: str = 'main'):
        for obj in objs:
            self._frames[frame].remove(obj)

    def handle_event(self, event: pygame.event.Event):
        """
        用于将pg接收到的事件下发处理
        """
        for obj in reversed(self._frames.get(self._current_frame, [])):  # 倒序来确保最新添加的最先判断
            if obj.handle_event(event, self):  # 是否消费此event
                break

    def update(self):
        """
        遍历更新，目前来讲先加入的先更新
        """
        for obj in self._frames.get(self._current_frame, []):  # 倒序来确保最新添加的最先判断
            obj.update(self)

    def draw(self, screen: pygame.Surface):
        for obj in self._frames.get(self._current_frame, []):  # 倒序来确保最新添加的最先判断
            obj.draw(screen)


if __name__ == '__main__':
    ui = UIManager()
    test = TestObject((0, 0, 0, 0), WHITE)
    ui.add(test, TestObject((0, 0, 0, 0), WHITE))
    print(ui._frames)
    ui.remove(test)
    print(ui._frames)
    test2 = TestObject((0, 0, 0, 0), WHITE)
    ui.add(test, test2)
    print(ui._frames)
    ui.remove(test, test2)
    print(ui._frames)
