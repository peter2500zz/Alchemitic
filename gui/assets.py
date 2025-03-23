import pygame
import base64
import io

from core.logger import new_logger

from gui.error import AssetsNotInitializedYet

logger = new_logger('GUI.AssetsLoader')


class AssetsLoader:
    _instance = None

    _default_image = None
    loaded_image: dict[str, pygame.Surface] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def init(cls, assets: dict[str, dict[str, str]]):
        if not cls._default_image:
            # 经典紫黑块
            cls._default_image = pygame.image.load(io.BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAACXBIWXMAAAAnAAAAJwEqCZFPAAAAEklEQVQImWP4z/CfAQL+M/wHABvyA/3mbB67AAAAAElFTkSuQmCC')))

        def load(asset_path):
            try:
                return pygame.image.load(asset_path).convert_alpha()
            except FileNotFoundError:
                logger.warning(f'无法加载资源 {asset_path}')
                return cls._default_image

        logger.info('初始化资源')

        for image in assets['images']:
            cls.loaded_image[image] = load(f'assets/images/{image}.png')

    @classmethod
    def get_image(cls, name: str):
        if not cls._default_image:
            raise AssetsNotInitializedYet(name)

        return cls.loaded_image.get(name, cls._default_image)

