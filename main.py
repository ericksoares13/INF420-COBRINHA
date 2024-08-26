import pygame
import cv2
import numpy as np

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

    draw_text(label, pygame.font.Font(None, 70), (0, 0, 0), screen, x + width // 2, y + height // 2)

    return False

def load_and_blur_video(video_path):
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

    # Converte o frame para RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Redimensiona o frame para caber na tela do Pygame
    frame = cv2.resize(frame, (780, 780))

    # Aplica o desfoque (GaussianBlur)
    frame = cv2.GaussianBlur(frame, (15, 15), 0)

    # Converte o frame para o formato Pygame
    frame = np.rot90(frame)  # Rotaciona a imagem para se alinhar ao formato do Pygame
    frame = pygame.surfarray.make_surface(frame)

    return frame


def main_menu():

    video_path = "menu/video_menu.mp4"
    cap = load_and_blur_video(video_path)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if cap:
            background = process_frame(cap)
            screen.blit(background, (0, 0))

        if draw_button("Manual", 190, 235, 400, 60,
                       pygame.Color("green"), pygame.Color("purple"), lambda: Game.game_loop("manual")):
            screen.fill((255, 255, 255))

        if draw_button("Deep Q-Learning", 190, 335, 400, 60,
                       pygame.Color("green"), pygame.Color("purple"), lambda: Game.game_loop("ia")):
            screen.fill((255, 255, 255))

        if draw_button("Monte Carlo", 190, 435, 400, 60,
                       pygame.Color("green"), pygame.Color("purple"), lambda: Game.game_loop("monteCarlo")):
            screen.fill((255, 255, 255))

        if draw_button("Training", 190, 535, 400, 60,
                       pygame.Color("green"), pygame.Color("purple"), lambda: Game.game_loop("train")):
            screen.fill((255, 255, 255))

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            return

        pygame.display.flip()
        clock.tick(60)


main_menu()
