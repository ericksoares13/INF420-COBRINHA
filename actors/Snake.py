import pygame
from screen.Screen import Screen


class Snake:
    _INSTANCE = None
    __SNAKE_HEAD = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Snake, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        Snake.__SNAKE_HEAD = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
        Snake.__SNAKE_HEAD.center = (Screen().get_screen_width() / 2, Screen().get_screen_height() / 2)

    @staticmethod
    def get_snake_pixel():
        return Snake.__SNAKE_HEAD.copy()
