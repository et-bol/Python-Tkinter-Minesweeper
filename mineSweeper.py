import time
import tkinter
from tkinter import messagebox
import random


class mineSweeper:

    def __init__(self, master):
        self.master = master
        self.master.title("Mine Sweeper")
        self.master.resizable(False, False)
        self.mainframe = tkinter.Frame(self.master, bg='white')
        self.mainframe.pack(fill=tkinter.BOTH, expand=True)

        self.flag_image = "flag.png"
        self.flag_image_for_button = tkinter.PhotoImage(file=self.flag_image)

        # Buttons are tested based on their text values, these are constants
        self.MINE = "#"
        self.EMPTY_CELL = " "
        self.BUFFER_CELL = "  "

        self.width = 16
        self.height = 16
        self.amt_mines = 40

        self.amt_cells_cleared = 0

        # generate menu
        self.generate_menu()

        # creates a 2D list of buttons and adds in
        self.cells = self.create_cell_list(self.height, self.width)

        # adds the list of buttons into a grid
        self.generate_cells(self.cells)

    def reset(self):
        for widget in self.mainframe.winfo_children():
            widget.destroy()
        self.amt_cells_cleared = 0
        self.cells = self.create_cell_list(self.height, self.width)
        self.generate_cells(self.cells)

    # generates a 2d list filled with buttons
    def create_cell_list(self, rows, cols):
        list = []
        for row in range(rows + 1):
            list.append([])
            for col in range(cols + 1):
                btn = tkinter.Button(self.mainframe,
                                     width=2,
                                     height=1,
                                     text=" ",
                                     bg="grey",
                                     fg="grey",
                                     command=lambda a=row, b=col, c=False:
                                     self.clicked(a, b, c))
                btn.bind("<Button-3>", lambda e, a=row, b=col: self.flagged(a, b))
                btn["state"] = "disabled"
                list[row].append(btn)
        return list

    # randomly assigns mines to the list and ads proximity values to nearby cells
    def fill_cell_list(self, rows, cols, amt_mines, y, x):
        # creates buffer next to the first clicked button so that player always lands on and empty cell
        first_button = self.cells[y][x]
        first_button["text"] = self.BUFFER_CELL
        self.cells[y - 1][x]["text"] = self.BUFFER_CELL
        self.cells[y + 1][x]["text"] = self.BUFFER_CELL
        self.cells[y][x - 1]["text"] = self.BUFFER_CELL
        self.cells[y][x + 1]["text"] = self.BUFFER_CELL
        self.cells[y - 1][x + 1]["text"] = self.BUFFER_CELL
        self.cells[y - 1][x - 1]["text"] = self.BUFFER_CELL
        self.cells[y + 1][x + 1]["text"] = self.BUFFER_CELL
        self.cells[y + 1][x - 1]["text"] = self.BUFFER_CELL

        # fills with mines
        for x in range(amt_mines):
            btn = self.cells[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
            if btn["text"] == self.MINE or btn["text"] == self.BUFFER_CELL:
                while btn["text"] == self.MINE or btn["text"] == self.BUFFER_CELL:
                    btn = self.cells[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
            btn["text"] = self.MINE

        # fills with proximity values
        for row in range(rows):
            for col in range(cols):
                btn = self.cells[row][col]
                if btn["text"] == self.MINE:
                    continue
                else:
                    neighbors = self.amt_neighbors(row, col)
                    if neighbors == 0:
                        btn["text"] = self.EMPTY_CELL
                    else:
                        btn["text"] = neighbors

    def generate_cells(self, cells):
        width = len(cells[0]) - 1
        height = len(cells) - 1
        for row_index in range(height):
            tkinter.Grid.rowconfigure(self.mainframe, row_index, weight=1)
            for col_index in range(width):
                tkinter.Grid.columnconfigure(self.mainframe, col_index, weight=1)
                btn = cells[row_index][col_index]
                btn["state"] = "normal"
                btn.grid(row=row_index, column=col_index, sticky="nsew")

    def generate_menu(self):
        menubar = tkinter.Menu(self.master)

        game = tkinter.Menu(menubar, tearoff=0)
        game.add_radiobutton(label="Beginner ( Width = 10, Height = 10, Mines = 12 )",
                         command=self.beginner)
        game.add_radiobutton(label="Intermediate ( Width = 16, Height = 16, Mines = 40 )",
                         command=self.intermediate)
        game.add_radiobutton(label="Expert ( Width = 30, Height = 16, Mines = 99 )",
                         command=self.expert)
        menubar.add_cascade(label='Game', menu=game)

        menubar.add_separator()

        display = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Display", menu=display)

        menubar.add_separator()

        reset = tkinter.Menu(menubar, tearoff=0)
        reset.add_command(label="Click To Reset", command=self.reset)
        menubar.add_cascade(label="Reset", menu=reset)

        self.master.config(menu=menubar)

    # -----------   MENU BAR METHODS   --------------------
    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_amt_mines(self, amt_mines):
        self.amt_mines = amt_mines

    def beginner(self):
        self.width = 10
        self.height = 10
        self.amt_mines = 12

    def intermediate(self):
        self.width = 16
        self.height = 16
        self.amt_mines = 40

    def expert(self):
        self.width = 30
        self.height = 16
        self.amt_mines = 99

    def amt_neighbors(self, row, col):
        neighbors = 0
        if self.cells[row - 1][col]["text"] == self.MINE:
            neighbors += 1
        if self.cells[row - 1][col - 1]["text"] == self.MINE:
            neighbors += 1
        if self.cells[row - 1][col + 1]["text"] == self.MINE:
            neighbors += 1
        if self.cells[row][col - 1]["text"] == self.MINE:
            neighbors += 1
        if self.cells[row][col + 1]["text"] == self.MINE:
            neighbors += 1
        if self.cells[row + 1][col]["text"] == self.MINE:
            neighbors += 1
        if self.cells[row + 1][col + 1]["text"] == self.MINE:
            neighbors += 1
        if self.cells[row + 1][col - 1]["text"] == self.MINE:
            neighbors += 1
        return neighbors

    def clicked(self, row, col, recur):
        btn = self.cells[row][col]
        if self.amt_cells_cleared == 0:
            self.fill_cell_list(self.height, self.width, self.amt_mines, row, col)
            self.amt_cells_cleared += 9
        if btn["text"] == self.MINE and recur == False:
            btn["state"] = "disabled"
            btn.config(relief=tkinter.SUNKEN, bg="red")
            self.reveal_buttons()
            self.losing_message()
        elif self.amt_cells_cleared == ((self.width * self.height) - self.amt_mines):
            self.winning_message()
        elif btn["text"] == self.EMPTY_CELL and btn["state"] == "normal":
            btn["state"] = "disabled"
            btn.config(relief=tkinter.SUNKEN, bg="white")
            self.amt_cells_cleared += 1
            self.clicked(row - 1, col, True)
            self.clicked(row + 1, col, True)
            self.clicked(row - 1, col - 1, True)
            self.clicked(row - 1, col + 1, True)
            self.clicked(row + 1, col - 1, True)
            self.clicked(row - 1, col + 1, True)
            self.clicked(row, col - 1, True)
            self.clicked(row, col + 1, True)
        elif btn["state"] == "normal":
            self.amt_cells_cleared += 1
            btn["state"] = "disabled"
            btn.config(relief=tkinter.SUNKEN, bg="white")

    def flagged(self, row, col):
        btn = self.cells[row][col]
        if btn["state"] == "normal" and btn["relief"] != tkinter.SUNKEN:
            btn["state"] = "disabled"
            btn.config(image=self.flag_image_for_button)
        elif btn['state'] == "disabled" and btn["relief"] != tkinter.SUNKEN:
            btn["state"] = "normal"
            btn.config(bg="grey", fg="grey", image="")

    def winning_message(self):
        tkinter.messagebox.showinfo("WIN", "You Win!!!")
        self.reset()

    def losing_message(self):
        tkinter.messagebox.showinfo("Loss", "You Lose!!!")
        self.reset()

    def reveal_buttons(self):
        width = len(self.cells[0])
        height = len(self.cells)

        for row in range(height):
            for col in range(width):
                btn = self.cells[row][col]
                if btn["state"] == "disabled" and btn["image"] == "":
                    continue
                else:
                    btn["state"] = "disabled"
                    btn.config(image="")
                    if btn["text"] == self.MINE:
                        btn.config(relief=tkinter.SUNKEN, bg="red")
                    else:
                        btn.config(relief=tkinter.SUNKEN, bg="yellow")


if __name__ == '__main__':
    root = tkinter.Tk()
    mineSweeper(root)
    root.mainloop()


