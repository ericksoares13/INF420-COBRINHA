import random

import pygame

from components.Screen import Screen


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
        Food.__x = random.randint(0, Screen.get_screen_width() // (Screen.get_pixel_size() * 2))
        Food.__y = random.randint(0, Screen.get_screen_height() // (Screen.get_pixel_size() * 2))
        Food.__food.center = (Food.__x * Screen.get_pixel_size(), Food.__y * Screen.get_pixel_size())
        return Food.__food

    @staticmethod
    def get_position():
        return Food.__food.center

    @staticmethod
    def get_food_pixel():
        return Food.__food
