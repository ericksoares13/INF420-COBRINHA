from enum import Enum
import random

import numpy as np
import pygame

from snake.components.Screen import Screen
from snake.actors.Snake import Snake
from snake.actors.Food import Food


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
    _INSTANCE = None
    _components = None
    __move_counter = 0
    __key = pygame.K_SPACE
    _ate = False

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Components, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    @staticmethod
    def process():
        Components.__move_counter += 1

        Components.__process_key()

        if Components.__move_counter > Snake().get_snake_speed():
            Snake().move_snake()
            Components.__move_counter = 0

        Components.__feeding_snake()

    @staticmethod
    def __process_key():
        key_pressed = Components.__key
        if key_pressed == pygame.K_UP and Snake().get_snake_direction() != (0, Screen.get_pixel_size()):
            Snake().set_snake_direction((0, -Screen.get_pixel_size()))
        if key_pressed == pygame.K_DOWN and Snake().get_snake_direction() != (0, -Screen.get_pixel_size()):
            Snake().set_snake_direction((0, Screen.get_pixel_size()))
        if key_pressed == pygame.K_LEFT and Snake().get_snake_direction() != (Screen.get_pixel_size(), 0):
            Snake().set_snake_direction((-Screen.get_pixel_size(), 0))
        if key_pressed == pygame.K_RIGHT and Snake().get_snake_direction() != (-Screen.get_pixel_size(), 0):
            Snake().set_snake_direction((Screen.get_pixel_size(), 0))
        if key_pressed == pygame.K_ESCAPE:
            Screen.end_game()

    @staticmethod
    def set_key(key):
        Components.__key = key

    @staticmethod
    def __feeding_snake():
        if Snake().get_snake_head_position() == Food().get_position():
            Components._ate = True

    @staticmethod
    def update():
        if Components._ate:
            Snake().grow_snake()
            Food().randon_position()
            Components._ate = False
            Components.set_key(direction_map[Snake.get_snake_direction()])

    @staticmethod
    def generate():
        Components.__draw_components()
        Screen.flip_display()

    @staticmethod
    def __draw_components():
        Screen.draw_food(Food().get_food_pixel())
        for i, part in enumerate(Snake().get_snake_body()):
            if len(Snake().get_snake_body()) == 1:
                Screen.draw_snake(part, 0.5)
            else:
                Screen.draw_snake(part, i / len(Snake().get_snake_body()))

    @staticmethod
    def __get_key(action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]

        key_mapping = {
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_UP: Direction.UP
        }

        key = key_mapping.get(Components.__key, None)

        if key is None:
            key = random.choice(clock_wise)
        idx = clock_wise.index(key)

        if np.array_equal(action, [1, 0, 0]):       # reto
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):     # direita
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:                                           # esquerda
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        return new_dir.value

    @staticmethod
    def train(action):
        game_over = False

        Components.set_key(Components.__get_key(action))
        Components.__process_key()
        Snake().move_snake_whitout_colision()
        Components.__feeding_snake()

        if ((Snake().snake_collide_with_border() or Snake().collide_without_head(Snake().get_snake_head_position()))
                or Snake().get_train_it() > 100 * Snake().get_snake_size()):
            game_over = True

        reward = 0
        if game_over:
            reward = -10
        elif Components._ate:
            reward = 10

        Components.update()
        Components.generate()

        return reward, game_over, Snake().get_score()
