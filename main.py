import pygame

from components.Components import Components

pygame.init()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Components.process()
    Components.update()
    Components.generate()

    clock.tick(60)

pygame.quit()
