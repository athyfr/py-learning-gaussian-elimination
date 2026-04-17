"""Convenient type annotations for use with testing."""

import matrix

InitData = tuple[matrix.Data, bool]
ClassWithInitData = tuple[matrix.Matrix, InitData]
