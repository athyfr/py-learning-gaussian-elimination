"""Convenient type annotations for use with testing."""
import matrix

# Types for general-purpose fixtures.
Info = dict
ClassWithInfo = tuple[matrix.Matrix, Info]
ClassWith1Random = tuple[matrix.Matrix, int]
ClassWith2Randoms = tuple[matrix.Matrix, int, int]
Slice = list[float]

# Types for test-specific fixtures. (setup/teardown)
AddRowData = tuple[matrix.Matrix, int, int, float, Slice]
MultiplyRowData = tuple[matrix.Matrix, int, float, Slice | None]
SwapRowData = tuple[matrix.Matrix, int, int, matrix.Data]
