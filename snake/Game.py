import pygame

from monteCarlo.MonteCarlo import MonteCarlo
from neuralNetwork.Agent import Agent
from snake.actors.Food import Food
from snake.actors.Snake import Snake
from snake.components.Components import Components
from snake.components.Screen import Screen

import matplotlib.pyplot as plt


def process_manual_events(component):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        component.set_key(pygame.K_UP)
    elif key[pygame.K_DOWN]:
        component.set_key(pygame.K_DOWN)
    elif key[pygame.K_LEFT]:
        component.set_key(pygame.K_LEFT)
    elif key[pygame.K_RIGHT]:
        component.set_key(pygame.K_RIGHT)
    elif key[pygame.K_ESCAPE]:
        component.set_key(pygame.K_ESCAPE)


def manual_game():
    component = Components()
    snake = Snake()
    food = Food(snake)
    clock = pygame.time.Clock()

    while Screen().get_state():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Screen.end_game()
                return

        process_manual_events(component)

        component.process(snake, food)
        component.update(snake, food)
        component.generate(snake, food)

        clock.tick(60)


def plot(scores, mean_scores, filename='./model/plot.png'):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Scores')
    plt.plot(mean_scores, label='Mean Scores')
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.legend()
    plt.savefig(filename)


def reset_game(sanke, component, food):
    Screen().start_game()
    sanke.start_snake()
    component.set_key(pygame.K_SPACE)
    food.randon_position()


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    component = Components()
    snake = Snake()
    food = Food(snake)
    agent = Agent(snake, food)
    clock = pygame.time.Clock()
    move_counter = 0

    while True:
        move_counter += 1

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            break

        if move_counter > 0:
            move_counter = 0

            state_old = agent.get_state()
            final_move = agent.get_action(state_old)

            reward, done, score = component.train(snake, food, final_move, 'train')

            state_new = agent.get_state()
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)

            if done:
                reset_game(snake, component, food)
                agent.n_games += 1
                agent.train_long_memory()
                if score > record:
                    record = score
                    agent.model.save()

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

        clock.tick(60)


def ia():
    component = Components()
    snake = Snake()
    food = Food(snake)
    agent = Agent(snake, food)
    clock = pygame.time.Clock()
    move_counter = 0

    while True:
        move_counter += 1

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            break

        if move_counter > snake.get_snake_speed():
            move_counter = 0

            state_old = agent.get_state()
            final_move = agent.get_action(state_old)

            _, done, _ = component.train(snake, food, final_move)

            if done:
                break

        clock.tick(60)


def monte_carlo():
    component = Components()
    snake = Snake()
    food = Food(snake)
    monte_carlo_agent = MonteCarlo(component, snake, food)
    clock = pygame.time.Clock()
    move_counter = 0

    while Screen().get_state():
        move_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Screen.end_game()
                return

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            break

        if move_counter > 0:
            move_counter = 0

            monte_carlo_agent.agente()

            component.monte_carlo(snake, food)

        clock.tick(60)


class Game:
    _INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Game, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    @staticmethod
    def game_loop(mode):
        if mode == 'manual':
            manual_game()
        elif mode == 'ia':
            ia()
        elif mode == 'monteCarlo':
            monte_carlo()
        else:
            train()
