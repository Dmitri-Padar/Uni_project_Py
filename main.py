import tkinter as tk
from random import sample
import time

side = 3
block = side * side

def pattern(r, c):
    return (side * (r % side) + r // side + c) % block


def mix(size):
    return sample(list(size), len(size))

def generator():
    rBase = range(side)
    nums = mix(range(1, block + 1))

    rows = []
    for i in mix(rBase):
        for j in mix(rBase):
            rows.append(i * side + j)

    cols = []
    for i in mix(rBase):
        for j in mix(rBase):
            cols.append(i * side + j)

    layout = []

    for r in rows:
        row = []
        for c in cols:
            row.append(nums[pattern(r, c)])
        layout.append(row)

    return layout

def remove_numbers(layout, difficulty):
    blocks = block * block

    if difficulty == "1":
        empty = blocks // 3
    elif difficulty == "2":
        empty = blocks // 2
    else:
        empty = blocks * 3 // 5

    coords = sample(
        [(r, c) for r in range(block) for c in range(block)],
        empty
    )

    for r, c in coords:
        layout[r][c] = " "

    return layout


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Generator")
        self.root.geometry("850x520")
        self.root.configure(bg="beige")

        self.frame = tk.Frame(root, bg="beige")
        self.frame.pack(pady=10)

        self.difficulty = tk.StringVar(value="1")

        self.game_over = False
        self.timer_running = False
        self.start_time = 0
        self.checks_left = 3

        tk.Label(
            self.frame,
            text="Choose difficulty:",
            bg="BEIGE"
        ).grid(row=0, column=0)

        tk.OptionMenu(
            self.frame,
            self.difficulty,
            "1", "2", "3"
        ).grid(row=0, column=1)

        tk.Button(
            self.frame,
            text="Generate",
            command=self.generate
        ).grid(row=0, column=2)

        tk.Button(
            self.frame,
            text="Check",
            command=self.check_solution
        ).grid(row=0, column=3)
        
        self.checks_label = tk.Label(
            self.frame,
            text=f"Checks left: {self.checks_left}",
            font=("Arial", 12),
            bg="BEIGE"
        )
        self.checks_label.grid(row=0, column=5, padx=20)

        self.timer_label = tk.Label(
            self.frame,
            text="Time: 00:00",
            font=("Arial", 12),
            bg="BEIGE"
        )
        self.timer_label.grid(row=0, column=4, padx=20)

        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=10)

        self.update_timer()

    def update_timer(self):
        if self.timer_running and not self.game_over:
            elapsed = int(time.time() - self.start_time)

            minutes = elapsed // 60
            seconds = elapsed % 60

            self.timer_label.config(
                text=f"Time: {minutes:02}:{seconds:02}"
            )
        self.root.after(1000, self.update_timer)
        
    def validate_input(self, value):
        return value == "" or (value in "123456789" and len(value) == 1)

    def generate(self):
        self.start_time = time.time()
        self.game_over = False
        self.timer_running = True
        
        self.checks_left = 3
        self.checks_label.config(
            text=f"Checks left: {self.checks_left}"
        )

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.entries = []
        
        vcmd = (self.root.register(self.validate_input), "%P")

        ready_layout = generator()

        self.solution = [row[:] for row in ready_layout]

        for_solution_layout = remove_numbers(
            ready_layout,
            self.difficulty.get()
        )

        for i in range(block):
            row_entries = []

            for j in range(block):
                val = for_solution_layout[i][j]

                interactive = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=("Arial", 18),
                    justify="center",
                    borderwidth=1,
                    relief="ridge",
                    validate="key",
                    validatecommand=vcmd
                )

                if val != " ":
                    interactive.insert(0, str(val))
                    interactive.config(state="disabled")

                padx = (3 if j % 3 == 0 else 1, 3 if j == 8 else 1)
                pady = (3 if i % 3 == 0 else 1, 3 if i == 8 else 1)

                interactive.grid(
                    row=i,
                    column=j,
                    padx=padx,
                    pady=pady
                )

                row_entries.append(interactive)

            self.entries.append(row_entries)

    def check_solution(self):
        if self.checks_left <= 0:
            return

        self.checks_left -= 1

        self.checks_label.config(
            text=f"Checks left: {self.checks_left}"
        )

        correct = True

        for i in range(block):
            for j in range(block):
                entry = self.entries[i][j]
                number = entry.get()

                if not number.isdigit():
                    entry.config(bg="pink")
                    correct = False
                    continue

                if int(number) != self.solution[i][j]:
                    entry.config(bg="pink")
                    correct = False
                else:
                    entry.config(bg="lightgreen")

        if correct:
            self.game_over = True

            tk.Label(
                self.frame,
                text="Good job!!!",
                font=("Arial", 12, "bold"),
                bg="BEIGE",
                fg="green"
            ).grid(row=1, column=0, columnspan=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
