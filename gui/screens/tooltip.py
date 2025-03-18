import pygame

from gui.base import PgObject
from gui.config import *


class ToolTipObject(PgObject):
    def __init__(self, title: str = '标题',desc: str = '描述', *, color=BLACK):
        super().__init__(color=color)
        self.title = title
        self.desc: list[str] = desc.split('\n')
        self._font_size = 16
        self.font = pygame.font.SysFont(FONTS, self._font_size)

        self.z_index = ZIndex.tooltip
        self.visible = False

    def _draw(self, surface, manager):
        for tooltip in manager.query(ToolTipObject):
            if tooltip is self:
                continue
            if tooltip.visible:
                return

        title = self.font.render(self.title, True, RED)

        desc = [self.font.render(desc, True, BLUE) for desc in self.desc]

        self.rect.width = max(surface.get_rect().width for surface in [title] + desc)
        self.rect.height = sum(surface.get_rect().height for surface in [title] + desc)

        self.rect.topleft = pygame.mouse.get_pos()
        self.rect.top -= self._font_size
        self.rect.left += self._font_size

        if self.rect.right > WINDOW_SIZE[0]:
            self.rect.right = WINDOW_SIZE[0]
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > WINDOW_SIZE[1]:
            self.rect.bottom = WINDOW_SIZE[1]
        elif self.rect.top < 0:
            self.rect.top = 0

        pygame.draw.rect(surface, self.color, self.rect)
        text_offset = 0
        for text_surface in [title] + desc:
            text_rect = text_surface.get_rect()
            text_rect.topleft = self.rect.topleft
            text_rect.top += text_offset
            surface.blit(text_surface, text_rect)
            text_offset += text_rect.height

