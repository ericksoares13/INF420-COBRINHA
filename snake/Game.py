import pygame

from neuralNetwork.Agent import Agent
from snake.actors.Food import Food
from snake.actors.Snake import Snake
from snake.components.Components import Components
from snake.components.Screen import Screen

import matplotlib.pyplot as plt


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
    def __process_manual_events():
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            Components.set_key(pygame.K_UP)
        elif key[pygame.K_DOWN]:
            Components.set_key(pygame.K_DOWN)
        elif key[pygame.K_LEFT]:
            Components.set_key(pygame.K_LEFT)
        elif key[pygame.K_RIGHT]:
            Components.set_key(pygame.K_RIGHT)
        elif key[pygame.K_ESCAPE]:
            Components.set_key(pygame.K_ESCAPE)

    @staticmethod
    def __plot(scores, mean_scores, filename='./model/plot.png'):
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

    @staticmethod
    def __reset_game():
        Screen().start_game()
        Snake().start_snake()
        Components().set_key(pygame.K_SPACE)
        Food().randon_position()

    @staticmethod
    def __train():
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        agent = Agent()
        clock = pygame.time.Clock()
        move_counter = 0

        while True:
            move_counter += 1

            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                break

            if move_counter > Snake().get_snake_speed():
                move_counter = 0

                state_old = agent.get_state()
                final_move = agent.get_action(state_old)

                reward, done, score = Components.train(final_move)

                state_new = agent.get_state()
                agent.train_short_memory(state_old, final_move, reward, state_new, done)
                agent.remember(state_old, final_move, reward, state_new, done)

                if done:
                    Game.__reset_game()
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
                    Game.__plot(plot_scores, plot_mean_scores)

            clock.tick(60)

    @staticmethod
    def __manual_game():
        clock = pygame.time.Clock()

        while Screen().get_state():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Screen.end_game()
                    return

            Game().__process_manual_events()

            Components.process()
            Components.update()
            Components.generate()

            clock.tick(60)

    @staticmethod
    def game_loop(mode):
        Game.__reset_game()

        if mode == 'manual':
            Game.__manual_game()
        else:
            Game.__train()
