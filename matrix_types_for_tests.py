"""Convenient type annotations for use with testing."""
import types

import matrix

# Types for general-purpose fixtures.
InitData = tuple[matrix.Data, bool]
ClassWithInitData = tuple[matrix.Matrix, InitData]
ClassWith2Randoms = tuple[matrix.Matrix, int, int]
Slice = list[float]

# Types for test-specific fixtures. (setup/teardown)
AddRowData = tuple[matrix.Matrix, int, int, float, Slice]
