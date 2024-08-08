import pygame
from components.Screen import Screen


class Snake:
    _INSTANCE = None
    __SNAKE_HEAD = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Snake, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            Snake.__SNAKE_HEAD = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
            x_position = (Screen().get_screen_width() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
            y_position = (Screen().get_screen_height() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
            Snake.__SNAKE_HEAD.center = (x_position, y_position)
            self._initialized = True

    @staticmethod
    def get_snake_pixel():
        return Snake.__SNAKE_HEAD.copy()
