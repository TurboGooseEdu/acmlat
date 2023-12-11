shifts = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def get_neighbour_cell_indices(row: int, col: int) -> list[tuple[int, int]]:
    neighbours = []
    for shift in shifts:
        row_shift, col_shift = shift
        new_row = row + row_shift
        new_col = col + col_shift
        neighbours.append((new_row, new_col))
    return neighbours


def generate_bool_table(n: int) -> list[list[int]]:
    table = []

    def gen(cur_table: list[int]) -> None:
        if len(cur_table) == n:
            table.append(cur_table)
            return
        gen(cur_table + [0])
        gen(cur_table + [1])

    gen([])
    return table


bool_table = generate_bool_table(8)
