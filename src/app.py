import numpy as np
import queue
import time

#Checks if the board is solved
def is_solved(node, board_size):
    for x in range(board_size):
        for y in range(board_size):
            if x == board_size-1 and y == board_size-1:
                if node[x][y] != 0:
                    return False

            elif node[x][y] != x * board_size + y+ 1:
                return False
    return True


#Return position (2d index) of empty
def get_position_of_empty(node, board_size):
    for x in range(board_size):
        for y in range(board_size):
            if node[x][y] == 0:
                return x, y
    #should raise error here
    return -1, -1


def can_move_right(board_size, zero_x, zero_y):
    return zero_y < board_size - 1


def can_move_left(board_size, zero_x, zero_y):
    return zero_y > 0


def can_move_up(board_size, zero_x, zero_y):
    return zero_x > 0


def can_move_down(board_size, zero_x, zero_y):
    return zero_x < board_size - 1


def generate_node_right(node, zero_x, zero_y):
    next_node = np.copy(node)
    temp = next_node[zero_x][zero_y + 1]
    next_node[zero_x][zero_y + 1] = 0
    next_node[zero_x][zero_y] = temp
    return next_node


def generate_node_left(node, zero_x, zero_y):
    next_node = np.copy(node)
    temp = next_node[zero_x][zero_y - 1]
    next_node[zero_x][zero_y - 1] = 0
    next_node[zero_x][zero_y] = temp
    return next_node


def generate_node_up(node, zero_x, zero_y):
    next_node = np.copy(node)
    temp = next_node[zero_x - 1][zero_y]
    next_node[zero_x - 1][zero_y] = 0
    next_node[zero_x][zero_y] = temp
    return next_node


def generate_node_down(node, zero_x, zero_y):
    next_node = np.copy(node)
    temp = next_node[zero_x + 1][zero_y]
    next_node[zero_x + 1][zero_y] = 0
    next_node[zero_x][zero_y] = temp
    return next_node


#Generate new boards and infromation about move from current board
def get_next_nodes(node, board_size, order):
    zero_x, zero_y = get_position_of_empty(node, board_size)
    next_nodes = []

    for direction in order:
        if direction == 'L' and can_move_left(board_size, zero_x, zero_y):
            next_nodes.append((generate_node_left(node, zero_x, zero_y), 'L'))
        if direction == 'R' and can_move_right(board_size, zero_x, zero_y):
            next_nodes.append((generate_node_right(node, zero_x, zero_y), 'R'))
        if direction == 'U' and can_move_up(board_size, zero_x, zero_y):
            next_nodes.append((generate_node_up(node, zero_x, zero_y), 'U'))
        if direction == 'D' and can_move_down(board_size, zero_x, zero_y):
            next_nodes.append((generate_node_down(node, zero_x, zero_y), 'D'))
    return next_nodes


#Solve 15-puzzle using bfs search strategy. It also utilizes set to keep track of all 
#nodes that we've already visited to avoid duplication of work
def bfs(start_node, board_size, order):
    #Start calculation time
    start_time = time.time_ns()
    
    #Prepare necessary data structures
    q = queue.Queue()
    seen_nodes = set()

    #Put our starting node in queue
    q.put((start_node, 0, ''))
    processed_nodes = 0

    while True:
        #If there are no more elements to explore, we are done, we couldn't find solution
        if q.empty():
            return '', processed_nodes, len(seen_nodes), 0, time.time_ns() - start_time

        current_node, depth, moves = q.get()
        processed_nodes += 1

        #If current node is solutin, return all relevant statistics
        if is_solved(current_node, board_size):
            return moves, processed_nodes, len(seen_nodes), depth, time.time_ns() - start_time

        #Generate all posible nodes from current node
        next_nodes = get_next_nodes(current_node, board_size, order)
        for next_node, move in next_nodes:
            #If we've already seen node like this, do not add it
            #We are using .tobytes() method, as numpy arrays are not hashable by default
            #which is necessary property if we want to use default python set
            if next_node.tobytes() not in seen_nodes:
                q.put((next_node, depth + 1, moves + move))
                seen_nodes.add(next_node.tobytes())


LIMIT_DEPTH = 20


#Solve 15-puzzle using dfs search strategy. We are NOT using set to keep track
#all of nodes that we've visited. But we are using limit_depth to control how deep
#we go with dfs. This way we can backup and explore other nodes
#If we keep both limit and set we could end up with situation where we back off and 
#do not explore some nodes because there were added on the track that we abandoned
def dfs(start_node, board_size, order):
    #Start calculation time
    start_time = time.time_ns()

    #Reverse order as child nodes are added in LIFO fashion
    order = list(reversed(order))

    #Prepare necessary data structures
    stack = []

    #Put our starting node on stack
    stack.append((start_node, 0, ''))
    processed_nodes = 0

    max_processed_depth = 0

    while True:
        #If there are no more elements to explore, we are done, we couldn't find solution
        if len(stack) == 0:
            return '', processed_nodes, processed_nodes, 0, time.time_ns() - start_time

        current_node, depth, moves = stack.pop()
        processed_nodes += 1
        
        #Keep track of the max depth that we've achieved
        #Note: In bfs we do not have to do that as we are exploring all nodes at the same level first
        if depth > max_processed_depth:
            max_processed_depth = depth

        #If current node is solution, return all relevant statistics
        if is_solved(current_node, board_size):
            return moves, processed_nodes, processed_nodes, max_processed_depth, time.time_ns() - start_time
        
        #If we reached max depth, just back off
        if depth >= LIMIT_DEPTH:
            continue

        #Generate all posible nodes from current node
        next_nodes = get_next_nodes(current_node, board_size, order)
        for next_node, move in next_nodes:
            stack.append((next_node, depth + 1, moves + move))
                
