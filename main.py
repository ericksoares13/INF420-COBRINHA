import pygame
import cv2
import numpy as np
import math

from snake.Game import Game
from snake.components.Screen import Screen

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((780, 780))
pygame.display.set_caption("Snake")

font_path = "font/PressStart2P-Regular.ttf"
game_font = pygame.font.Font(font_path, 25)
title_font = pygame.font.Font(font_path, 40)
developer_font = pygame.font.Font(font_path, 8)
help_font = pygame.font.Font(font_path, 22)
rules_font = pygame.font.Font(font_path, 16)

menu_state = 'main'
selected_mode = None
mouse_clicked = False


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_button(label, x, y, width, height, active_color, inactive_color, action=None):
    global mouse_clicked
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and not mouse_clicked:
            mouse_clicked = True
            if action:
                return action()
            else:
                return True
        elif click[0] == 0:
            mouse_clicked = False
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


def game_over_display(score_iterations, mode, level):
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
                       navy_blue, (255, 255, 255)):
            break

        aux = draw_button("Jogar Novamente", 188, 500, 413, 60, navy_blue, (255, 255, 255),
                          lambda: Game.game_loop(mode, level))

        if aux is not False:
            score_iterations = aux

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(15)

def draw_help_icon(x, y, radius, color, font, text, text_color):
    pygame.draw.circle(screen, color, (x, y), radius)
    draw_text(text, font, text_color, screen, x, y)


def help_icon_clicked(x, y, radius):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    dist = math.sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2)

    if dist < radius and click[0] == 1:
        return True

    return False


