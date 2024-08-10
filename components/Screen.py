import pygame


class Screen:
    # 10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 48, 60, 72, 80, 90, 120, 144, 180, 240 e 360
    __SCREEN_WIDTH = 720
    __SCREEN_HEIGHT = 720
    __PIXEL_SIZE = 60
    __SCREEN = None
    __running = True
    _INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Screen, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            Screen.__SCREEN = pygame.display.set_mode((Screen.__SCREEN_WIDTH, Screen.__SCREEN_HEIGHT))
            Screen.__SCREEN.fill("black")
            self._initialized = True

    @staticmethod
    def get_screen_width():
        return Screen.__SCREEN_WIDTH

    @staticmethod
    def get_screen_height():
        return Screen.__SCREEN_HEIGHT

    @staticmethod
    def get_pixel_size():
        return Screen.__PIXEL_SIZE

    @staticmethod
    def get_state():
        return Screen.__running

    @staticmethod
    def draw_snake(part, ratio):
        color = pygame.Color(
            int(pygame.Color("purple").r * (1 - ratio) + pygame.Color("blue").r * ratio),
            int(pygame.Color("purple").g * (1 - ratio) + pygame.Color("blue").g * ratio),
            int(pygame.Color("purple").b * (1 - ratio) + pygame.Color("blue").b * ratio)
        )
        pygame.draw.rect(Screen.__SCREEN, color, part)

    @staticmethod
    def draw_food(food):
        pygame.draw.rect(Screen.__SCREEN, "red", food)

    @staticmethod
    def flip_display():
        pygame.display.update()
        Screen.__SCREEN.fill("white")

    @staticmethod
    def end_game():
        Screen.__running = False
