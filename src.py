import random
import time
import gurobipy as gp
from gurobipy import GRB
import tkinter as tk
from tkinter import messagebox

n, m = None, None
row_blocks, col_blocks = [], []
grid_buttons = []
gurobi_solution = []
ans = []
br, bc, er, lr, ec, lc = [], [], [], [], [], []
difficulty = None
puzzle_bank = [
    {
        "row_blocks": [[2], [2], [1, 1], [4], [3]],
        "col_blocks": [[1, 1], [1, 3], [2], [3], [1, 1]],
    },
    {
        "row_blocks": [[3], [1, 2], [1], [2], [4]],
        "col_blocks": [[1], [1, 2], [1, 2], [3, 1], [2]],
    },
    {
        "row_blocks": [[2], [2, 1], [1], [3], [4]],
        "col_blocks": [[1, 2], [4], [2], [2, 1], [1]],
    },
    {
        "row_blocks": [[3], [2], [3], [1], [4]],
        "col_blocks": [[1], [2], [1, 1, 1], [3, 1], [3]],
    },
    {
        "row_blocks": [[1, 2], [2], [3], [2], [3]],
        "col_blocks": [[1, 3], [3], [1, 1], [2], [2]],
    },
    {
        "row_blocks": [[2], [3], [3], [2, 1], [2]],
        "col_blocks": [[2], [3], [3], [2, 1], [2]],
    },
    {
        "row_blocks": [[1, 1], [1, 1], [4], [3], [2]],
        "col_blocks": [[2], [1], [4], [3], [3]],
    },
    {
        "row_blocks": [[1], [3], [5], [3], [1]],
        "col_blocks": [[1], [3], [5], [3], [1]],
    },
    {
        "row_blocks": [[1, 1], [1, 1], [2], [3], [3, 1]],
        "col_blocks": [[2], [2, 2], [3], [3], [1]],
    },
    {
        "row_blocks": [[2], [3], [2], [3], [2, 1]],
        "col_blocks": [[4], [4], [1, 1], [1, 1], [1]],
    },
    {
        "row_blocks": [[3, 2], [3, 3], [3, 3], [4, 3], [4, 1, 2], [5, 1], [3, 1, 2], [1], [2], [2, 2]],
        "col_blocks": [[5, 1], [7], [7], [3, 1], [2, 1], [1, 2], [3], [5], [3, 1, 2], [1, 5]],
    },
    {
        "row_blocks": [[1, 3], [1, 3], [2, 2], [1, 1], [3], [8], [8], [8], [3], [3, 3]],
        "col_blocks": [[3], [1], [4, 1], [4, 1], [5, 1], [3, 3], [4, 3], [2, 5], [5], [5]],
    },
    {
        "row_blocks": [[1, 3, 2], [5, 1], [1, 1, 2], [1, 4], [2, 2], [3, 3], [3, 2], [4, 2], [1, 1, 1], [5]],
        "col_blocks": [[4, 1], [1, 2], [3, 3], [2, 1, 1, 1], [4, 3], [3, 1, 1], [2, 2], [1, 1], [1, 6], [2, 4]],
    },
    {
        "row_blocks": [[3, 2], [2, 3], [1, 3], [2, 3], [2, 1], [2], [1, 1, 3, 2], [3, 1, 1, 2], [3, 1, 2], [3, 1, 2]],
        "col_blocks": [[4], [3], [1, 4], [6], [2, 4, 1], [1, 1], [3], [3], [4, 4], [5, 4]],
    },
    {
        "row_blocks": [[3, 1], [3, 1], [3], [3, 4], [9], [4, 1], [3, 2], [4, 2], [2, 2], [3]],
        "col_blocks": [[1, 3], [6], [8, 1], [8], [6], [1], [3], [2], [2, 3], [2, 1, 3]],
    },
]


