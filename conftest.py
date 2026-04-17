import json
from pathlib import Path

import pytest

import matrix
import matrix_types_for_tests as mtft

# Load example matrices from JSON file.
matrices: dict[str, dict]
with Path("test_matrix_cases.json").open() as f:
    matrices: dict[str, dict] = json.load(f)


@pytest.fixture(params=matrices)
def matrix_init_data_fixture(
    request: pytest.FixtureRequest,
) -> mtft.MatrixInitData:
    """Get initializer data for a Matrix."""
    matrix_dict: dict = request.param
    matrix_dict.setdefault("augmented", False)
    return matrix_dict["data"], matrix_dict["augmented"]


@pytest.fixture
def matrix_class_with_init_data_fixture(
    matrix_init_data_fixture: mtft.MatrixInitData,
) -> mtft.MatrixWithInitData:
    """Get a pre-initialized Matrix along with init data."""
    data, augmented = matrix_init_data_fixture

    return matrix.Matrix(data, augmented), (data, augmented)
