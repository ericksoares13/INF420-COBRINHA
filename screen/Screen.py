import pygame


class Screen:
    __SCREEN_WIDTH = 1280
    __SCREEN_HEIGHT = 720
    __PIXEL_SIZE = 20
    __SCREEN = None
    _INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Screen, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            Screen.__SCREEN = pygame.display.set_mode((Screen.__SCREEN_WIDTH, Screen.__SCREEN_HEIGHT))
            self._initialized = True

    @staticmethod
    def get_screen():
        return Screen.__SCREEN

    @staticmethod
    def get_screen_width():
        return Screen.__SCREEN_WIDTH

    @staticmethod
    def get_screen_height():
        return Screen.__SCREEN_HEIGHT

    @staticmethod
    def get_pixel_size():
        return Screen.__PIXEL_SIZE
