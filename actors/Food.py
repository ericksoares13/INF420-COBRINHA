import random

import pygame

from components.Screen import Screen


class Food:
    _INSTANCE = None
    __FOOD = None
    __x = None
    __y = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Food, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            Food.__FOOD = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
            Food.randon_position()
            self._initialized = True

    @staticmethod
    def randon_position():
        Food.__x = random.randint(0, Screen.get_screen_width()//Screen.get_pixel_size())
        Food.__y = random.randint(0, Screen.get_screen_height()//Screen.get_pixel_size())
        Food.__FOOD.center = (Food.__x*Screen.get_pixel_size(), Food.__y*Screen.get_pixel_size())
        return Food.__FOOD

    @staticmethod
    def get_position():
        return Food.__x, Food.__y

    @staticmethod
    def get_food_pixel():
        return Food.__FOOD
