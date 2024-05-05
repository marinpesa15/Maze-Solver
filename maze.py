from cell import Cell
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_wall_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for col in range(self.num_cols):
            column = []
            for row in range(self.num_rows):
                column.append(Cell(self.win))
            self.cells.append(column)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self._animate()


    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_wall_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self.cells[i - 1][j].visited:
                next_index_list.append((i-1, j))
            if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
                next_index_list.append((i+1, j))
            if j > 0 and not self.cells[i][j - 1].visited:
                next_index_list.append((i, j-1))
            if j < self.num_rows - 1 and not self.cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return
            
            direciton_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direciton_index]

            if next_index[0] == i + 1:
                self.cells[i][j].has_right_wall = False
                self.cells[i + 1][j].has_left_wall = False
            if next_index[0] == i - 1:
                self.cells[i][j].has_left_wall = False
                self.cells[i - 1][j].has_right_wall = False
            if next_index[1] == j + 1:
                self.cells[i][j].has_bottom_wall = False
                self.cells[i][j + 1].has_top_wall = False
            if next_index[1] == j - 1:
                self.cells[i][j].has_top_wall = False
                self.cells[i][j - 1].has_bottom_wall = False
            
            self._break_wall_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()

        self.cells[i][j].visited = True

        if self.cells[i][j] == self.cells[-1][-1]:
            return True
        
        if i > 0 and self.cells[i][j].has_left_wall == False and self.cells[i-1][j].visited == False:
            self.cells[i][j].draw_move(self.cells[i-1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i-1][j], True)

        if i < self.num_cols and self.cells[i][j].has_right_wall == False and self.cells[i + 1][j].visited == False:
            self.cells[i][j].draw_move(self.cells[i+1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i+1][j], True)
        
        if j > 0 and self.cells[i][j].has_top_wall == False and self.cells[i][j - 1].visited == False:
            self.cells[i][j].draw_move(self.cells[i][j-1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j-1], True)

        if j < self.num_rows and self.cells[i][j].has_bottom_wall == False and self.cells[i][j + 1].visited == False:
            self.cells[i][j].draw_move(self.cells[i][j+1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j+1], True)
        
        return False

