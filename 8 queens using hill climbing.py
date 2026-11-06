
import random

N = 8

def calculate_heuristic(board):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def hill_climbing():
    board = [random.randint(0, N - 1) for _ in range(N)]

    while True:
        current_h = calculate_heuristic(board)

        if current_h == 0:
            return board

        best_board = board[:]
        best_h = current_h

        for col in range(N):
            for row in range(N):
                if board[col] != row:
                    new_board = board[:]
                    new_board[col] = row
                    h = calculate_heuristic(new_board)

                    if h < best_h:
                        best_h = h
                        best_board = new_board

        if best_h == current_h:
            board = [random.randint(0, N - 1) for _ in range(N)]
        else:
            board = best_board

def print_board(board):
    for row in range(N):
        for col in range(N):
            if board[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

solution = hill_climbing()

print("Solution:")
print_board(solution)
print("Number of conflicts:", calculate_heuristic(solution))
