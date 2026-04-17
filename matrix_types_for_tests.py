"""Convenient type annotations for use with testing."""

import matrix

MatrixInitData = tuple[matrix.Data, bool]
MatrixWithInitData = tuple[matrix.Matrix, MatrixInitData]
