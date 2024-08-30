import random
import copy
import numpy as np

from snake.components.Screen import Screen
from snake.actors.Snake import collide_with_border


class MonteCarlo:
    def __init__(self, component, snake, food):
        self.component = component
        self.snake = snake
        self.food = food

    def monte_carlo_agente(self, simulacoes=40):
        pontuacoes = {}

        for direcao in [(0, -Screen().get_pixel_size()), (0, Screen().get_pixel_size()),
                        (-Screen().get_pixel_size(), 0), (Screen().get_pixel_size(), 0)]:
            if self.movimento_valido(direcao):
                pontuacoes[direcao] = self.simular_jogo(direcao, simulacoes)

        if pontuacoes:
            pontuacoes_valores = list(pontuacoes.values())
            if all(p == pontuacoes_valores[0] for p in pontuacoes_valores):
                melhor_direcao = random.choice(list(pontuacoes.keys()))
            else:
                melhor_direcao = max(pontuacoes, key=pontuacoes.get)
        else:
            melhor_direcao = random.choice([(0, -Screen().get_pixel_size()), (0, Screen().get_pixel_size()),
                                            (-Screen().get_pixel_size(), 0), (Screen().get_pixel_size(), 0)])

        return melhor_direcao

    def simular_jogo(self, direcao, simulacoes=40):
        pontuacoes = []

        for _ in range(simulacoes):
            copia_jogo = copy.deepcopy(self)
            copia_jogo.snake.set_snake_direction(direcao)
            copia_jogo.snake.move_snake_whitout_colision()
            comidas = 0
            movimentos = 1

            if copia_jogo.snake.get_snake_head_position() == copia_jogo.food.get_position():
                copia_jogo.snake.grow_snake()
                if copia_jogo.snake.get_snake_size() == ((Screen.get_screen_height() // Screen.get_pixel_size()) - 1) ** 2:
                    copia_jogo.food.end_food()
                else:
                    copia_jogo.food.randon_position()
                    comidas += 1

            while (movimentos < copia_jogo.snake.get_snake_size() *
                   (Screen().get_screen_width() // Screen().get_pixel_size())):
                possiveis = copy.deepcopy([(0, -Screen().get_pixel_size()), (0, Screen().get_pixel_size()),
                                           (-Screen().get_pixel_size(), 0), (Screen().get_pixel_size(), 0)])
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

            tamanho_cobra = int(copia_jogo.snake.get_snake_size())
            expoente = tamanho_cobra * 0.25

            pontuacao = (comidas + 1) * (movimentos ** expoente)
            pontuacoes.append(pontuacao)

        return np.mean(pontuacoes) if pontuacoes else 0

    def movimento_valido(self, direcao):
        nova_pos = (self.snake.get_snake_head_position()[0] - (Screen().get_pixel_size() // 2) + direcao[0],
                    self.snake.get_snake_head_position()[1] - (Screen().get_pixel_size() // 2) + direcao[1])
        return not (collide_with_border(nova_pos) or self.snake.collide_without_head(nova_pos))

    def agente(self):
        if self.snake.get_last_snake_direction() == (0, 0):
            direcao = random.choice([(0, -Screen().get_pixel_size()), (0, Screen().get_pixel_size()),
                                     (-Screen().get_pixel_size(), 0), (Screen().get_pixel_size(), 0)])
            self.snake.set_snake_direction(direcao)
        else:
            direcao = self.monte_carlo_agente()
            self.snake.set_snake_direction(direcao)
        self.snake.move_snake()
