from gui.base import PgObject
from gui.managers.ui import UIManager


class SmoothMove:
    _instance = None

    moving_objs = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def update(cls):
        delta_time = UIManager.clock.get_time() / 1000
        for obj, data in cls.moving_objs.copy().items():
            obj: PgObject

            delta_x = data['v'][0] * delta_time
            delta_y = data['v'][1] * delta_time

            if abs(obj.rect.x + delta_x) >= abs(data['target_pos'][0]) and abs(obj.rect.y + delta_y) >= abs(data['target_pos'][1]):
                # todo! 这里有数学问题！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                print(obj.rect.x + delta_x, data['target_pos'][0])
                cls.moving_objs.pop(obj)
                continue

            if abs(delta_x) < 1 and obj.rect.x != data['target_pos'][0]:
                delta_x = 1 if delta_x > 0 else -1
            if abs(obj.rect.x + delta_x) >= abs(data['target_pos'][0]):
                obj.rect.x = data['target_pos'][0]
            else:
                obj.rect.x += delta_x

            if abs(delta_y) < 1 and obj.rect.y != data['target_pos'][1]:
                delta_y = 1 if delta_y > 0 else -1
            if abs(obj.rect.y + delta_y) >= abs(data['target_pos'][1]):
                obj.rect.y = data['target_pos'][1]
            else:
                obj.rect.y += delta_y

    @classmethod
    def move(cls, obj: PgObject, target_pos: tuple[int, int], time: float):
        cls.moving_objs[obj] = {
            'v': ((target_pos[0] - obj.rect.x) / time, (target_pos[1] - obj.rect.y) / time),
            'target_pos': target_pos,
        }
        print(cls.moving_objs)
