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
        screen_width = Screen.get_screen_width()
        screen_height = Screen.get_screen_height()

        possible_positions = [
            (x * pixel_size, y * pixel_size)
            for x in range(1, (screen_width - pixel_size) // pixel_size)
            for y in range(1, (screen_height - pixel_size) // pixel_size)
        ]

        valid_positions = [pos for pos in possible_positions if not self.snake.collide_any_part(pos)]

        if valid_positions:
            self.__x, self.__y = random.choice(valid_positions)
            self.__food.center = (self.__x, self.__y)

        return self.__food

    def end_food(self):
        self.__food.center = (-1000, -1000)

    def get_position(self):
        return self.__food.center

    def get_food_pixel(self):
        return self.__food
