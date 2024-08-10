import pygame


class Screen:
    # 18, 20, 30, 36, 50
    __SCREEN_WIDTH = 900
    __SCREEN_HEIGHT = 900
    __PIXEL_SIZE = 50
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
            Screen.__SCREEN.fill("white")
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
    def get_quant_pixel():
        return ((Screen.__SCREEN_HEIGHT // Screen.__PIXEL_SIZE) - 1) ** 2

    @staticmethod
    def get_state():
        return Screen.__running

    @staticmethod
    def draw_snake(part, ratio):
        border_rect = part.inflate(2, 2)
        pygame.draw.rect(Screen.__SCREEN, "black", border_rect)
        color = pygame.Color(
            int(pygame.Color("purple").r * (1 - ratio) + pygame.Color("blue").r * ratio),
            int(pygame.Color("purple").g * (1 - ratio) + pygame.Color("blue").g * ratio),
            int(pygame.Color("purple").b * (1 - ratio) + pygame.Color("blue").b * ratio)
        )
        pygame.draw.rect(Screen.__SCREEN, color, part)

    @staticmethod
    def draw_food(food):
        border_rect = food.inflate(2, 2)
        pygame.draw.rect(Screen.__SCREEN, "black", border_rect)
        pygame.draw.rect(Screen.__SCREEN, "red", food)

    @staticmethod
    def flip_display():
        pygame.display.update()
        Screen.__SCREEN.fill("white")
        w = Screen.__SCREEN_WIDTH
        h = Screen.__SCREEN_HEIGHT
        b = Screen.__PIXEL_SIZE // 2
        for x in range(b, w, b * 2):
            pygame.draw.line(Screen.__SCREEN, (230, 230, 230), (x, 0), (x, h))
        for y in range(b, h, b * 2):
            pygame.draw.line(Screen.__SCREEN, (230, 230, 230), (0, y), (w, y))
        pygame.draw.rect(Screen.__SCREEN, "black", pygame.Rect(0, 0, w, b))
        pygame.draw.rect(Screen.__SCREEN, "black", pygame.Rect(0, 0, b, h))
        pygame.draw.rect(Screen.__SCREEN, "black", pygame.Rect(0, h - b, w, b))
        pygame.draw.rect(Screen.__SCREEN, "black", pygame.Rect(w - b, 0, b, h))

    @staticmethod
    def end_game():
        Screen.__running = False