#Calculates x,y coordinates where value should be
def get_desired_index(board_size, value):
    if value == 0:
        return board_size - 1, board_size - 1
    else:
        return  (value - 1) // board_size, (value - 1) % board_size,

#Calculates manhattan error. The lower, the closer to the solution we are
def manhattan(current_board, board_size):
    manh_error = 0
    for index_row, row in enumerate(current_board):
        for index_col, elem in enumerate(row):
            target_row, target_col = get_desired_index(board_size, elem)
            manh_error += abs(index_row - target_row) + abs(index_col - target_col)
    return manh_error

#Calculates hamming error. The lower, the closer to the solution we are
def hamming(current_board, board_size):
    hamm_error = 0
    for index_row, row in enumerate(current_board):
        for index_col, elem in enumerate(row):
            target_row, target_col = get_desired_index(board_size, elem)
            if target_row != index_row or target_col != index_col:
                hamm_error += 1
    return hamm_error

#Solve 15-puzzle using astr search strategy. heuristic_fun is any function that can take
#board and board_size and produce the heuristic value which has property 
#the lower the closer to the solution
def astr(start_node, board_size, heuristic_fun):
    #Start calculation time
    start_time = time.time_ns()

    #Prepare necessary data structures
    #Priority queue will always have element with lowest value at top
    #It will hold tuples (heuristic_value, board.tobytes(), board)
    #Second value must be board.tobytes(), so in case the heuristic values are the same
    #priority queue can order them based on bytes 
    #numpy arrays are not comparable itself
    pq = queue.PriorityQueue()
    #Node to path is dictionary which stores node -> shortest path to it
    #Thanks to that if we find shorter path to given node we can update it
    node_to_path = dict()

    #Put or starting board 
    pq.put((heuristic_fun(start_node, board_size), start_node.tobytes(), start_node))
    node_to_path[start_node.tobytes()] = ''
    processed_nodes = 0

    max_processed_depth = 0

    while True:
        #If there are no more elements to explore, we are done, we couldn't find solution
        if pq.empty():
            return '', processed_nodes, len(node_to_path.keys()), 0, time.time_ns() - start_time
        _, _, current_node = pq.get()
        moves = node_to_path[current_node.tobytes()]
        processed_nodes += 1

        #Keep track of the max depth that we've achieved
        depth = len(moves)
        if depth > max_processed_depth:
            max_processed_depth = depth

        #If current node is solution, return all relevant statistics
        if is_solved(current_node, board_size):
            return moves, processed_nodes, len(node_to_path.keys()), max_processed_depth, time.time_ns() - start_time

        #If we reached max depth, just back off
        if depth >= LIMIT_DEPTH:
            continue

        #Generate all posible nodes from current node
        #Order here does not matter, as priority queue will put them in good order
        next_nodes = get_next_nodes(current_node, board_size, 'LUDR')
        for next_node, move in next_nodes:
            #If we have not seen node like this
            #Put it in priority queue and save path to it
            if next_node.tobytes() not in node_to_path:
                pq.put((heuristic_fun(next_node, board_size), next_node.tobytes(), next_node))
                node_to_path[next_node.tobytes()] = moves + move
            #If we have seen node like this check 
            #if we have found shorter path to it
            #if so, update the shortest path 
            else:
                current_path_to_next_node = node_to_path[next_node.tobytes()]
                if len(moves) + 1 < len(current_path_to_next_node):
                    node_to_path[next_node.tobytes()] = moves + move


def save_solution_to_file(solution, file_name):
    with open(file_name, 'w') as f:
        f.write(str(len(solution)) + '\n')
        f.write(solution)

def save_additional_info_to_file(solution_len, processed_nodes, seen_nodes, max_depth, time, file_name):
    with open(file_name, 'w') as f:
        f.write(str(solution_len) + '\n')
        f.write(str(processed_nodes) + '\n')
        f.write(str(seen_nodes) + '\n')
        f.write(str(max_depth) + '\n')
        time_ms = "{:.3f}".format(time / 1_000_000)
        f.write(time_ms + '\n')

def read_board_from_file(file_name):
    with open(file_name, 'r') as f:
        height, width = f.readline().split(' ')
        board = np.zeros(shape=(int(height),int(width)))
        for i in range(int(height)):
            row = f.readline().split(' ')
            for j in range(int(width)):
                board[i][j] = int(row[j])
        return board


from argParser import ArgParser

if __name__ == '__main__':
    args = ArgParser.parse_args()
    board = read_board_from_file(args.source_file)

    if args.algorithm == 'bfs':
        solution, processed, seen, max_depth, time = bfs(board, 4, args.order)
        save_solution_to_file(solution, args.solution_file)
        save_additional_info_to_file(len(solution), processed, seen, max_depth, time, args.statistic_file)

    if args.algorithm == 'dfs':
        solution, processed, seen, max_depth, time = dfs(board, 4, args.order)
        save_solution_to_file(solution, args.solution_file)
        save_additional_info_to_file(len(solution), processed, seen, max_depth, time, args.statistic_file)

    if args.algorithm == 'astr':
        heur_fun = manhattan
        if args.order == 'hamm':
            heur_fun = hamming

        solution, processed, seen, max_depth, time = astr(board, 4, heur_fun)
        save_solution_to_file(solution, args.solution_file)
        save_additional_info_to_file(len(solution), processed, seen, max_depth, time, args.statistic_file)
