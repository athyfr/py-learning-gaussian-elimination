import pytest
import matrix

# -- Implementations of the Teacher's tests.

# A wrapper for my implementation, with a signature copied from the
# teacher's source files.
def twoRowGausian(A=[[1,0,0],[0,1,0]]):
    the_matrix: matrix.Matrix = matrix.Matrix()

# Copied and pasted from teacher's OneDrive:
def test_twoRowGausian():
   assert twoRowGausian([[ 2,3,7],[ -4,6,-2]]) == ([[1.0, 0.0, 2.0], [0.0, 1.0, 1.0]], 0)
   assert twoRowGausian([[ 2,3,7],[  4,6,-2]])[1] == 2
   assert twoRowGausian([[ 2,3,7],[ 4,6,14]])[1] == 1
   assert twoRowGausian([[ 2,3,12],[ -4,6,0]]) == ([[1.0, 0.0, 3.0], [0.0, 1.0, 2.0]], 0)

# -- Some of my own tests
