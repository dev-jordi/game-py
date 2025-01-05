import pygame
import random

# Inicializa o Pygame
pygame.init()

# Define as cores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Dimensões da tela
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define o relógio para controlar a velocidade do jogo
clock = pygame.time.Clock()

# Tamanho dos blocos (cobra e comida)
BLOCK_SIZE = 20
SPEED = 7

# Fonte para o texto
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Carrega o sprite da cobra (use uma imagem sua, ex: snake.png)
snake_sprite = pygame.image.load("player.png").convert_alpha()  # A imagem deve ser 20x20 pixels
snake_sprite = pygame.transform.scale(snake_sprite, (BLOCK_SIZE, BLOCK_SIZE))

# Função para mostrar a pontuação
def show_score(score):
    value = score_font.render("Pontuação: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])
    
# Função para desenhar a cobra com sprites
def draw_snake_with_sprites(snake_body):
    for block in snake_body:
        screen.blit(snake_sprite, (block[0], block[1]))

# Função para mostrar a mensagem de fim de jogo
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH // 3, HEIGHT // 3])

# Função principal do jogo
def game_loop():
    game_over = False
    game_close = False

    # Posições iniciais da cobra
    x = WIDTH // 2
    y = HEIGHT // 2

    # Movimento da cobra (velocidade inicial)
    x_change = 0
    y_change = 0

    # Corpo da cobra
    snake_body = []
    snake_length = 1

    # Posição inicial da comida
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Loop do jogo
    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("You won, Press C to retry or Q", RED)
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x_change == 0:  # Impede a cobra de se mover na direção oposta
                        x_change = -BLOCK_SIZE
                        y_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x_change == 0:
                        x_change = BLOCK_SIZE
                        y_change = 0
                elif event.key == pygame.K_UP:
                    if y_change == 0:
                        y_change = -BLOCK_SIZE
                        x_change = 0
                elif event.key == pygame.K_DOWN:
                    if y_change == 0:
                        y_change = BLOCK_SIZE
                        x_change = 0

        # Verifica se a cobra saiu da tela (bordas)
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        # Atualiza a posição da cobra
        x += x_change
        y += y_change

        # Preenche a tela com preto
        screen.fill(BLACK)

        # Desenha a comida
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Atualiza a cobra
        snake_head = [x, y]
        snake_body.append(snake_head)

        # Verifica se a cobra cresceu
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Verifica se a cobra colidiu consigo mesma
        for block in snake_body[:-1]:
            if block == snake_head:
                game_close = True

        # Desenha a cobra
        draw_snake_with_sprites(snake_body)

        # Mostra a pontuação
        show_score(snake_length - 1)

        # Atualiza a tela
        pygame.display.update()

        # Verifica se a cobra comeu a comida
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        # Controla a velocidade do jogo
        clock.tick(SPEED)

    # Sai do Pygame
    pygame.quit()

# Executa o jogo
if __name__ == "__main__":
    game_loop()