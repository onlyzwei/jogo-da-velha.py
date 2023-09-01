import pygame.font
from pygame.locals import *
from sys import exit

# Inicialização
pygame.init()
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo da Velha")
clock = pygame.time.Clock()
clock.tick(30)

# Variáveis
clicked = False
line_width = 6
player = 1
markers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
game_over = False
font = pygame.font.Font(None, 36)

# Cores
green = (0, 255, 0)
red = (255, 0, 0)


def draw_winner(winner):
    text = font.render(f"Winner: {winner}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)


def draw_grid():
    background = (255, 255, 200)
    grid = (50, 50, 50)
    screen.fill(background)
    for i in range(1, 3):
        pygame.draw.line(screen, grid, (0, i * 200), (screen_width, i * 200), line_width)
        pygame.draw.line(screen, grid, (i * 200, 0), (i * 200, screen_height), line_width)


def draw_markers():
    for row in range(3):
        for col in range(3):
            x = col * 200 + 100
            y = row * 200 + 100
            marker = markers[row][col]
            if marker == 1:
                draw_x(x, y)
            elif marker == -1:
                draw_circle(x, y)


def draw_x(x, y):
    pygame.draw.line(screen, green, (x - 70, y - 70), (x + 70, y + 70), line_width)
    pygame.draw.line(screen, green, (x - 70, y + 70), (x + 70, y - 70), line_width)


def draw_circle(x, y):
    pygame.draw.circle(screen, red, (x, y), 76, line_width)


def check_winner():
    for line in markers:
        soma = sum(line)
        if soma == 3:
            return "X"
        elif soma == -3:
            return "BOLA"

    for column in range(3):
        soma = markers[0][column] + markers[1][column] + markers[2][column]
        if soma == 3:
            return "X"
        elif soma == -3:
            return "BOLA"

    soma = markers[0][0] + markers[1][1] + markers[2][2]
    if soma == 3:
        return "X"
    elif soma == -3:
        return "BOLA"

    soma = markers[0][2] + markers[1][1] + markers[2][0]
    if soma == 3:
        return "X"
    elif soma == -3:
        return "BOLA"

    return None


def resetgame():
    global player, game_over
    screen.fill((255, 255, 255))
    draw_grid()
    for row in range(3):
        for col in range(3):
            markers[row][col] = 0
    game_over = False
    player = 1


def handle_mouse_click(pos):
    cell_x, cell_y = pos[0] // 200, pos[1] // 200
    if markers[cell_y][cell_x] == 0:
        markers[cell_y][cell_x] = player
        return True
    return False


while True:
    draw_grid()
    draw_markers()
    if not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and not clicked:
                clicked = True
            if event.type == MOUSEBUTTONUP and clicked:
                clicked = False
                mouse_pos = pygame.mouse.get_pos()
                if handle_mouse_click(mouse_pos):
                    player *= -1
                    winner = check_winner()
                    if winner:
                        print(f"O vencedor é: {winner}")
                        game_over = True
                        break
    else:
        draw_winner(winner)
        reset_text = font.render("Click to Restart", True, (0, 0, 0))
        reset_rect = reset_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(reset_text, reset_rect)
        pygame.display.update()

        for event in pygame.event.get():
            pygame.display.update()
            if event.type == MOUSEBUTTONDOWN and not clicked:
                clicked = True
            if event.type == MOUSEBUTTONUP and clicked:
                clicked = False
                mouse_pos = pygame.mouse.get_pos()
                if reset_rect.collidepoint(mouse_pos):
                    resetgame()
    pygame.display.update()
