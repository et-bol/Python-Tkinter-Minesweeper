import tkinter
import random


class mineSweeper:

    def __init__(self, master):
        self.master = master
        self.master.title("Mine Sweeper")
        self.master.resizable(False, False)
        self.mainframe = tkinter.Frame(self.master, bg='white')
        self.mainframe.pack(fill=tkinter.BOTH, expand=True)

        self.MINE = "#"
        self.EMPTY_CELL = " "

        width = 30
        height = 25
        amt_mines = 100

        # generate menu
        self.generate_menu()

        # creates a 2D list of buttons and adds in
        self.cells = self.create_cell_list(height, width)
        self.fill_cell_list(height, width, amt_mines)

        # adds the list of buttons into a grid
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
                                     self.clicked(a, b, c)
                                     )
                btn["state"] = "disabled"
                list[row].append(btn)
        return list

    # randomly assigns mines to the list and ads proximity values to nearby cells
    def fill_cell_list(self, rows, cols, amt_mines):
        # fills with mines
        for x in range(amt_mines):
            btn = self.cells[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
            if btn["text"] == self.MINE:
                while btn["text"] == self.MINE:
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
                        continue
                    else:
                        btn["text"] = neighbors

    def generate_cells(self, cells):
        width = len(cells[0]) - 1
        height = len(cells) - 1
        for row_index in range(height):
            tkinter.Grid.rowconfigure(self.mainframe, row_index, weight=1)
            for col_index in range(width):
                tkinter.Grid.columnconfigure(self.mainframe, col_index, weight=1)
                cells[row_index][col_index]["state"] = "normal"
                cells[row_index][col_index].grid(row=row_index, column=col_index, sticky="nsew")

    def generate_menu(self):
        menubar = tkinter.Menu(self.master)

        game = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Game', menu=game)

        display = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Display", menu=display)

        reset = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reset", menu=reset)

        self.master.config(menu=menubar)

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
        if btn["text"] == self.MINE and recur == False:
            print("You Lose!")
        elif btn["text"] == self.EMPTY_CELL and btn["state"] == "normal":
            btn["state"] = "disabled"
            btn.config(relief=tkinter.SUNKEN)
            self.clicked(row - 1, col, True)
            self.clicked(row + 1, col, True)
            self.clicked(row - 1, col - 1, True)
            self.clicked(row - 1, col + 1, True)
            self.clicked(row + 1, col - 1, True)
            self.clicked(row - 1, col + 1, True)
            self.clicked(row, col - 1, True)
            self.clicked(row, col + 1, True)
        else:
            btn["state"] = "disabled"
            btn.config(relief=tkinter.SUNKEN, bg="white")


if __name__ == '__main__':
    root = tkinter.Tk()
    mineSweeper(root)
    root.mainloop()