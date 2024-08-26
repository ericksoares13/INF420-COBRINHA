import pygame


class Screen:
    # 20, 26, 30, 52
    __SCREEN_WIDTH = 780
    __SCREEN_HEIGHT = 780
    __PIXEL_SIZE = 52
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
    def draw_snake(part, ratio, partBefore, partAfter):
        border_color = "black"
        color = pygame.Color(
            int(pygame.Color("purple").r * (1 - ratio) + pygame.Color("blue").r * ratio),
            int(pygame.Color("purple").g * (1 - ratio) + pygame.Color("blue").g * ratio),
            int(pygame.Color("purple").b * (1 - ratio) + pygame.Color("blue").b * ratio)
        )
        pygame.draw.rect(Screen.__SCREEN, color, part)

        x, y, width, height = part.x, part.y, part.width, part.height

        def draw_border(sides):
            if 'top' in sides:
                pygame.draw.line(Screen.__SCREEN, border_color, (x, y), (x + width, y))
            if 'bottom' in sides:
                pygame.draw.line(Screen.__SCREEN, border_color, (x, y + height), (x + width, y + height))
            if 'left' in sides:
                pygame.draw.line(Screen.__SCREEN, border_color, (x, y), (x, y + height))
            if 'right' in sides:
                pygame.draw.line(Screen.__SCREEN, border_color, (x + width, y), (x + width, y + height))

        directions = {
            (-52, 0): 'left',
            (52, 0): 'right',
            (0, -52): 'top',
            (0, 52): 'bottom'
        }

        delta_before = (part.x - partBefore.x, part.y - partBefore.y) if partBefore else (0, 0)
        delta_after = (partAfter.x - part.x, partAfter.y - part.y) if partAfter else (0, 0)

        if delta_before == delta_after:
            if delta_before in directions:
                if delta_before in [(-52, 0), (52, 0)]:
                    draw_border(['top', 'bottom'])
                elif delta_before in [(0, -52), (0, 52)]:
                    draw_border(['left', 'right'])
            else:
                draw_border(['top', 'bottom', 'left', 'right'])
        elif delta_after == (0, 0):
            if delta_before == (-52, 0):
                draw_border(['top', 'bottom', 'left'])
            elif delta_before == (52, 0):
                draw_border(['top', 'bottom', 'right'])
            elif delta_before == (0, -52):
                draw_border(['left', 'right', 'top'])
            elif delta_before == (0, 52):
                draw_border(['left', 'right', 'bottom'])
        elif delta_before == (0, 0):
            if delta_after == (-52, 0):
                draw_border(['top', 'bottom', 'right'])
            elif delta_after == (52, 0):
                draw_border(['top', 'bottom', 'left'])
            elif delta_after == (0, -52):
                draw_border(['left', 'right', 'bottom'])
            elif delta_after == (0, 52):
                draw_border(['left', 'right', 'top'])
        else:
            if directions[delta_before] == 'left' and directions[delta_after] == 'top':
                draw_border(['left', 'bottom'])
            elif directions[delta_before] == 'left' and directions[delta_after] == 'bottom':
                draw_border(['left', 'top'])
            elif directions[delta_before] == 'right' and directions[delta_after] == 'top':
                draw_border(['right', 'bottom'])
            elif directions[delta_before] == 'right' and directions[delta_after] == 'bottom':
                draw_border(['right', 'top'])
            elif directions[delta_before] == 'top' and directions[delta_after] == 'left':
                draw_border(['top', 'right'])
            elif directions[delta_before] == 'top' and directions[delta_after] == 'right':
                draw_border(['top', 'left'])
            elif directions[delta_before] == 'bottom' and directions[delta_after] == 'left':
                draw_border(['bottom', 'right'])
            elif directions[delta_before] == 'bottom' and directions[delta_after] == 'right':
                draw_border(['bottom', 'left'])


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

    @staticmethod
    def start_game():
        Screen.__running = True
