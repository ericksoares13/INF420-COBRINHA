import random

import pygame

from snake.components.Screen import Screen


class Food:
    __food = None
    __x = None
    __y = None

    def __init__(self, snake):
        self.__food = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
        self.snake = snake
        self.randon_position()

    def randon_position(self):
        pixel_size = Screen.get_pixel_size()
        while True:
            self.__x = random.randint(1, (Screen.get_screen_width() - pixel_size) // pixel_size)
            self.__y = random.randint(1, (Screen.get_screen_height() - pixel_size) // pixel_size)
            self.__x = self.__x * pixel_size
            self.__y = self.__y * pixel_size

            if not self.snake.collide_any_part((self.__x, self.__y)):
                self.__food.center = (self.__x, self.__y)
                break

        return self.__food

    def get_position(self):
        return self.__food.center

    def get_food_pixel(self):
        return self.__food
