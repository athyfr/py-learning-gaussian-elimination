import json
from pathlib import Path

import pytest

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
    return matrix_dict["data"], matrix_dict["augmented"]
