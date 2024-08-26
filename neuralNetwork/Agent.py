import torch
import random
import numpy as np
import math
from collections import deque
from neuralNetwork.NeuralNetwork import LinearQNet, QTrainer

from snake.actors.Snake import collide_with_border
from snake.components.Screen import Screen

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self, snake, food):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(16, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self._load_model()
        self.snake = snake
        self.food = food

    def _load_model(self):
        try:
            self.model.load_state_dict(torch.load("./model/model.pth"))
            print("Modelo carregado com sucesso.")
        except FileNotFoundError:
            print("Nenhum modelo salvo encontrado, iniciando novo treinamento.")
        except Exception as e:
            print(f"Erro ao carregar o modelo: {e}")

    def get_state(self):
        head_x, head_y = self.snake.get_snake_head_position()
        food_x, food_y = self.food.get_position()

        point_l = (head_x - Screen.get_pixel_size(), head_y)
        point_r = (head_x + Screen.get_pixel_size(), head_y)
        point_u = (head_x, head_y - Screen.get_pixel_size())
        point_d = (head_x, head_y + Screen.get_pixel_size())

        dir_l = self.snake.get_snake_direction() == (-Screen.get_pixel_size(), 0)
        dir_r = self.snake.get_snake_direction() == (Screen.get_pixel_size(), 0)
        dir_u = self.snake.get_snake_direction() == (0, -Screen.get_pixel_size())
        dir_d = self.snake.get_snake_direction() == (0, Screen.get_pixel_size())

        tail_x, tail_y = self.snake.get_snake_tail_position()
        dir_tail_x, dir_tail_y = self.snake.get_snake_tail_direction()
        new_tail = tail_x + dir_tail_x, tail_y + dir_tail_y

        distance_to_food = math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2)

        state = [
            self.collide(point_r, dir_r) or self.collide(point_l, dir_l)
            or self.collide(point_u, dir_u) or self.collide(point_d, dir_d),

            self.collide(point_r, dir_u) or self.collide(point_l, dir_d)
            or self.collide(point_u, dir_l) or self.collide(point_d, dir_r),

            self.collide(point_r, dir_d) or self.collide(point_l, dir_u)
            or self.collide(point_u, dir_r) or self.collide(point_d, dir_l),

            self.collide_snake((Screen.get_pixel_size(), 0), dir_r) or
            self.collide_snake((-Screen.get_pixel_size(), 0), dir_l) or
            self.collide_snake((0, -Screen.get_pixel_size()), dir_u) or
            self.collide_snake((0, Screen.get_pixel_size()), dir_d),

            self.collide_snake((Screen.get_pixel_size(), 0), dir_u) or
            self.collide_snake((-Screen.get_pixel_size(), 0), dir_d) or
            self.collide_snake((0, -Screen.get_pixel_size()), dir_l) or
            self.collide_snake((0, Screen.get_pixel_size()), dir_r),

            self.collide_snake((Screen.get_pixel_size(), 0), dir_d) or
            self.collide_snake((-Screen.get_pixel_size(), 0), dir_u) or
            self.collide_snake((0, -Screen.get_pixel_size()), dir_r) or
            self.collide_snake((0, Screen.get_pixel_size()), dir_l),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            food_x < head_x,
            food_x > head_x,
            food_y < head_y,
            food_y > head_y,

            self.collide(new_tail),

            distance_to_food / (Screen.get_screen_width() + Screen.get_screen_height())
        ]
        return np.array(state, dtype=int)

    def collide(self, point, direction=True):
        if not direction:
            return False
        point = point[0] - (Screen.get_pixel_size() // 2), point[1] - (Screen.get_pixel_size() // 2)
        return collide_with_border(point) or self.snake.collide_without_head(point)

    def collide_snake(self, dist, direction):
        if not direction:
            return False

        total = 0
        x, y = self.snake.get_snake_head_position()
        x -= (Screen.get_pixel_size() // 2)
        y -= (Screen.get_pixel_size() // 2)
        while 0 < x < Screen.get_screen_width() and 0 < y < Screen.get_screen_height():
            total += 1
            x += dist[0]
            y += dist[1]

            for segment in self.snake.get_snake_body():
                if (x, y) == segment.topleft:
                    return total

        return 0

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        final_move[move] = 1
        return final_move
