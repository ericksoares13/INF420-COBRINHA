import pygame
import cv2
import numpy as np

from snake.Game import Game
from snake.components.Screen import Screen

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((780, 780))
pygame.display.set_caption("Snake")

font_path = "font/PressStart2P-Regular.ttf"
game_font = pygame.font.Font(font_path, 25)
title_font = pygame.font.Font(font_path, 40)


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
            return action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    draw_text(label, game_font, (0, 0, 0), screen, x + width // 2, y + height // 2)
    return False


def draw_centered_text(text, font, color, screen, screen_width,  screen_height, y_offset):
    # Renderize o texto
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 + y_offset))

    # Desenhe o texto na tela
    screen.blit(text_surface, text_rect)


def load_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro ao carregar o vídeo.")
        return None

    return cap


def process_frame(cap):
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = cv2.resize(frame, (780, 780))

    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    return frame


def apply_blur(surface, radius):
    if radius < 1:
        return surface

    scale = 1.0 / radius
    surf_size = surface.get_size()
    scaled_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))

    small_surface = pygame.transform.smoothscale(surface, scaled_size)
    blurred_surface = pygame.transform.smoothscale(small_surface, surf_size)

    return blurred_surface


def game_over_display(score_iterations, mode):
    if score_iterations is False:
        return

    while True:
        screen.blit(apply_blur(Screen().get_game_over_screen(), 8), (0, 0))

        square_width, square_height = 450, 400
        square_x = (screen.get_width() - square_width) // 2 + 3
        square_y = (screen.get_height() - square_height) // 2

        shadow_offset = 0.5
        shadow_rect = (square_x - shadow_offset, square_y - shadow_offset, square_width + (4 * shadow_offset), square_height + (4 * shadow_offset))
        border_radius = 20

        light_blue = pygame.Color(173, 216, 230)
        navy_blue = pygame.Color("#afa9d2")

        pygame.draw.rect(screen, (100, 100, 100), shadow_rect,border_radius=border_radius)
        pygame.draw.rect(screen, light_blue, (square_x, square_y, square_width, square_height),border_radius=border_radius)

        if score_iterations[0] + 1 == ((Screen.get_screen_width() // Screen.get_pixel_size()) - 1) ** 2:
            draw_text("You Won", title_font, "#00009C", screen, screen.get_width() // 2 + 2, square_y + 50)
        else:
            draw_text("Game Over", title_font, "#00009C", screen, screen.get_width() // 2 + 6, square_y + 50)

        draw_centered_text(f"Movimento:{score_iterations[1]}", game_font, (0, 0, 0), screen, screen.get_width() + 4, square_y + 520, -50)
        draw_centered_text(f"Pontuação:{score_iterations[0]}", game_font, (0, 0, 0), screen, screen.get_width() + 4, square_y + 420, 50)

        if draw_button("Voltar ao Menu", 188, 410, 413, 60,
                       navy_blue, (255, 255, 255), main_menu):
            break

        aux = draw_button("Jogar Novamente", 188, 500, 413, 60, navy_blue, (255, 255, 255),
                          lambda: Game.game_loop(mode))

        if aux is not False:
            score_iterations = aux

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(15)


def main_menu():
    video_path = "menu/menu_video.mp4"
    cap = load_video(video_path)

    while True:
        if cap:
            background = process_frame(cap)
            screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_text("JOGO DA COBRINHA", title_font, (0, 0, 0), screen, 390, 108)

        light_blue = pygame.Color(173, 216, 230)
        navy_blue = pygame.Color("#afa9d2")

        game_over_display(draw_button("Manual", 182, 227, 416, 60, navy_blue, light_blue,
                                      lambda: Game.game_loop("manual")), "manual")

        game_over_display(draw_button("Deep Q-Learning", 182, 332, 416, 60, navy_blue, light_blue,
                                      lambda: Game.game_loop("ia")), "ia")

        game_over_display(draw_button("Monte Carlo", 182, 436, 416, 60, navy_blue, light_blue,
                                      lambda: Game.game_loop("monteCarlo")), "monteCarlo")

        draw_button("Training", 182, 540, 416, 60, navy_blue, light_blue,
                    lambda: Game.game_loop("train"))

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            return

        pygame.display.flip()
        clock.tick(60)


main_menu()
