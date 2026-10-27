import heapq
import copy

def find_blank(state):
    """Finds the coordinates (row, col) of the empty slot (0)."""
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_manhattan_distance(state, goal_state):
    """Calculates total Manhattan Distance heuristic relative to the custom goal state."""
    distance = 0
    # Map out where each number is supposed to go based on the user's custom goal
    target_positions = {}
    for r in range(3):
        for c in range(3):
            val = goal_state[r][c]
            if val != 0:
                target_positions[val] = (r, c)
                
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0 and val in target_positions:
                target_r, target_c = target_positions[val]
                distance += abs(r - target_r) + abs(c - target_c)
    return distance

def get_neighbors(state):
    """Generates all possible valid board moves from the current position."""
    neighbors = []
    r, c = find_blank(state)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
    
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = copy.deepcopy(state)
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            neighbors.append(new_state)
            
    return neighbors

def state_to_tuple(state):
    """Converts a 2D grid into an immutable tuple structure so it can be hashed."""
    return tuple(tuple(row) for row in state)

def count_inversions(state):
    """Flattens the grid and counts inversions to check for mathematical solvability."""
    flat_list = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions

def is_solvability_matching(start, goal):
    """
    In the 8-puzzle, a state can reach another state if and only if 
    both states have the same inversion parity (both even or both odd).
    """
    return (count_inversions(start) % 2) == (count_inversions(goal) % 2)

def solve_puzzle(start_state, goal_state):
    """Solves the 8-puzzle layout using the optimal A* search algorithm."""
    if not is_solvability_matching(start_state, goal_state):
        return None # Mathematically impossible configuration
        
    initial_h = get_manhattan_distance(start_state, goal_state)
    priority_queue = [(initial_h, 0, start_state, [])]
    
    visited = set()
    visited.add(state_to_tuple(start_state))
    
    while priority_queue:
        _, cost, current, path = heapq.heappop(priority_queue)
        
        if current == goal_state:
            return path + [current]
            
        for neighbor in get_neighbors(current):
            neighbor_tuple = state_to_tuple(neighbor)
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                h = get_manhattan_distance(neighbor, goal_state)
                f = (cost + 1) + h
                heapq.heappush(priority_queue, (f, cost + 1, neighbor, path + [current]))
                
    return None

def print_board(state):
    """Prints the board layout cleanly in the IDLE console window."""
    for row in state:
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()

def get_user_matrix(matrix_name):
    """Prompts the user to input a 3x3 layout row-by-row with input filtering."""
    print(f"\n--- Enter the {matrix_name} Grid Layout ---")
    print("Enter 3 numbers per row separated by spaces. Use '0' for the blank space.")
    print("Example format row entry: 1 2 3")
    
    matrix = []
    all_numbers = set()
    
    while len(matrix) < 3:
        try:
            row_input = input(f"Enter numbers for Row {len(matrix) + 1}: ").split()
            if len(row_input) != 3:
                print("Error: You must type exactly 3 numbers.")
                continue
                
            row_nums = [int(x) for x in row_input]
            
            # Basic range checking
            if any(num < 0 or num > 8 for num in row_nums):
                print("Error: Numbers must be between 0 and 8.")
                continue
                
            # Duplicate checking
            if any(num in all_numbers for num in row_nums):
                print("Error: Duplicate numbers detected. Every number from 0-8 must appear exactly once.")
                continue
                
            all_numbers.update(row_nums)
            matrix.append(row_nums)
            
        except ValueError:
            print("Error: Invalid characters detected. Please type integers only.")
            
    # Final matrix completeness check
    if len(all_numbers) != 9 or set(range(9)) != all_numbers:
        print("Initialization failed! You did not include all numbers from 0 to 8. Please restart entry.")
        return get_user_matrix(matrix_name)
        
    return matrix

if __name__ == "__main__":
    print("==============================================")
    print("      Dynamic Custom 8-Puzzle A* Solver       ")
    print("==============================================")
    
    # Accept inputs from the user
    start_layout = get_user_matrix("INITIAL (STARTING)")
    goal_layout = get_user_matrix("FINAL (TARGET / GOAL)")
    
    print("\n----------------------------------------------")
    print("Confirming Initial Grid Configuration:")
    print_board(start_layout)
    print("Confirming Target Grid Configuration:")
    print_board(goal_layout)
    print("----------------------------------------------")
    
    print("Analyzing layout configurations and executing search path algorithm...\n")
    solution_steps = solve_puzzle(start_layout, goal_layout)
    
    if solution_steps:
        print(f"🎉 Success! Optimal solution discovered in {len(solution_steps) - 1} moves:")
        for index, step in enumerate(solution_steps):
            if index == 0:
                print("Step 0: (Starting Position)")
            else:
                print(f"Step {index}:")
            print_board(step)
    else:
        print("❌ Unsolvable: This initial layout mathematically cannot reach that target layout configuration.")
