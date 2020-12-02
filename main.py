import pygame
import time
import random
import math
import random
import socket

PWM = 255
BUFFER_SIZE = 1024
message = ""
WIDTH = 800
HEIGHT = 800
FPS = 30
grid = []
visited = []
solVisited = []
availableSpaces = {}
solution = []
facingDir = 2

direction = {
    "N": [0, -1],
    "S": [0, 1],
    "E": [1, 0],
    "W": [-1, 0],
}

n = 10
w = WIDTH / n
h = HEIGHT / n

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")
clock = pygame.time.Clock()
white = [255, 255, 255]
black = [0, 0, 0]
screen.fill(white)
pygame.display.update()


def drawGrid(n):
    w = WIDTH / n
    h = HEIGHT / n
    x = 0.0
    y = 0.0
    for i in range(0, n):
        for j in range(0, n):
            pygame.draw.line(screen, black, [x, y], [x + w, y], 2)  # TOP
            pygame.draw.line(screen, black, [x, y], [x, y + h], 2)  # LEFT
            pygame.draw.line(screen, black, [x + w, y], [x + w, y + h], 2)  # RIGHT
            pygame.draw.line(screen, black, [x, y + h], [x + w, y + h], 2)  # BOTTOM
            grid.append([x, y])
            availableSpaces[(x, y)] = []
            x += w
        x = 0.0
        y += h
    print(len(grid))
    pygame.display.update()


def carveMazefrom(x, y, grid):
    if [x, y] in visited or [x, y] not in grid:
        return
    else:
        visited.append([x, y])

    dir_order = ["N", "S", "E", "W"]
    random.shuffle(dir_order)

    for i in range(0, len(dir_order)):
        next_x = x + (direction.get(dir_order[i])[0]) * w
        next_y = y + (direction.get(dir_order[i])[1]) * h

        if [next_x, next_y] not in visited and [next_x, next_y] in grid:
            if dir_order[i] == "N":
                availableSpaces[(x, y)] = availableSpaces.get((x, y)) + ["N"]
                pygame.draw.line(screen, white, [x, y], [x + w, y], 2)
            if dir_order[i] == "S":
                availableSpaces[(x, y)] = availableSpaces.get((x, y)) + ["S"]
                pygame.draw.line(screen, white, [x, y + h], [x + w, y + h], 2)
            if dir_order[i] == "E":
                availableSpaces[(x, y)] = availableSpaces.get((x, y)) + ["E"]
                pygame.draw.line(screen, white, [x + w, y], [x + w, y + h], 2)
            if dir_order[i] == "W":
                availableSpaces[(x, y)] = availableSpaces.get((x, y)) + ["W"]
                pygame.draw.line(screen, white, [x, y], [x, y + h], 2)
            pygame.display.update()
            time.sleep(0.05)  # Comment This If You Dont Want To Wait For Maze To Generate
            carveMazefrom(next_x, next_y, grid)


def solveMaze(x, y, aSpaces, grid, currentPath):
    if ((x, y) in currentPath):
        return
    currentPath.append((x, y))

    if (x, y) == (WIDTH - w, HEIGHT - h):
        solution[:] = list(currentPath)
        currentPath.pop()
        return

    for i in range(0, len(aSpaces.get((x, y)))):
        next_x = x + (direction.get(aSpaces.get((x, y))[i])[0]) * w
        next_y = y + (direction.get(aSpaces.get((x, y))[i])[1]) * h
        if aSpaces.get((x, y))[i] == "N":
            solveMaze(next_x, next_y, aSpaces, grid, currentPath)
        if aSpaces.get((x, y))[i] == "S":
            solveMaze(next_x, next_y, aSpaces, grid, currentPath)
        if aSpaces.get((x, y))[i] == "E":
            solveMaze(next_x, next_y, aSpaces, grid, currentPath)
        if aSpaces.get((x, y))[i] == "W":
            solveMaze(next_x, next_y, aSpaces, grid, currentPath)
    currentPath.pop()
    return


