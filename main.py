#imports
import pygame
import random
import time


#constants
WIDTH = 800
HEIGHT = 800
FPS = 30
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
LBLUE = [51, 201, 255]
LLBLUE = [218, 247, 166]
RED = [255, 0, 0]

global n, num

#maze variables
#print("Enter a value for n: ")
global n
num = ""
clock = pygame.time.Clock()

#gridSize = WIDTH/n
x = 0
y = 0
#gridSize = WIDTH/n
grid = []
visited = []
stack = []
solution = {}

#draws the grid
def draw_grid(screen, x, y, gridSize):
    for i in range(n):
        x = 0
        for j in range(n):
            pygame.draw.line(screen, BLACK, [x, y], [x+gridSize, y]) #top of cell
            pygame.draw.line(screen, BLACK, [x+gridSize, y], [x+gridSize, y+gridSize]) # right of cell
            pygame.draw.line(screen, BLACK, [x, y], [x, y+gridSize])  # left of cell
            pygame.draw.line(screen, BLACK, [x, y+gridSize], [x + gridSize, y + gridSize])  # bottom of cell
            grid.append((x, y))
            x = x+gridSize
        y = y + gridSize

def push_up(screen, x, y, gridSize):
    pygame.draw.rect(screen, LLBLUE, (x + 1, y - gridSize + 1, gridSize-1, 2*gridSize-1), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(screen, x, y, gridSize):
    pygame.draw.rect(screen, LLBLUE, (x + 1, y + 1, gridSize - 1, 2*gridSize - 1), 0)
    pygame.display.update()


def push_left(screen, x, y, gridSize):
    pygame.draw.rect(screen, LLBLUE, (x - gridSize +1, y +1, 2*gridSize -1, gridSize - 1), 0)
    pygame.display.update()


def push_right(screen, x, y, gridSize):
    pygame.draw.rect(screen, LLBLUE, (x +1, y +1, 2*gridSize -1, gridSize - 1), 0)
    pygame.display.update()


def single_cell(screen, x, y, gridSize):
    pygame.draw.rect(screen, LBLUE, (x +1, y +1, gridSize - 2, gridSize - 2), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(screen, x, y, gridSize):
    pygame.draw.rect(screen, LLBLUE, (x +1, y +1, gridSize - 2, gridSize - 2), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell


def solution_cell(screen, x, y):
    pygame.draw.rect(screen, RED, (x+8, y+8, 5, 5), 0)             # used to show the solution
    pygame.display.update()                                        # has visited cell

#creates the maze out of the given grid
def carve_maze(screen,x, y, gridSize):
    single_cell(screen, x, y, gridSize)
    stack.append((x, y))
    visited.append((x, y))
    while len(stack) > 0:
        time.sleep(0.07)
        cell = []
        if (x + gridSize, y) not in visited and (x + gridSize, y) in grid:
            cell.append("right")
        if (x - gridSize, y) not in visited and (x - gridSize, y) in grid:
            cell.append("left")
        if (x, y + gridSize) not in visited and (x, y + gridSize) in grid:
            cell.append("down")
        if (x, y - gridSize) not in visited and (x, y - gridSize) in grid:
            cell.append("up")

        if len(cell) > 0:
            cell_chosen = (random.choice(cell))

            if cell_chosen == "right":
                push_right(screen, x, y, gridSize)
                solution[(x+gridSize, y)] = x,y
                x = x + gridSize
                visited.append((x,y))
                stack.append((x,y))

            elif cell_chosen == "left":
                push_left(screen, x, y, gridSize)
                solution[(x-gridSize , y)] = x, y
                x = x - gridSize
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(screen, x, y, gridSize)
                solution[(x, y + gridSize)] = x, y
                y = y + gridSize
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(screen, x, y, gridSize)
                solution[(x, y - gridSize)] = x, y
                y = y - gridSize
                visited.append((x, y))
                stack.append((x, y))

        else:
            x,y = stack.pop()
            single_cell(screen, x, y, gridSize)
            time.sleep(0.05)
            backtracking_cell(screen, x, y, gridSize)

# def plot_route_back(screen,x,y, gridSize):
#     solution_cell(screen, x, y)                                          # solution list contains all the coordinates to route back to start
#     while (x, y) != (gridSize,gridSize):                                     # loop until cell position == start position
#         x, y = solution[x, y]                                    # "key value" now becomes the new key
#         solution_cell(screen,x, y)                                      # animate route back
#         time.sleep(.1)

def dispCover(screen):
    num = ""
    n = 1
    started = False
    while not started:
        titlescreen = pygame.image.load("titlepage.png")
        screen.blit(titlescreen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key >= 48 and event.key <= 57 and len(num) < 10:
                    num = num + chr(event.key)  # Adds another character to the name
                if event.key == pygame.K_BACKSPACE:  # Removes the last character in the name
                    num = num[:-1]
                if event.key == pygame.K_RETURN:
                    started = True
                    n = int(num)
        pygame.display.update()


def game_loop(screen):
    running = True
    while running:
        # keep running at the right speed
        clock.tick(FPS)
        # process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


def dispTitle(screen):
    titlescreen = pygame.image.load("titlepage.png")
    screen.blit(titlescreen, (0, 0))

if __name__=="__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid")
    titlescreen = pygame.image.load("titlepage.png")
    screen.blit(titlescreen, (0, 0))


    started = False
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key >= 48 and event.key <= 57 and len(num) < 10:
                    num = num + chr(event.key)  # Adds another character to the name
                if event.key == pygame.K_BACKSPACE:  # Removes the last character in the name
                    num = num[:-1]
                if event.key == pygame.K_RETURN:
                    if num == "":  # If it's blank set it to Player1
                        num = "1"
                    started = True
                    n = int(num)
        pygame.display.update()
    #main program
    screen.fill(WHITE)
    x, y = 0, 0
    gridSize = WIDTH / n

    draw_grid(screen, 40, 0, gridSize)
    carve_maze(screen, x, y, gridSize)
    game_loop(screen)

