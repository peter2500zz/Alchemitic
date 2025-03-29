from gui.base import PgObject
from gui.managers.ui import UIManager


class SmoothMove:
    _instance = None

    moving_objs = {}

    def __new__(cls, *args, ** kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def update(cls):
        delta_time = UIManager.clock.get_time() / 1000
        for obj, data in cls.moving_objs.copy().items():
            obj: PgObject
            target_pos = data['target_pos']
            current_x, current_y = obj.rect.topleft
            target_x, target_y = target_pos
            vx, vy = data['v']
            rx, ry = data['remainder']

            # X轴处理
            remaining_x = target_x - current_x
            if remaining_x:
                dx_total = vx * delta_time + rx
                dx = int(dx_total)
                rx = dx_total - dx

                # 方向校验
                if remaining_x > 0 > dx or remaining_x < 0 < dx:
                    dx = remaining_x
                    rx = 0.0
                # 超界校验
                elif abs(dx) > abs(remaining_x):
                    dx = remaining_x
                    rx = 0.0

                current_x += dx
            else:
                rx = 0.0

            # Y轴处理
            remaining_y = target_y - current_y
            if remaining_y:
                dy_total = vy * delta_time + ry
                dy = int(dy_total)
                ry = dy_total - dy

                if remaining_y > 0 > dy or remaining_y < 0 < dy:
                    dy = remaining_y
                    ry = 0.0
                elif abs(dy) > abs(remaining_y):
                    dy = remaining_y
                    ry = 0.0

                current_y += dy
            else:
                ry = 0.0

            # 更新状态
            obj.rect.topleft = (current_x, current_y)
            data['remainder'] = (rx, ry)

            if (current_x, current_y) == target_pos:
                cls.moving_objs.pop(obj)

    @classmethod
    def move(cls, obj: PgObject, target_pos: tuple[int, int], time: float):
        origin_pos = obj.rect.topleft

        if obj_data := cls.moving_objs.get(obj):
            s_all = (abs(obj_data['origin_pos'][i] - pos) for i, pos in enumerate(obj_data['target_pos']))
            s_done = (abs(obj_data['origin_pos'][i] - pos) for i, pos in enumerate(obj.rect.topleft))
            percent = (sum(s_done) / 2) / (sum(s_all) / 2)
            time *= percent

        cls.moving_objs[obj] = {
            'v': (
                (target_pos[0] - obj.rect.x) / time,
                (target_pos[1] - obj.rect.y) / time
            ),
            'origin_pos': origin_pos,
            'target_pos': target_pos,
            'remainder': (0.0, 0.0)
        }