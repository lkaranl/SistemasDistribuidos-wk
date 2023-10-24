import socket
import threading
import json
import random

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

WINDOW_SIZE = (600, 600)

# Lista para armazenar as snakes de todos os jogadores
snakes = []

PIXEL_SIZE = 10  # Defina PIXEL_SIZE conforme necessário

# Inicialize a direção das snakes e a posição da "bolinha"
snake_directions = []
apple_pos = (random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE) * PIXEL_SIZE,
             random.randint(0, WINDOW_SIZE[1] // PIXEL_SIZE) * PIXEL_SIZE)


def handle_client(client_socket, snake_id):
    global snakes, snake_directions, apple_pos, new_head_pos
    while True:
        try:
            # Receba mensagens do cliente e atualize o estado do jogo
            msg = client_socket.recv(4096)
            if not msg:
                break  # Cliente desconectado
            direction = json.loads(msg)['direction']
            # Atualize a direção da snake
            snake_directions[snake_id] = direction
            # Identifique a snake que precisa ser atualizada
            snake = snakes[snake_id]
            # Atualize a posição da cabeça da snake com base na direção
            head_pos = snake[0]
            current_direction = snake_directions[snake_id]
            if current_direction == K_UP:
                new_head_pos = (head_pos[0], head_pos[1] - PIXEL_SIZE)
            elif current_direction == K_DOWN:
                new_head_pos = (head_pos[0], head_pos[1] + PIXEL_SIZE)
            elif current_direction == K_LEFT:
                new_head_pos = (head_pos[0] - PIXEL_SIZE, head_pos[1])
            elif current_direction == K_RIGHT:
                new_head_pos = (head_pos[0] + PIXEL_SIZE, head_pos[1])
            # Insira a nova posição da cabeça no início da lista de posições da snake
            snake.insert(0, new_head_pos)
            # Verifique se a snake pegou a "bolinha"
            if new_head_pos == apple_pos:
                # Gere uma nova posição para a "bolinha"
                apple_pos = (random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE) * PIXEL_SIZE,
                             random.randint(0, WINDOW_SIZE[1] // PIXEL_SIZE) * PIXEL_SIZE)
            else:
                # Remova a última posição da lista de posições da snake para manter o mesmo tamanho
                snake.pop()
            # Atualize a snake na lista de snakes
            snakes[snake_id] = snake
            # Envie o estado atualizado do jogo para o cliente
            game_state = json.dumps({'snakes': snakes, 'apple_pos': apple_pos})
            client_socket.sendall(bytes(game_state, 'utf-8'))
        except Exception as e:
            print(f"Erro: {e}")
            break
    client_socket.close()


def server_thread():
    global snakes, snake_directions  # Adicione snake_directions aqui
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 7777))
    server.listen(5)
    print("Servidor iniciado.")
    while True:
        client_socket, addr = server.accept()
        print(f"Conexão de {addr}")
        # Crie uma nova snake para este jogador
        snake_id = len(snakes)
        snakes.append([(250, 50), (260, 50), (270, 50)])
        snake_directions.append(K_LEFT)  # Defina uma direção inicial para a nova snake
        # Envie o id da snake para o cliente
        client_socket.sendall(bytes(str(snake_id), 'utf-8'))
        client_handler = threading.Thread(target=handle_client, args=(client_socket, snake_id))
        client_handler.start()


# Inicie o servidor em uma nova thread
server_thread = threading.Thread(target=server_thread)
server_thread.start()
