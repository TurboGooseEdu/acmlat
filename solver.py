from pysat.solvers import Solver

from helpers import *

HIDDEN = "?"
MINE = "*"


class MinesweeperSolver:
    def __init__(self, field: list[list[str]]):
        self.solver = Solver("g4")
        self.field = field
        self.height = len(field)
        self.width = len(field[0])

        self._add_border_constraints()
        self._encode_open_cells_constraints()

    def _add_border_constraints(self) -> None:
        for c in range(self.width + 2):
            self.solver.add_clause([-self._cell_pos_to_var(0, c)])
            self.solver.add_clause([-self._cell_pos_to_var(self.height + 1, c)])

        for r in range(self.height + 2):
            self.solver.add_clause([-self._cell_pos_to_var(r, 0)])
            self.solver.add_clause([-self._cell_pos_to_var(r, self.width + 1)])

    def _cell_pos_to_var(self, row: int, col: int) -> int:
        return row * (self.width + 2) + col + 1

    def _encode_open_cells_constraints(self) -> None:
        for row in range(1, self.height + 1):
            for col in range(1, self.width + 1):
                cell_value = self.field[row - 1][col - 1]
                if cell_value == HIDDEN:
                    continue
                # x = mine, -x = no mine
                if cell_value == MINE:
                    self.solver.add_clause([self._cell_pos_to_var(row, col)])
                else:
                    neighbours = get_neighbour_cell_indices(row, col)
                    neighbour_vars = list(map(lambda n: self._cell_pos_to_var(*n), neighbours))
                    self._exactly(int(cell_value), neighbour_vars)

    def _exactly(self, n: int, variables: list[int]) -> None:
        for row in bool_table:
            if sum(row) == n:
                continue
            clause = []
            for i, value in enumerate(row):
                if value == 1:
                    clause.append(-variables[i])
                else:
                    clause.append(variables[i])
            self.solver.add_clause(clause)

    def is_safe_field(self, row: int, col: int) -> bool:
        if self.field[row][col] != HIDDEN:
            return self.field[row][col] != MINE
        target_cell_var = self._cell_pos_to_var(row + 1, col + 1)
        return not self.solver.solve(assumptions=[target_cell_var])


if __name__ == '__main__':

    def print_matrix(matrix):
        for row in matrix:
            print("  ".join(list(map(lambda e: str(e), row))))
        print()


    def guess_mine_for_each_cell():
        guess_for_each_cell = []
        for row in range(len(field)):
            row_guess = []
            for col in range(len(field[0])):
                row_guess.append(0 if solver.is_safe_field(row, col) else 1)
            guess_for_each_cell.append(row_guess)
        return guess_for_each_cell


    field = [
        ['0', '1', '1', '1', '0', '0', '0', '1', '?'],
        ['0', '1', '?', '1', '0', '0', '0', '1', '1'],
        ['0', '1', '1', '1', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['1', '1', '1', '1', '1', '0', '0', '1', '1'],
        ['?', '1', '1', '?', '1', '0', '0', '1', '?'],
        ['?', '?', '?', '3', '3', '1', '0', '1', '1'],
        ['?', '?', '?', '?', '?', '2', '1', '1', '0'],
        ['?', '?', '?', '?', '?', '?', '?', '1', '0']
    ]

    print("Original field:")
    print_matrix(field)

    solver = MinesweeperSolver(field)
    print("Safety for each cell (1 = safe, 0 = not safe):")
    print_matrix(guess_mine_for_each_cell())
