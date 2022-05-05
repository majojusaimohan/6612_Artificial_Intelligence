import sys
import pygame
import time
import config
import queue
import threading
from tkinter import *
from tkinter import ttk
from pygame.locals import *

# Local defined modules
from grid import Grid
from search import Search
from window import *

gridQ = queue.Queue()

config.init()

# Starting instance to display tkinter window 
opt = GridOptions()
opt.mainloop()

# to capture inputs of the user
Grid_size = opt.shared_data["Grid_size"].get()
Start_row = opt.shared_data["Start_row"].get()
s_c = opt.shared_data["Start_column"].get()
g_r = opt.shared_data["Goal_Row"].get()
g_c = opt.shared_data["Goal_column"].get()
Search_Algorithm = opt.shared_data["Search_Algorithm"].get()

row = (0, 0)
col = (0, 0)

# default size of small medium and lagre grid
if Grid_size == "Small":
    row = (200, 10)
    col = (200, 10)
elif Grid_size == "Medium":
    row = (500, 25)
    col = (500, 25)
elif Grid_size == "Large":
    row = (800, 40)
    col = (800, 40)

# grid of search algorithm
myGrid = Grid(row[0], col[0])
myMatrix = Search(gridQ, row[1], col[1], (Start_row, s_c), (g_r, g_c))


# starting the grid
pygame.init()
myGrid.initGrid()

# starting and ending values 
myGrid.fillSquare(Start_row, s_c, config.yellow)
myGrid.fillSquare(g_r, g_c, config.yellow)

# for recording mouse clicks
pos_x = 0
pos_y = 0
getWalls = True
fillCells = False

# for recording mouse clicks
while getWalls:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                getWalls = False
        elif event.type == MOUSEBUTTONDOWN:
            fillCells = True
        elif event.type == MOUSEBUTTONUP:
            fillCells = False

        # displaying walls on the grid
        if fillCells:
            try:
                #coloring the grid 
                pos_x, pos_y = event.pos
                pos_x, pos_y = myGrid.getCell(pos_x, pos_y)
                rec = pygame.Rect(pos_x, pos_y, 20, 20)
                pygame.draw.rect(myGrid.screen, config.fill, rec)
                myMatrix.setCell(pos_y // 20, pos_x // 20, "B")
                pygame.display.update()
            except:
                pass
    pygame.display.flip()

# starting thread for Search algorithm
if Search_Algorithm == "BFS":
    t1 = threading.Thread(target=myMatrix.bfs())
elif Search_Algorithm == "DFS":
    t1 = threading.Thread(target=myMatrix.dfs())
elif Search_Algorithm == "A-Star":
    t1 = threading.Thread(target=myMatrix.a_star())

t1.start()

# coloring the path traced by the algorithm 
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if not gridQ.empty():
        x, y, clr = gridQ.get()

        myGrid.fillSquare(x, y, clr)
        pygame.display.update()



