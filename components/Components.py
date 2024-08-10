import pygame

from components.Screen import Screen
from actors.Snake import Snake
from actors.Food import Food


class Components:
    _INSTANCE = None
    _components = None
    __move_counter = 0
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
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] and Snake().get_snake_direction() != (0, Screen.get_pixel_size()):
            Snake().set_snake_direction((0, -Screen.get_pixel_size()))
        if key_pressed[pygame.K_DOWN] and Snake().get_snake_direction() != (0, -Screen.get_pixel_size()):
            Snake().set_snake_direction((0, Screen.get_pixel_size()))
        if key_pressed[pygame.K_LEFT] and Snake().get_snake_direction() != (Screen.get_pixel_size(), 0):
            Snake().set_snake_direction((-Screen.get_pixel_size(), 0))
        if key_pressed[pygame.K_RIGHT] and Snake().get_snake_direction() != (-Screen.get_pixel_size(), 0):
            Snake().set_snake_direction((Screen.get_pixel_size(), 0))

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

    @staticmethod
    def generate():
        Components.__draw_components()
        Screen.flip_display()

    @staticmethod
    def __draw_components():
        Screen.draw_food(Food().get_food_pixel())
        for i, part in enumerate(Snake().get_snake_body()):
            Screen.draw_snake(part, i / len(Snake().get_snake_body()))