def filter_puzzles():
    global puzzle_bank
    if difficulty == "Easy":
        return [p for p in puzzle_bank if len(p["row_blocks"]) == 5 and len(p["col_blocks"]) == 5]
    elif difficulty == "Hard":
        return [p for p in puzzle_bank if len(p["row_blocks"]) == 10 and len(p["col_blocks"]) == 10]
    return puzzle_bank


def get_block_size(i, is_row=True):
    if is_row:
        return len(row_blocks[i])
    return len(col_blocks[i])


def get_e(data):
    e = {}
    for i, x in enumerate(data):
        index = 0
        Flag = False
        for t, each in enumerate(x):
            if Flag:
                e[i, t] = index + 1
            else:
                e[i, t] = index
                Flag = True
            index += each
    return e


def get_l(data, is_row=True):
    l = {}
    for i, x in enumerate(data):
        index = m if is_row else n
        Flag = False
        for t, each in enumerate(reversed(x)):
            if Flag:
                l[i, len(x) - 1 - t] = index - each - 1
            else:
                l[i, len(x) - 1 - t] = index - each
                Flag = True
            index -= each
    return l


def display_solution():
    for i in range(n):
        for j in range(m):
            btn = grid_buttons[i][j]
            btn.config(bg="black" if ans[i][j] > 0.5 else "white")


def solve_with_gurobi():
    global gurobi_solution
    br.clear()
    bc.clear()
    for i in range(n):
        br.append(get_block_size(i, True))

    for j in range(m):
        bc.append(get_block_size(j, False))

    er = get_e(row_blocks)
    ec = get_e(col_blocks)

    lr = get_l(row_blocks, True)
    lc = get_l(col_blocks, False)

    model = gp.Model("Nonogram")
    model.setParam('OutputFlag', 0)

    z = {}
    for i in range(n):
        for j in range(m):
            z[i, j] = model.addVar(name=f'z[{i}, {j}]', vtype=GRB.BINARY)

    y = {}
    for i in range(n):
        for t in range(br[i]):
            for j in range(er[i, t], lr[i, t] + 1):
                y[i, t, j] = model.addVar(name=f'y[{i}, {t}, {j}]', vtype=GRB.BINARY)

    x = {}
    for j in range(m):
        for t in range(bc[j]):
            for i in range(ec[j, t], lc[j, t] + 1):
                x[j, t, i] = model.addVar(name=f'y[{j}, {t}, {i}]', vtype=GRB.BINARY)

    for i in range(n):
        for t in range(br[i]):
            model.addConstr(gp.quicksum(y[i, t, j] for j in range(er[i, t], lr[i, t] + 1)) == 1)
            if t < br[i] - 1:
                for j in range(er[i, t], lr[i, t] + 1):
                    model.addConstr(
                        y[i, t, j] <= gp.quicksum(
                            y[i, t + 1, J] for J in range(j + 1 + row_blocks[i][t], lr[i, t + 1] + 1))
                    )

    for j in range(m):
        for t in range(bc[j]):
            model.addConstr(gp.quicksum(x[j, t, i] for i in range(ec[j, t], lc[j, t] + 1)) == 1)
            if t < bc[j] - 1:
                for i in range(ec[j, t], lc[j, t] + 1):
                    model.addConstr(
                        x[j, t, i] <= gp.quicksum(
                            x[j, t + 1, I] for I in range(i + 1 + col_blocks[j][t], lc[j, t + 1] + 1))
                    )

    for i in range(n):
        for j in range(m):
            model.addConstr(
                z[i, j] <= gp.quicksum(
                    gp.quicksum(
                        y[i, t, J] for J in range(max(er[i, t], j - row_blocks[i][t] + 1), min(lr[i, t], j) + 1)
                    ) for t in range(br[i])
                )
            )

    for i in range(n):
        for j in range(m):
            model.addConstr(
                z[i, j] <= gp.quicksum(
                    gp.quicksum(
                        x[j, t, I] for I in range(max(ec[j, t], i - col_blocks[j][t] + 1), min(lc[j, t], i) + 1)
                    ) for t in range(bc[j])
                )
            )

    for i in range(n):
        for j in range(m):
            for t in range(br[i]):
                for J in range(max(er[i, t], j - row_blocks[i][t] + 1), min(lr[i, t], j) + 1):
                    model.addConstr(z[i, j] >= y[i, t, J])

    for j in range(m):
        for i in range(n):
            for t in range(bc[j]):
                for I in range(max(ec[j, t], i - col_blocks[j][t] + 1), min(lc[j, t], i) + 1):
                    model.addConstr(z[i, j] >= x[j, t, I])

    model.setObjective(0)
    start = time.time()
    model.optimize()
    end = time.time()

    if model.status == gp.GRB.INFEASIBLE:
        print("###################\n### No Solution ###\n###################")
    else:
        gurobi_solution = [[int(z[i, j].x > 0.5) for j in range(m)] for i in range(n)]
        ans.clear()
        for i in range(n):
            element = []
            for j in range(m):
                if z[i, j].x > 0.5:
                    element.append(1)
                else:
                    element.append(0)
            ans.append(element)
        return ans
    print(f"Solved in {end - start} seconds.")