drawGrid(n)
carveMazefrom(0, 0, grid)
solveMaze(0, 0, availableSpaces, grid, [])
for i in solution:
    pygame.draw.circle(screen, [255,0,0],[ int(i[0]+(w/2)) , int(i[1]+(h/2))],10)
    #print(i[0],i[1])
    pygame.display.update()
    time.sleep(0.05)  # Comment This If You Dont Want To Wait For Solution To Generate

# Write your code here or make a new python file and run the code from here
#movement methods

#2,4,6,8 for south,west, east, north
#assume that the object is initially facing south

def compLocX(loc1, loc2):
    dir = 0
    if (loc1 < loc2):
        dir = 6
    elif (loc1 > loc2):
        dir = 4
    else:
        dir = 0
    #print(dir)
    return dir

def compLocY(loc1, loc2):
    dir = 0
    if (loc1 < loc2):
        dir = 2
    elif (loc1 > loc2):
        dir = 8
    else:
        dir = 0
    #print(dir)
    return dir

def step(arr):

      #for x in arr:
          #print(x)

      tcpCommand = []
      currFaceDir = 2
      dir = 0
      for i, j in zip(arr[:-1], arr[1:]):
         dirX = compLocX(i[0], j[0])
         dirY = compLocY(i[1],j[1])
         if (dirX == 6) or (dirX == 4):
             dir = compLocX(i[0], j[0])
         if (dirY == 8) or (dirY == 2):
             dir = compLocY(i[1],j[1])

         if(dir == 2):
             if (currFaceDir == 2):
                 command = "[255][0][255][0]"
                 faceDir = 2
             elif (currFaceDir == 4):
                 command = "([255][0][0][255],[255][0][255][0])"
                 faceDir = 2
             elif (currFaceDir == 6):
                 command = "([0][255][255][0],[255][0][255][0])"
                 faceDir = 2
             elif (currFaceDir == 8):
                 command = "[0][255][0][255]"
                 faceDir = 8
             tcpCommand.append(command)

         elif (dir == 4):
             if (currFaceDir == 4):
                 command = "[255][0][255][0]"
                 faceDir = 4
             elif (currFaceDir == 8):
                 command = "([255][0][0][255],[255][0][255][0])"
                 faceDir = 4
             elif (currFaceDir == 2):
                 command = "([0][255][255][0],[255][0][255][0])"
                 faceDir = 4
             elif (currFaceDir == 6):
                 command = "[0][255][0][255]"
                 faceDir = 6
             tcpCommand.append(command)

         elif (dir == 6):
             if (currFaceDir == 6):
                 command = "[255][0][255][0]"
                 faceDir = 6
             elif (currFaceDir == 2):
                 command = "([255][0][0][255],[255][0][255][0])"
                 faceDir = 6
             elif (currFaceDir == 8):
                 command = "([0][255][255][0],[255][0][255][0])"
                 faceDir = 6
             elif (currFaceDir == 4):
                 command = "[0][255][0][255]"
                 faceDir = 4
             tcpCommand.append(command)

         elif (dir == 8):
             if (currFaceDir == 8):
                 command = "[255][0][255][0]"
                 faceDir = 8
             elif (currFaceDir == 6):
                 command = "([255][0][0][255],[255][0][255][0])"
                 faceDir = 8
             elif (currFaceDir == 4):
                 command = "([0][255][255][0],[255][0][255][0])"
                 faceDir = 8
             elif (currFaceDir == 2):
                 command = "[0][255][0][255]"
                 faceDir = 2
             tcpCommand.append(command)
         currFaceDir = faceDir
         #tcpCommand.append(command)
      #print(stepX, stepY)
      stop = "[0][0][0][0]"
      tcpCommand.append(stop)
      return tcpCommand

mazeSolution = step(solution) #commands to solve the maze
print(mazeSolution)


#socket code
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
while True:
    msg = s.recv(1000000)
    if len(msg) <= 0:
        break
    message = '\n'.join(mazeSolution) +   msg.decode("utf-8")
print(message)
# The array that contains the solution is called solution[], use this for the TCP Stream.


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False