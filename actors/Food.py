import random
from screen.Screen import Screen


class Food:
    _INSTANCE = None
    __x = None
    __y = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Food, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        pass

    @staticmethod
    def randon_position():
        Food.__x = random.randint(0, Screen.get_screen_width())
        Food.__y = random.randint(0, Screen.get_screen_height())
        return Food.__x, Food.__y

    @staticmethod
    def get_position():
        return Food.__x, Food.__y
