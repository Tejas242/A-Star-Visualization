from colorama import init, Fore, Style
import heapq
import random
import time

# Initialize colorama for colored output
init(autoreset=True)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(grid, node):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            x = node.x + dx
            y = node.y + dy
            if x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0]) and grid[x][y] != '#':
                neighbors.append(Node(x,y))
    return neighbors

def heuristic(node1,node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def reconstruct_path(came_from,current):
    total_path=[current]
    while current in came_from.keys():
        current=came_from[current]
        total_path.insert(0,current)
    return total_path

def a_star(grid,start,end):
    open_set=[start]
    came_from={}
    
    start.g=0
    start.h=heuristic(start,end)
    
    while open_set:
        
        current=heapq.heappop(open_set)
        
        if current.x==end.x and current.y==end.y:
            return reconstruct_path(came_from,current)
        
        for neighbor in get_neighbors(grid,current):
            
            tentative_g_score=current.g+heuristic(current,neighbor)
            
            if neighbor not in came_from.keys() or tentative_g_score<neighbor.g:
                
                came_from[neighbor]=current
                
                neighbor.g=tentative_g_score
                
                neighbor.h=heuristic(neighbor,end)
                
                neighbor.f=neighbor.g+neighbor.h
                
                if neighbor not in open_set:
                    heapq.heappush(open_set,neighbor)
                    
                    
output_count = 1

while True:
	
	# Define a grid
	print("Enter Rows and Colums:")
	ROWS = int(input("ROWS: "))
	COLS = int(input("COLUMNS: "))
	
	start_time = time.time() # Keep track of time
	grid = [[' ' for j in range(COLS)] for i in range(ROWS)]

	# Set random obstacles
	for i in range(ROWS):
		for j in range(COLS):
			if random.random() < 0.3 and (i,j) != (0,0) and (i,j) != (ROWS-1, COLS-1):
				grid[i][j] = '#'

	# Set start and end nodes
	start = Node(0, 0)
	end = Node(ROWS-1, COLS-1)

	# Run A* algorithm
	path = a_star(grid, start, end)

	# Highlight path in the grid
	for node in path:
		grid[node.x][node.y] = '*'

	# Define colors for different symbols
	colors = {'#': Fore.RED, '*': Fore.GREEN, 'S': Fore.YELLOW, 'E': Fore.YELLOW}

	print("\nOUTPUT {}\n".format(output_count))
	
	# Print the grid
	print('+' + '-'*(2*COLS+1) + '+')
	for i in range(ROWS):
		row_str = '| '
		for j in range(COLS):
			char = grid[i][j]
			if (i,j) == (0,0):
				char = 'S'
			elif (i,j) == (ROWS-1, COLS-1):
				char = 'E'
			row_str += f'{colors.get(char, "")}{char} {Style.RESET_ALL}'
		row_str += '|'
		print(row_str)
	print('+' + '-'*(2*COLS+1) + '+')
	
	time_taken = time.time() - start_time # Keep track of time

	print(f'Start: ({start.x}, {start.y})')
	print(f'End: ({end.x}, {end.y})')
	print(f'Obstacle density: {sum(1 for i in range(ROWS) for j in range(COLS) if grid[i][j]=="#") / (ROWS*COLS):.2f}')
	print(f'Path length: {len(path)}')
	print(f'Nodes explored: {len(set(path))}')
	print(f'Total nodes: {ROWS*COLS}')
	print(f'Time Taken: {time_taken}')
	
	print('\n')
	
