import pygame

from snake.Game import Game

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((780, 780))
pygame.display.set_caption("Escolha o modo de jogo")


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_button(label, x, y, width, height, active_color, inactive_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    draw_text(label, pygame.font.Font(None, 74), (0, 0, 0), screen, x + width // 2, y + height // 2)

    return False


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))

        if draw_button("Manual", 300, 300, 200, 50,
                       (0, 0, 255), (0, 255, 0), lambda: Game.game_loop("manual")):
            screen.fill((255, 255, 255))

        if draw_button("IA", 300, 400, 200, 50,
                       (0, 0, 255), (0, 255, 0), lambda: Game.game_loop("ia")):
            screen.fill((255, 255, 255))

        if draw_button("Monte Carlo", 300, 500, 200, 50,
                       (0, 0, 255), (0, 255, 0), lambda: Game.game_loop("monteCarlo")):
            screen.fill((255, 255, 255))

        if draw_button("Train", 300, 600, 200, 50,
                       (0, 0, 255), (0, 255, 0), lambda: Game.game_loop("train")):
            screen.fill((255, 255, 255))

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            return

        pygame.display.flip()
        clock.tick(60)


main_menu()
