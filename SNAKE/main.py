#!/bin/python3 env

import pygame

WINDOW_SIZE = (600, 600)
PIXEL_SIZE = 10

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption('Snake')

snake_pos = [(250, 50), (260, 50), (270, 50)]
snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((255, 255, 255))

apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
apple_surface.fill((255, 0, 0))

while True:
    screen.fill(())
    for event in pygame.event.get():
        if event.type == quit:
            pygame.quit()
            quit()
    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    snake_pos[0] = snake_pos[0] [0] + 10, snake_pos[0] [1]

    pygame.display.update()
