import pygame

from gui.base_object import PgObject, TestObject
from gui.colors import WHITE


class UIManager:
    """
    用于统一管理obj的类
    todo? 也许之后要改个名字？ 或者设置一个父类来分别 manage 物体和 UI？
    """
    def __init__(self):
        self._frames: dict[str, list[PgObject]] = {
            'main': []
        }
        self._current_frame = 'main'

    def add(self, *objs: PgObject, frame: str = 'main'):
        self._frames[frame].extend(objs)

    def remove(self, *objs: PgObject, frame: str = 'main'):
        for obj in objs:
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
        for obj in self._frames.get(self._current_frame, []):  # todo! 需要加入一个 z-index 来确保不同层的 obj 分开绘制
            obj.draw(screen, self)

    def query(self, *query_class: object, frame: str = 'main') -> list[object]:
        """
        参考bevy的query，这样的搜索机制看起来不错
        """
        result = []
        if query_class:
            for obj in self._frames.get(frame, []):
                if isinstance(obj, query_class):
                    result.append(obj)
        return result


# 调试区域
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
