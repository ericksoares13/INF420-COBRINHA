from enum import Enum
import random

import numpy as np
import pygame

from snake.components.Screen import Screen


class Direction(Enum):
    RIGHT = pygame.K_RIGHT
    LEFT = pygame.K_LEFT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN


direction_map = {
    (0, -Screen.get_pixel_size()): pygame.K_UP,
    (0, Screen.get_pixel_size()): pygame.K_DOWN,
    (-Screen.get_pixel_size(), 0): pygame.K_LEFT,
    (Screen.get_pixel_size(), 0): pygame.K_RIGHT
}


class Components:
    __move_counter = 0
    __key = pygame.K_SPACE
    _ate = False

    def __init__(self):
        # Não tem parâmetros
        pass

    def process(self, snake, food):
        self.__move_counter += 1

        self.__process_key(snake)

        if self.__move_counter > snake.get_snake_speed():
            snake.move_snake()
            self.__move_counter = 0

        self.__feeding_snake(snake, food)

    def __process_key(self, snake):
        key_pressed = self.__key
        if key_pressed == pygame.K_UP and snake.get_last_snake_direction() != (0, Screen.get_pixel_size()):
            snake.set_snake_direction((0, -Screen.get_pixel_size()))
        if key_pressed == pygame.K_DOWN and snake.get_last_snake_direction() != (0, -Screen.get_pixel_size()):
            snake.set_snake_direction((0, Screen.get_pixel_size()))
        if key_pressed == pygame.K_LEFT and snake.get_last_snake_direction() != (Screen.get_pixel_size(), 0):
            snake.set_snake_direction((-Screen.get_pixel_size(), 0))
        if key_pressed == pygame.K_RIGHT and snake.get_last_snake_direction() != (-Screen.get_pixel_size(), 0):
            snake.set_snake_direction((Screen.get_pixel_size(), 0))

    def set_key(self, key):
        self.__key = key

    def __feeding_snake(self, snake, food):
        if snake.get_snake_head_position() == food.get_position():
            self._ate = True

    def update(self, snake, food):
        if self._ate:
            snake.grow_snake()
            if snake.get_snake_size() == (Screen.get_screen_height() // Screen.get_pixel_size()) ** 2:
                food.end_food()
                Screen.end_game()
            else:
                food.randon_position()
                self._ate = False
                self.set_key(direction_map[snake.get_last_snake_direction()])

    def generate(self, snake, food):
        if Screen.get_state():
            self.__draw_components(snake, food)
            Screen.flip_display()

    def __draw_components(self, snake, food):
        Screen.draw_food(food.get_food_pixel())
        snake_body = snake.get_snake_body()
        for i, part in enumerate(snake_body):
            if len(snake.get_snake_body()) == 1:
                Screen.draw_snake(part, 0.5, snake_body[i-1] if i > 0 else None,
                                  snake_body[i+1] if i < len(snake_body) - 1 else None)
            else:
                Screen.draw_snake(part, i / len(snake.get_snake_body()), snake_body[i-1] if i > 0 else None,
                                  snake_body[i+1] if i < len(snake_body) - 1 else None)

    def __get_key(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]

        key_mapping = {
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_UP: Direction.UP
        }

        key = key_mapping.get(self.__key, None)

        if key is None:
            key = random.choice(clock_wise)
        idx = clock_wise.index(key)

        if np.array_equal(action, [1, 0, 0]):       # reto
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):     # direita
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:                                       # esquerda
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        return new_dir.value

    def train(self, snake, food, action, mode='ia'):
        self.set_key(self.__get_key(action))
        self.__process_key(snake)
        snake.move_snake_whitout_colision()
        self.__feeding_snake(snake, food)

        if ((snake.snake_collide_with_border() or snake.collide_without_head(snake.get_snake_head_position()))
                or (mode == 'train' and snake.get_iteration() >
                    10 * snake.get_snake_size() * (Screen().get_screen_width() // Screen.get_pixel_size()))):
            return -10, True, snake.get_score()

        reward = 0
        if self._ate:
            reward = 10

        self.update(snake, food)
        self.generate(snake, food)

        return reward, False, snake.get_score()

    def monte_carlo(self, snake, food):
        self.__feeding_snake(snake, food)
        self.update(snake, food)
        self.generate(snake, food)
