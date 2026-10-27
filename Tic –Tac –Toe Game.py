import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Human vs Robot Tic-Tac-Toe")

# Setup players
HUMAN = "X"
ROBOT = "O"
buttons = []

def check_win(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player: return True
        if board[0][i] == board[1][i] == board[2][i] == player: return True
    if board[0][0] == board[1][1] == board[2][2] == player: return True
    if board[0][2] == board[1][1] == board[2][0] == player: return True
    return False

def check_tie(board):
    for row in board:
        if "" in row: return False
    return True

def get_board_state():
    return [[buttons[r][c]['text'] for c in range(3)] for r in range(3)]

# Minimax algorithm gives the robot absolute perfect logic
def minimax(board, depth, is_maximizing):
    if check_win(board, ROBOT): return 10 - depth
    if check_win(board, HUMAN): return depth - 10
    if check_tie(board): return 0

    if is_maximizing:
        best_score = float('-inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = ROBOT
                    score = minimax(board, depth + 1, False)
                    board[r][c] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = HUMAN
                    score = minimax(board, depth + 1, True)
                    board[r][c] = ""
                    best_score = min(score, best_score)
        return best_score

def robot_move():
    board = get_board_state()
    best_score = float('-inf')
    best_move = None

    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = ROBOT
                score = minimax(board, 0, False)
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    best_move = (r, c)

    if best_move:
        r, c = best_move
        buttons[r][c].config(text=ROBOT, state="disabled", disabledforeground="blue")
        check_game_over()

def check_game_over():
    board = get_board_state()
    if check_win(board, HUMAN):
        messagebox.showinfo("Game Over", "Wow! You beat the robot!")
        reset_game()
        return True
    elif check_win(board, ROBOT):
        messagebox.showinfo("Game Over", "Robot wins! Better luck next time.")
        reset_game()
        return True
    elif check_tie(board):
        messagebox.showinfo("Game Over", "It's a tie!")
        reset_game()
        return True
    return False

def human_click(row, col):
    # Player makes a move
    buttons[row][col].config(text=HUMAN, state="disabled", disabledforeground="red")
    
    # Check if the human won or tied, if not, the robot takes its turn
    if not check_game_over():
        root.after(300, robot_move) # 300ms slight delay so the robot feels like it's "thinking"

def reset_game():
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", state="normal", bg="SystemButtonFace")

# Grid layout creation
for r in range(3):
    row_buttons = []
    for c in range(3):
        btn = tk.Button(root, text="", font=('Arial', 24, 'bold'), width=5, height=2,
                        command=lambda row=r, col=c: human_click(row, col))
        btn.grid(row=r, column=c, padx=3, pady=3)
        row_buttons.append(btn)
    buttons.append(row_buttons)

root.mainloop()