def draw_text_wrapped_left(text, font, color, surface, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        test_width, _ = font.size(test_line)

        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    for i, line in enumerate(lines):
        line_surface = font.render(line.strip(), True, color)
        line_rect = line_surface.get_rect(topleft=(x, y + i * font.get_linesize()))
        surface.blit(line_surface, line_rect)


def draw_background():
    w = screen.get_width()
    h = screen.get_height()
    b = Screen.get_pixel_size() // 2

    background_surface = pygame.Surface((w, h))

    background_surface.fill("white")

    for x in range(b, w, b * 2):
        pygame.draw.line(background_surface, (230, 230, 230), (x, 0), (x, h))
    for y in range(b, h, b * 2):
        pygame.draw.line(background_surface, (230, 230, 230), (0, y), (w, y))

    pygame.draw.rect(background_surface, "black", pygame.Rect(0, 0, w, b))
    pygame.draw.rect(background_surface, "black", pygame.Rect(0, 0, b, h))
    pygame.draw.rect(background_surface, "black", pygame.Rect(0, h - b, w, b))
    pygame.draw.rect(background_surface, "black", pygame.Rect(w - b, 0, b, h))

    return background_surface


def apply_blur_rules(surface):
    array = pygame.surfarray.array3d(surface)
    array = cv2.GaussianBlur(array, (15, 15), 0)
    return pygame.surfarray.make_surface(array)


def show_game_rules():
    while True:
        pygame.event.get()
        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            break

        background = draw_background()
        blurred_background = apply_blur_rules(background)

        screen.blit(blurred_background, (0, 0))

        draw_text("REGRAS DO JOGO", title_font, (0, 0, 0), screen, 390, 108)

        square_width, square_height = 570, 510
        square_x = (screen.get_width() - square_width) // 2 + 3
        square_y = (screen.get_height() - square_height) // 2 + 25

        shadow_offset = 0.5
        shadow_rect = (square_x - shadow_offset, square_y - shadow_offset, square_width + (4 * shadow_offset), square_height + (4 * shadow_offset))
        border_radius = 20

        light_blue = pygame.Color(173, 216, 230)
        navy_blue = pygame.Color("#afa9d2")

        pygame.draw.rect(screen, (100, 100, 100), shadow_rect, border_radius=border_radius)
        pygame.draw.rect(screen, light_blue, (square_x, square_y, square_width, square_height),
                         border_radius=border_radius)

        numbers = [
            "1. ",
            "2. ",
            "3. ",
            "4. ",
            "5. "
        ]

        rules = [
            "Use as setas do teclado para mover a cobrinha.",
            "Coma a comida para crescer, ganhar pontos e velocidade.",
            "Evite bater nas paredes ou no próprio corpo, senão, o jogo termina.",
            "A cada comida alcançada, a cabeça da cobra trocará de lugar com a ponta de sua cauda.",
            "Aperte a tecla 'q' para encerrar uma partida ou voltar ao menu."
        ]

        y_offset = 190
        y_offset_number = 197

        spacings = [0, 50, 100, 160, 240]
        spacing_number = [0, 70, 140, 220, 320]

        # Desenhando cada regra com o espaçamento ajustado
        for i, (number, rule) in enumerate(zip(numbers, rules)):
            draw_text(number, rules_font, (0, 0, 0), screen, 155, y_offset_number + spacing_number[i])
            draw_text_wrapped_left(rule, rules_font, (0, 0, 0), screen, 180, y_offset + spacings[i], 490)
            y_offset += 20

        if draw_button("Voltar ao Menu", 182, 585, 416, 60, navy_blue, (255, 255, 255)):
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(60)


def draw_developers_name(screen, font, color, x, y):
    developers_text = "Developed by: Erick Soares, Júlio Henrique"
    draw_text(developers_text, font, color, screen, x, y)


def main_menu():
    global menu_state, selected_mode
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

        pygame.event.get()
        key = pygame.key.get_pressed()

        if key[pygame.K_q]:
            menu_state = 'main'

        draw_text("JOGO DA COBRINHA", title_font, (0, 0, 0), screen, 390, 108)

        light_blue = pygame.Color(173, 216, 230)
        navy_blue = pygame.Color("#afa9d2")

        if menu_state == 'main':
            if draw_button("Manual", 182, 227, 416, 60, navy_blue, light_blue, lambda: select_mode('manual')):
                menu_state = 'difficulty'
            if draw_button("Deep Q-Learning", 182, 332, 416, 60, navy_blue, light_blue, lambda: select_mode('ia')):
                menu_state = 'difficulty'
            if draw_button("Monte Carlo", 182, 436, 416, 60, navy_blue, light_blue, lambda: select_mode('monteCarlo')):
                menu_state = 'difficulty'
            if draw_button("Training", 182, 540, 416, 60, navy_blue, light_blue, lambda: select_mode('train')):
                menu_state = 'difficulty'
        elif menu_state == 'difficulty':
            if draw_button("Fácil", 182, 227, 416, 60, navy_blue, light_blue,
                           lambda: start_game(selected_mode, 'easy')):
                menu_state = 'main'
            if draw_button("Médio", 182, 332, 416, 60, navy_blue, light_blue,
                           lambda: start_game(selected_mode, 'medium')):
                menu_state = 'main'
            if draw_button("Difícil", 182, 436, 416, 60, navy_blue, light_blue,
                           lambda: start_game(selected_mode, 'hard')):
                menu_state = 'main'
            if draw_button("Extremo", 182, 540, 416, 60, navy_blue, light_blue,
                           lambda: start_game(selected_mode, 'extreme')):
                menu_state = 'main'

        help_x = 728
        help_y = 728
        radius = 20
        draw_help_icon(help_x, help_y, radius, light_blue, help_font, '?', (0, 0, 0))

        if help_icon_clicked(help_x, help_y, radius):
            show_game_rules()

        draw_developers_name(screen, developer_font, (255, 255, 255), 390, 767)

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            return

        pygame.display.flip()
        clock.tick(60)


def select_mode(mode):
    global selected_mode
    selected_mode = mode
    return True


def start_game(mode, difficulty):
    game_over_display(Game.game_loop(mode, difficulty), mode, difficulty)
    return True


main_menu()
