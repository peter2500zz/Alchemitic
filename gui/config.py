from enum import Enum

class DebugMark:
    """继承此标记的类不会被查询到"""
    pass

class ZIndex(Enum):
    """最高的数值越后被渲染"""
    backgrounds = 0
    objects = 10
    static_item = 19
    ui = 20
    item_slot = 21
    dragging = 30
    dragging_item = 40
    text = 400
    tooltip = 500
    int_ui = 200
    debug = 999


# ==== 颜色定义 ====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# 窗口尺寸
WINDOW_SIZE = (800, 450)
FONTS = ["microsoftyahei", "wqy-zenhei"]
