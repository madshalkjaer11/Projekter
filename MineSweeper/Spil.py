import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 800
FIELD_WIDTH, FIELD_HEIGHT = 50, 50
START_X, START_Y = 150, 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))

board = []
buttons = []
revealed = [[False for _ in range(10)] for _ in range(10)]
flagged = [[False for _ in range(10)] for _ in range(10)]
antal_miner = 0
antal_sikre_felter = 0
abnåede_sikre_felter = 0
start_tid = time.time()

font = pygame.font.Font(None, 50)
gameover_font = pygame.font.Font(None, 100)
prøv_igen = pygame.Rect(250, 450, 300, 50)

generate_board = True
running = True
gameover = False
won = False
stop_tid = False

def new_game():

    global board, buttons, revealed, flagged
    global antal_miner, start_tid
    global gameover, won, generate_board, stop_tid

    antal_miner = 0
    start_tid = time.time()

    board.clear()
    buttons.clear()

    revealed = [[False for _ in range(10)] for _ in range(10)]
    flagged = [[False for _ in range(10)] for _ in range(10)]

    gameover = False
    won = False
    generate_board = True
    stop_tid = False

def check_win():
    for row in range(10):
        for colomn in range(10):
            if not board[row][colomn] and not revealed[row][colomn]:
                return False
    return True

def reveal(row, column):

    # Uden for brættet
    if not (0 <= row < 10 and 0 <= column < 10):
        return

    # Allerede åbnet
    if revealed[row][column]:
        return

    # Åbn feltet
    revealed[row][column] = True

    # Stop hvis det er en mine
    if board[row][column]:
        return

    # Stop hvis der er nabo-miner
    if count_neighbours(row, column) > 0:
        return

    # Åbn alle naboer
    for i in range(-1, 2):
        for j in range(-1, 2):

            if i == 0 and j == 0:
                continue

            reveal(row + i, column + j)



def count_neighbours(row, colomn):

    bombs = 0

    for i in range(-1, 2):
        for j in range(-1, 2):

            if i == 0 and j == 0:
                continue

            new_row = row + i
            new_colomn = colomn + j 

            if 0 <= new_row < 10 and 0 <= new_colomn < 10:
                if board[new_row][new_colomn]:
                    bombs += 1

    return bombs

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not gameover and not won:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for row in range(10):
                        for colomn in range(10):
                            if flagged[row][colomn] == False:
                                if buttons[row][colomn].collidepoint(event.pos):
                                    reveal(row, colomn)
                                    
                                    if check_win():
                                        won = True

                                    if board[row][colomn]:
                                        gameover = True
                                        stop_tid = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    for row in range(10):
                        for colomn in range(10):
                            if buttons[row][colomn].collidepoint(event.pos):
                                flagged[row][colomn] = not flagged[row][colomn]

        if won or gameover:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if prøv_igen.collidepoint(event.pos):
                        new_game()



    screen.fill((30, 30, 30))

    # Tegn baggrund
    pygame.draw.rect(screen, (180, 180, 180), (150, 150, 500, 500))

    if generate_board:
        for row in range(10):
            board_row = []
            button_row = []

            for colomn in range(10):
                
                mine = random.randint(1, 100) < 13

                board_row.append(mine)

                X = START_X + (colomn * FIELD_WIDTH)
                Y = START_Y + (row * FIELD_HEIGHT)
                button_row.append(pygame.Rect(X, Y, FIELD_WIDTH, FIELD_HEIGHT))

            board.append(board_row)
            buttons.append(button_row)
        generate_board = False

    for row in range(10):
        for colomn in range(10):

            X = START_X + (colomn * FIELD_WIDTH)
            Y = START_Y + (row * FIELD_HEIGHT)
            
            if (row + colomn) % 2 == 0:
                color = (252, 193, 104)
            else:
                color = (219, 172, 99)

            bombs = count_neighbours(row, colomn)

            if bombs == 1:
                number_color = (99, 159, 219)
            elif bombs == 2:
                number_color = (133, 212, 91)
            elif bombs == 3:
                number_color = (242, 135, 102)
            elif bombs == 4:
                number_color = (242, 247, 143)

            if bombs < 1 or board[row][colomn]:
                pygame.draw.rect(screen, color, (X, Y, FIELD_WIDTH, FIELD_HEIGHT))
            else:
                number_of_bombs = font.render(str(bombs), True, (number_color))
                pygame.draw.rect(screen, color, (X, Y, FIELD_WIDTH, FIELD_HEIGHT))
                screen.blit(number_of_bombs, (X + 14, Y + 10))

            if board[row][colomn]:
                pygame.draw.circle(screen, (242, 74, 48), (X + FIELD_WIDTH // 2, Y + FIELD_HEIGHT // 2), FIELD_WIDTH // 3)
            
    for row in range(10):
        for colomn in range(10):

            if (row + colomn) % 2 == 0:
                color = (156, 201, 66)
            else:
                color = (146, 184, 72)

            if not revealed[row][colomn]:
                pygame.draw.rect(screen, color, buttons[row][colomn])

    for row in range(10):
        for colomn in range(10):

            X = START_X + (colomn * FIELD_WIDTH)
            Y = START_Y + (row * FIELD_HEIGHT)
    
            if flagged[row][colomn]:
                pygame.draw.line(screen, (242, 74, 48), (X + 25, Y + 40), (X + 25, Y + 10), 5)
                pygame.draw.polygon(screen, (242, 74, 48), ((X + 22.5, Y + 12.5), (X + 10, Y + 20), (X + 25, Y + 20)))

    if gameover:
        overlay = pygame.Surface((500, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (150, 150))

        tekst = gameover_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(tekst, (200, 350))

        pygame.draw.rect(screen, (180, 180, 180), prøv_igen)
        tekst = font.render("Prøv igen", True, (255, 255, 255))
        screen.blit(tekst, (325, 460))

    if won:
        overlay = pygame.Surface((500, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (150, 150))

        tekst = gameover_font.render("VICTORY", True, (0, 255, 0))
        screen.blit(tekst, (250, 350))

        pygame.draw.rect(screen, (180, 180, 180), prøv_igen)
        tekst = font.render("Nyt spil", True, (255, 255, 255))
        screen.blit(tekst, (325, 460))

    for row in range(10):
        for colomn in range(10):
            if revealed[row][colomn]:
                flagged[row][colomn] = False
    
    if not stop_tid:
        tid = time.time() - start_tid

    tekst = font.render(str(round(tid)), True, (255, 255, 255))
    screen.blit(tekst, (375, 100))



    pygame.display.flip()

pygame.quit()