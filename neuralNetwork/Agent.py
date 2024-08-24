import torch
import random
import numpy as np
from collections import deque
from neuralNetwork.NeuralNetwork import LinearQNet, QTrainer

from snake.actors.Food import Food
from snake.actors.Snake import Snake
from snake.components.Screen import Screen

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


def collide(point):
    return Snake().collide_with_border(point) or Snake().collide_without_head(point)


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self._load_model()

    def _load_model(self):
        try:
            self.model.load_state_dict(torch.load("./model/model.pth"))
            print("Modelo carregado com sucesso.")
        except FileNotFoundError:
            print("Nenhum modelo salvo encontrado, iniciando novo treinamento.")
        except Exception as e:
            print(f"Erro ao carregar o modelo: {e}")

    def get_state(self):
        head_x, head_y = Snake().get_snake_head_position()
        food_x, food_y = Food().get_position()

        point_l = (head_x - Screen.get_pixel_size(), head_y)
        point_r = (head_x + Screen.get_pixel_size(), head_y)
        point_u = (head_x, head_y - Screen.get_pixel_size())
        point_d = (head_x, head_y + Screen.get_pixel_size())

        dir_l = Snake().get_snake_direction() == (-Screen.get_pixel_size(), 0)
        dir_r = Snake().get_snake_direction() == (Screen.get_pixel_size(), 0)
        dir_u = Snake().get_snake_direction() == (0, -Screen.get_pixel_size())
        dir_d = Snake().get_snake_direction() == (0, Screen.get_pixel_size())

        state = [
            ((dir_r and collide(point_r)) or
             (dir_l and collide(point_l)) or
             (dir_u and collide(point_u)) or
             (dir_d and collide(point_d))),

            ((dir_u and collide(point_r)) or
             (dir_d and collide(point_l)) or
             (dir_l and collide(point_u)) or
             (dir_r and collide(point_d))),

            ((dir_d and collide(point_r)) or
             (dir_u and collide(point_l)) or
             (dir_r and collide(point_u)) or
             (dir_l and collide(point_d))),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            food_x < head_x,
            food_x > head_x,
            food_y < head_y,
            food_y > head_y
        ]
        return np.array(state, dtype=int)

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
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
