from collections import deque

# Define the sample tree graph
#         A
#       /   \
#      B     C
#     / \   / \
#    D   E F   G
#   /
#  H
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': [],
    'G': [],
    'H': []
}

# --- 1. BREADTH-FIRST SEARCH (BFS) ---
def bfs(graph, start, target):
    visited = set()
    queue = deque([[start]])
    nodes_explored = 0
    
    if start == target:
        return [start], 1
        
    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_explored += 1
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                new_path = list(path) + [neighbor]
                if neighbor == target:
                    return new_path, nodes_explored + 1
                queue.append(new_path)
    return None, nodes_explored

# --- 2. DEPTH-FIRST SEARCH (DFS) ---
def dfs(graph, start, target, path=None, visited=None, counter=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    if counter is None:
        counter = [0]
        
    counter[0] += 1
    if start == target:
        return path, counter[0]
        
    visited.add(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result, total_steps = dfs(graph, neighbor, target, path + [neighbor], visited, counter)
            if result is not None:
                return result, total_steps
    return None, counter[0]

# --- 3. ITERATIVE DEEPENING SEARCH (IDDFS) ---
def dls(graph, current, target, limit, path, counter):
    counter[0] += 1
    path.append(current)
    if current == target:
        return path
    if limit <= 0:
        path.pop()
        return None
        
    for neighbor in graph.get(current, []):
        if neighbor not in path:
            result = dls(graph, neighbor, target, limit - 1, path, counter)
            if result is not None:
                return result
    path.pop()
    return None

def iddfs(graph, start, target, max_depth=10):
    total_steps = [0]
    for depth in range(max_depth):
        path = []
        result = dls(graph, start, target, depth, path, total_steps)
        if result is not None:
            return result, total_steps[0]
    return None, total_steps[0]

# --- MAIN EXECUTION & OPTIMALITY SUMMARY ---
if __name__ == "__main__":
    print("==============================================")
    print("       Graph Search Algorithm Evaluator       ")
    print("==============================================")
    print("Available nodes: A, B, C, D, E, F, G, H")
    
    start_node = input("Enter START node: ").strip().upper()
    target_node = input("Enter TARGET node: ").strip().upper()
    
    if start_node not in graph or target_node not in graph:
        print("\n❌ Error: Nodes missing from graph.")
    else:
        print(f"\nEvaluating paths from '{start_node}' to '{target_node}'...\n")
        
        # Run algorithms and track execution stats
        path_bfs, steps_bfs = bfs(graph, start_node, target_node)
        path_dfs, steps_dfs = dfs(graph, start_node, target_node)
        path_iddfs, steps_iddfs = iddfs(graph, start_node, target_node)
        
        # Display Results
        print("--- SEARCH PROCESS ANALYSIS ---")
        print(f"🔹 BFS   -> Path: {' -> '.join(path_bfs) if path_bfs else 'None'} | Nodes Checked: {steps_bfs}")
        print(f"🔸 DFS   -> Path: {' -> '.join(path_dfs) if path_dfs else 'None'} | Nodes Checked: {steps_dfs}")
        print(f"🔺 IDDFS -> Path: {' -> '.join(path_iddfs) if path_iddfs else 'None'} | Nodes Checked: {steps_iddfs}\n")
        
        # Print Complexity Reference Table
        print("--- COMPLEXITY CHEAT-SHEET ---")
        print("• BFS   | Time: O(b^d) | Space: O(b^d)   | Guarantees Shortest Path: YES")
        print("• DFS   | Time: O(b^m) | Space: O(b*m)   | Guarantees Shortest Path: NO")
        print("• IDDFS | Time: O(b^d) | Space: O(b*d)   | Guarantees Shortest Path: YES")
        print("(b = branch factor, d = answer depth, m = max tree depth)\n")

        print("--- OPTIMALITY CONCLUSION ---")
        if not path_bfs:
            print("❌ No valid solution paths exist between these nodes.")
        else:
            # Determine path length optimality
            len_bfs = len(path_bfs)
            len_dfs = len(path_dfs)
            
            if len_bfs < len_dfs:
                print(f"✔️ **Path Optimality**: **BFS and IDDFS are optimal**. They found the shortest path ({len_bfs} nodes).")
                print(f"   ⚠️ DFS took a longer, non-optimal route ({len_dfs} nodes).")
            elif len_bfs == len_dfs:
                print(f"✔️ **Path Optimality**: All three algorithms found the same shortest path length ({len_bfs} nodes).")
            
            # Determine space-time efficiency balance recommendation
            print("\n👑 **Engine Recommendation**:")
            print("   For this tiny graph, standard BFS or DFS completes almost instantly.")
            print("   However, **IDDFS is the overall architectural winner**.")
            print("   Why? It guarantees the shortest path using minimal O(b*d) DFS memory space,")
            print("   avoiding the catastrophic O(b^d) memory explosion that BFS suffers from on large trees.")
