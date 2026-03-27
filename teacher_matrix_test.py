import pytest

import matrix

# All sorts of bad practices are present here, but I've left them for
# compatibility with the teacher's code. A better test module is present
# as ``test_matrix.py``.

# ruff: noqa

# A wrapper for my implementation, with a signature copied from the
# teacher's source files. Type annotations added.
def twoRowGausian(A=[[1,0,0],[0,1,0]]) -> tuple[list[list[float]], int]:
    # -- Initialize Matrix --

    the_matrix: matrix.Matrix =\
        matrix.Matrix(A, augmented=True, reflect_data=True)

    # -- Change to RREF --

    the_matrix.gaussian_elimination()

    # -- Check number of solutions

    # Free variables and inconsistencies will be listed at the bottom,
    # as per RREF, so the matrix will be searched from bottom to top.
    solution_type: int = 0

    for row in range(the_matrix.size[1]-1, -1, -1):
        # --- Stop iterating when we've left the zero rows ---
        row_leading_1_found: bool = False

        for col in range(the_matrix.size[0]):
            if not row_leading_1_found and the_matrix.data[col][row] != 0:
                row_leading_1_found = True
                break

        # If there's a leading 1, we've passed the zero rows.
        if row_leading_1_found:
            break

        # --- Check whether row makes sense (consistent) ---

        if the_matrix.data[the_matrix.size[0]][row] == 0:
            solution_type = 1
        else:
            # If it doesn't make sense, we don't need to keep going.
            solution_type = 2
            break

    # -- Reflect matrix data to match teacher's format --
    new_data: list[list[float]] = [[] for i in range(the_matrix.size[1])]

    for col in range(the_matrix.get_row_length()):
        for row in range(the_matrix.size[1]):
            new_data[row].append(the_matrix.data[col][row])

    # Return values are RREF data, and the solution type, which may be:
        # 0: Found a solution
        # 1: Infinite solutions (free variables present)
        # 2: No solution (system is inconsistent)
    return new_data, solution_type

# Test copied and pasted from teacher's OneDrive.
# Leave as is, so it can be easily updated by copy/paste.
def test_twoRowGausian():
   assert twoRowGausian([[ 2,3,7],[ -4,6,-2]]) == ([[1.0, 0.0, 2.0], [0.0, 1.0, 1.0]], 0)
   assert twoRowGausian([[ 2,3,7],[  4,6,-2]])[1] == 2
   assert twoRowGausian([[ 2,3,7],[ 4,6,14]])[1] == 1
   assert twoRowGausian([[ 2,3,12],[ -4,6,0]]) == ([[1.0, 0.0, 3.0], [0.0, 1.0, 2.0]], 0)
