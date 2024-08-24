import random

import pygame

from snake.actors.Snake import Snake
from snake.components.Screen import Screen


class Food:
    __food = None
    __x = None
    __y = None

    def __init__(self):
        self.__food = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
        self.randon_position()

    def randon_position(self):
        pixel_size = Screen.get_pixel_size()
        while True:
            self.__x = random.randint(1, (Screen.get_screen_width() - pixel_size) // pixel_size)
            self.__y = random.randint(1, (Screen.get_screen_height() - pixel_size) // pixel_size)

            if not Snake().collide_any_part((self.__x * pixel_size, self.__y * pixel_size)):
                self.__food.center = (self.__x * pixel_size, self.__y * pixel_size)
                break

        return self.__food

    def get_position(self):
        return self.__food.center

    def get_food_pixel(self):
        return self.__food
