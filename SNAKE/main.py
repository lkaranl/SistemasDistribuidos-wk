import pygame
import socket
import threading
import json
from pygame.locals import *

WINDOW_SIZE = (600, 600)
PIXEL_SIZE = 10

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption('Snake')

snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((255, 255, 255))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.2.96", 7777))

# Receba o id da snake do servidor
snake_id = int(client_socket.recv(4096))

snake_direction = K_LEFT
game_state = {'snakes': []}


def receive_game_state():
    global game_state
    while True:
        # Receba o estado do jogo do servidor
        data = client_socket.recv(4096)
        if not data:
            break  # Servidor desconectado
        game_state = json.loads(data)


# Inicie uma nova thread para receber o estado do jogo
receive_thread = threading.Thread(target=receive_game_state)
receive_thread.start()

while True:
    pygame.time.Clock().tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            client_socket.close()
            exit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                snake_direction = event.key
                # Envie a nova direção ao servidor
                msg = json.dumps({'id': snake_id, 'direction': snake_direction})
                client_socket.sendall(bytes(msg, 'utf-8'))

    # Renderize o estado do jogo
    screen.fill((0, 0, 0))
    for snake_pos in game_state['snakes']:
        for pos in snake_pos:
            screen.blit(snake_surface, pos)
    pygame.display.update()

client_socket.close()