def randomize_puzzle():
    global row_blocks, col_blocks, n, m
    puzzles = filter_puzzles()
    puzzle = random.choice(puzzles)
    row_blocks = puzzle["row_blocks"]
    col_blocks = puzzle["col_blocks"]
    n = len(row_blocks)
    m = len(col_blocks)


def create_game_board():
    global n, m, grid_buttons
    randomize_puzzle()

    for widget in root.winfo_children():
        widget.destroy()

    for i, row in enumerate(row_blocks):
        tk.Label(root, text="  ".join(map(str, row)), font=("Arial", 13, "bold")).grid(row=i + 1, column=0, sticky='e')

    for j, col in enumerate(col_blocks):
        tk.Label(root, text="\n".join(map(str, col)), font=("Arial", 13, "bold")).grid(row=0, column=j + 1, sticky='s')

    grid_buttons = [[None for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            btn = tk.Button(root, width=5, height=2, bg="white", command=lambda i=i, j=j: toggle_cell(i, j))
            btn.grid(row=i + 1, column=j + 1)
            grid_buttons[i][j] = btn

    solve_with_gurobi()

    solve_button = tk.Button(root, text="Solve", command=display_solution)
    solve_button.grid(row=n + 3, columnspan=m + 1, pady=10)

    check_button = tk.Button(root, text="Check", command=check_current_solution)
    check_button.grid(row=n + 2, columnspan=m + 1, pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white")
    exit_button.grid(row=n + 4, columnspan=m + 1, pady=10)


def toggle_cell(i, j):
    btn = grid_buttons[i][j]
    if btn["bg"] == "white":
        btn.config(bg="black")
    else:
        btn.config(bg="white")


def check_solution():
    player_solution = [[1 if grid_buttons[i][j]["bg"] == "black" else 0 for j in range(m)] for i in range(n)]
    return player_solution == gurobi_solution


def check_current_solution():
    if check_solution():
        messagebox.showinfo("Congratulations", "You won!")
    else:
        messagebox.showinfo("Keep Trying", "Don't give up!")


def show_difficulty_selection():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Choose a Difficulty Level:", font=("Arial", 11)).pack(pady=20)
    tk.Button(root, text="Easy", font=("Arial", 9), command=lambda: set_difficulty("Easy")).pack(pady=10)
    tk.Button(root, text="Hard", font=("Arial", 9), command=lambda: set_difficulty("Hard")).pack(pady=10)
    tk.Button(root, text="Exit", font=("Arial", 9), command=root.quit, bg="red", fg="white").pack(pady=10)

def set_difficulty(new_difficulty):
    global difficulty
    difficulty = new_difficulty
    create_game_board()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Nonogram")
    show_difficulty_selection()
    root.mainloop()