import random
import copy

import numpy as np

from snake.components.Screen import Screen
from snake.actors.Snake import collide_with_border

direcoes_possiveis = [(0, -Screen().get_pixel_size()), (0, Screen().get_pixel_size()),
                      (-Screen().get_pixel_size(), 0), (Screen().get_pixel_size(), 0)]


class MonteCarlo:
    def __init__(self, component, snake, food):
        self.component = component
        self.snake = snake
        self.food = food

    def monte_carlo_agente(self, simulacoes=150):
        pontuacoes = {}

        for direcao in direcoes_possiveis:
            if self.movimento_valido(direcao):
                pontuacoes[direcao] = self.simular_jogo(direcao, simulacoes)

        if not pontuacoes:
            return random.choice(direcoes_possiveis)

        if all(pontuacao == list(pontuacoes.values())[0] for pontuacao in pontuacoes.values()):
            return random.choice(list(pontuacoes.keys()))

        melhor_direcao = max(pontuacoes, key=pontuacoes.get)
        return melhor_direcao

    def simular_jogo(self, direcao, simulacoes=150):
        pontuacoes = []
        for _ in range(simulacoes):
            copia_jogo = copy.deepcopy(self)
            copia_jogo.snake.set_snake_direction(direcao)
            copia_jogo.snake.move_snake_whitout_colision()
            comidas = 0
            movimentos = 0

            while (movimentos < copia_jogo.snake.get_snake_size() *
                   (Screen().get_screen_width() // Screen().get_pixel_size())):
                possiveis = copy.deepcopy(direcoes_possiveis)
                while possiveis:
                    direcao_aleatoria = random.choice(possiveis)

                    if copia_jogo.movimento_valido(direcao_aleatoria):
                        copia_jogo.snake.set_snake_direction(direcao_aleatoria)
                        copia_jogo.snake.move_snake_whitout_colision()

                        movimentos += 1

                        if copia_jogo.snake.get_snake_head_position() == copia_jogo.food.get_position():
                            copia_jogo.snake.grow_snake()
                            copia_jogo.food.randon_position()
                            comidas += 1
                        break
                    else:
                        possiveis.remove(direcao_aleatoria)

                if not possiveis:
                    break

            pontuacao = comidas * (movimentos ** 6)
            pontuacoes.append(pontuacao)

        return np.mean(pontuacoes) if pontuacoes else 0

    def movimento_valido(self, direcao):
        nova_pos = (self.snake.get_snake_head_position()[0] + direcao[0],
                    self.snake.get_snake_head_position()[1] + direcao[1])
        return not (collide_with_border(nova_pos) or self.snake.collide_without_head(nova_pos))

    def agente(self):
        if self.snake.get_snake_direction() == (0, 0):
            direcao = random.choice(direcoes_possiveis)
            self.snake.set_snake_direction(direcao)
        else:
            direcao = self.monte_carlo_agente()
            self.snake.set_snake_direction(direcao)
        self.snake.move_snake()
