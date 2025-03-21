import pygame
import base64
import io

from core.logger import new_logger

from gui.error import AssetsNotInitializedYet

logger = new_logger('GUI.AssetsLoader')


class AssetsLoader:
    _instance = None

    _default_asset = None
    loaded_assets: dict[str, pygame.Surface] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def load(cls, assets: dict[str, str]):
        if not cls._default_asset:
            # 经典紫黑块
            cls._default_asset = pygame.image.load(io.BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAACXBIWXMAAAAnAAAAJwEqCZFPAAAAEklEQVQImWP4z/CfAQL+M/wHABvyA/3mbB67AAAAAElFTkSuQmCC')))

        def load(asset_path):
            try:
                return pygame.image.load(asset_path).convert_alpha()
            except FileNotFoundError:
                logger.warning(f'无法加载资源 {asset_path}')
                return cls._default_asset

        logger.info('初始化资源')

        for name, path in assets.items():
            cls.loaded_assets[name] = load(path)

    @classmethod
    def get(cls, name: str):
        if not cls._default_asset:
            raise AssetsNotInitializedYet(name)

        return cls.loaded_assets.get(name, cls._default_asset)


standard_assets = {
    'apple': 'assets/apple.png',
    'feather': 'assets/feather.png',
    'coal': 'assets/coal.png',
}
