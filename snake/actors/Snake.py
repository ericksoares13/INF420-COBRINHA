import pygame

from snake.components.Screen import Screen


def collide_with_border(pos):
    x, y = pos
    if x < Screen().get_pixel_size() // 2:
        return True
    if y < Screen().get_pixel_size() // 2:
        return True
    if x >= Screen().get_screen_width() - (Screen().get_pixel_size() // 2):
        return True
    if y >= Screen().get_screen_height() - (Screen().get_pixel_size() // 2):
        return True
    return False


class Snake:
    __snake_direction = (0, 0)
    __last_direction = (0, 0)
    __snake_speed = 15
    __snake_body = None
    __snake_head = None
    __snake_tail = None
    __iteration = 0
    __score = 0

    def __init__(self):
        self.__snake_head = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
        x_position = (Screen().get_screen_width() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
        y_position = (Screen().get_screen_height() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
        self.__snake_head.center = (x_position, y_position)
        self.__snake_tail = self.__snake_head.copy()
        self.__snake_body = [self.__snake_head.copy()]

    def get_snake_speed(self):
        return self.__snake_speed

    def get_snake_body(self):
        return self.__snake_body

    def get_snake_size(self):
        return len(self.__snake_body)

    def get_snake_head_position(self):
        return self.__snake_head.center

    def get_snake_tail_position(self):
        return self.__snake_tail.center

    def get_snake_tail_direction(self):
        if self.get_snake_size() == 1:
            x, y = self.__snake_direction
            return -1 * x, -1 * y
        last = self.__snake_body[0]
        second_last = self.__snake_body[1]
        return last[0] - second_last[0], last[1] - second_last[1]

    def get_snake_direction(self):
        return self.__snake_direction

    def get_last_snake_direction(self):
        return self.__last_direction

    def get_score(self):
        return self.__score

    def get_iteration(self):
        return self.__iteration

    def set_snake_direction(self, new_direction):
        self.__snake_direction = new_direction

    def grow_snake(self):
        self.__snake_body.insert(0, self.__snake_tail.copy())
        self.__snake_head = self.__snake_tail
        self.__snake_body = self.__snake_body[::-1]
        self.__change_direction()
        self.__update_velocity()
        self.__score += 1

    def __change_direction(self):
        last = self.__snake_body[-1]
        second_last = self.__snake_body[-2]
        self.__snake_direction = (last[0] - second_last[0], last[1] - second_last[1])
        self.__last_direction = self.__snake_direction

    def __update_velocity(self):
        max_length = Screen().get_quant_pixel()
        m = -15 / (max_length - 1)
        self.__snake_speed = m * self.get_snake_size() - m + 15
        if self.__snake_speed < 5:
            self.__snake_speed = 5

    def move_snake(self):
        self.move_snake_whitout_colision()

        x, y = self.get_snake_head_position()
        x -= Screen().get_pixel_size() // 2
        y -= Screen().get_pixel_size() // 2
        if self.collide_without_head((x, y)):
            Screen().end_game()
        if self.snake_collide_with_border():
            Screen().end_game()

    def move_snake_whitout_colision(self):
        self.__last_direction = self.__snake_direction
        self.__snake_head.move_ip(self.__snake_direction)
        self.__snake_body.append(self.__snake_head.copy())
        self.__snake_tail = self.__snake_body[0]
        self.__snake_body.pop(0)
        if self.__last_direction != (0, 0):
            self.__iteration += 1

    def collide_any_part(self, pos):
        aux = Screen.get_pixel_size() // 2
        return self.get_snake_head_position() == pos or self.collide_without_head((pos[0] - aux, pos[1] - aux))

    def collide_without_head(self, pos):
        for part in self.__snake_body[:-1]:
            if part.collidepoint(pos):
                return True
        return False

    def snake_collide_with_border(self):
        return collide_with_border(self.get_snake_head_position())

    def start_snake(self):
        self.__snake_head = pygame.rect.Rect(0, 0, Screen().get_pixel_size(), Screen().get_pixel_size())
        x_position = (Screen().get_screen_width() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
        y_position = (Screen().get_screen_height() // (Screen.get_pixel_size() * 2)) * Screen().get_pixel_size()
        self.__snake_head.center = (x_position, y_position)
        self.__snake_body = [self.__snake_head.copy()]
        self.__snake_direction = (0, 0)
        self.__last_direction = (0, 0)
        self.__iteration = 0
        self.__score = 0
