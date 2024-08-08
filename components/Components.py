from components.Screen import Screen
from actors.Snake import Snake
from actors.Food import Food


class Components:
    _INSTANCE = None
    _components = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Components, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    @staticmethod
    def process():
        pass

    @staticmethod
    def update():
        pass

    @staticmethod
    def generate():
        Components._draw_components()

    @staticmethod
    def _draw_components():
        Screen.draw_snake(Snake().get_snake_pixel())
        Screen.draw_food(Food().get_food_pixel())
