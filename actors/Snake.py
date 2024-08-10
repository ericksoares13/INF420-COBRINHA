import pygame

from components.Screen import Screen


class Snake:
    _INSTANCE = None
    __snake_direction = (0, 0)
    __snake_speed = 15
    __snake_body = None
    __snake_head = None
    __snake_tail = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Snake, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            Snake.__snake_head = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
            x_position = (Screen().get_screen_width() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
            y_position = (Screen().get_screen_height() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
            Snake.__snake_head.center = (x_position, y_position)
            Snake.__snake_body = [Snake.__snake_head.copy()]
            self._initialized = True

    @staticmethod
    def get_snake_speed():
        return Snake.__snake_speed

    @staticmethod
    def get_snake_body():
        return Snake.__snake_body

    @staticmethod
    def get_snake_head_position():
        return Snake.__snake_head.center

    @staticmethod
    def get_snake_direction():
        return Snake.__snake_direction

    @staticmethod
    def set_snake_direction(new_direction):
        Snake.__snake_direction = new_direction

    @staticmethod
    def grow_snake():
        Snake.__snake_body.insert(0, Snake.__snake_tail.copy())
        Snake.__snake_head = Snake.__snake_tail
        Snake.__snake_body = Snake.__snake_body[::-1]
        Snake.__change_direction()

    @staticmethod
    def __change_direction():
        last = Snake.__snake_body[-1]
        second_last = Snake.__snake_body[-2]
        Snake.__snake_direction = (last[0] - second_last[0], last[1] - second_last[1])

    @staticmethod
    def move_snake():
        Snake.__snake_head.move_ip(Snake.__snake_direction)
        Snake.__snake_body.append(Snake.__snake_head.copy())
        Snake.__snake_tail = Snake.__snake_body[0]
        Snake.__snake_body.pop(0)

        if Snake().collide_without_head(Snake().get_snake_head_position()):
            Screen().end_game()

    @staticmethod
    def collide_any_part(pos):
        return Snake().get_snake_head_position() == pos or Snake().collide_without_head(pos)

    @staticmethod
    def collide_without_head(pos):
        for part in Snake.__snake_body[0:-2]:
            if part.collidepoint(pos):
                return True
        return False
