import pygame
import heapq
import random
import time

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set the dimensions of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Define the size of the grid
ROWS = 50
COLS = 50
CELL_SIZE = SCREEN_HEIGHT // ROWS

# Set random obstacles
obstacle_prob = 0.3
grid = [[' ' for j in range(COLS)] for i in range(ROWS)]
for i in range(ROWS):
    for j in range(COLS):
        if random.random() < obstacle_prob and (i,j) != (0,0) and (i,j) != (ROWS-1, COLS-1):
            grid[i][j] = '#'

# Set start and end nodes
start = (0, 0)
end = (ROWS-1, COLS-1)

# Initialize the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("A* Algorithm")

def get_neighbors(grid, node):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            x = node[0] + dx
            y = node[1] + dy
            if x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0]) and grid[x][y] != '#':
                neighbors.append((x,y))
    return neighbors

def heuristic(node1,node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

def reconstruct_path(came_from,current):
    total_path=[current]
    while current in came_from.keys():
        current=came_from[current]
        total_path.insert(0,current)
    return total_path

def a_star(grid,start,end):
    open_set=[start]
    came_from={}
    g_scores = {start: 0}
    
    while open_set:
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        current = min(open_set, key=lambda x: g_scores[x] + heuristic(x, end))
        if current == end:
            return reconstruct_path(came_from, current)
        
        open_set.remove(current)
        
        for neighbor in get_neighbors(grid,current):
            
            tentative_g_score = g_scores[current] + heuristic(current,neighbor)
            
            if neighbor not in g_scores.keys() or tentative_g_score < g_scores[neighbor]:
                
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    
        # Visualize the search
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == '#':
                    color = BLACK
                elif (i,j) == start:
                    color = YELLOW
                elif (i,j) == end:
                    color = YELLOW
                elif (i,j) in came_from.keys():
                    color = GREEN
                elif (i,j) in open_set:
                    color = RED
                else:
                    color = WHITE
                pygame.draw.rect(screen, color, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
        
    return None

# Run A* algorithm
path = a_star(grid, start, end)

# Visualize final path
if path is not None:
    for node in path:
        grid[node[0]][node[1]] = '*'

while True:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # Draw grid
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] == '#':
                color = BLACK
            elif grid[i][j] == '*':
                color = YELLOW
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.display.update()

