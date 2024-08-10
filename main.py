import pygame

from components.Components import Components
from components.Screen import Screen

pygame.init()
clock = pygame.time.Clock()

while Screen().get_state():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Screen.end_game()

    Components.process()
    Components.update()
    Components.generate()

    clock.tick(60)

pygame.quit()
