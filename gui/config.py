from enum import Enum

class ZIndex(Enum):
    backgrounds = 0
    objects = 10
    ui = 20
    dragging = 30
    dragging_item = 40
    text = 400
    tooltip = 500
    debug = 999

WINDOW_SIZE = (800, 450)
FONTS = ["microsoftyahei", "wqy-zenhei"]
