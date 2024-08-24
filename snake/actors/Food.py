import random

import pygame

from snake.actors.Snake import Snake
from snake.components.Screen import Screen


class Food:
    _INSTANCE = None
    __food = None
    __x = None
    __y = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Food, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            Food.__food = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
            Food.randon_position()
            self._initialized = True

    @staticmethod
    def randon_position():
        pixel_size = Screen.get_pixel_size()
        while True:
            Food.__x = random.randint(1, (Screen.get_screen_width() - pixel_size) // pixel_size)
            Food.__y = random.randint(1, (Screen.get_screen_height() - pixel_size) // pixel_size)

            if not Snake().collide_any_part((Food.__x * pixel_size, Food.__y * pixel_size)):
                Food.__food.center = (Food.__x * pixel_size, Food.__y * pixel_size)
                break

        return Food.__food

    @staticmethod
    def get_position():
        return Food.__food.center

    @staticmethod
    def get_food_pixel():
        return Food.__food
