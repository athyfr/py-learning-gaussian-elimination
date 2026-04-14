import json
from pathlib import Path

import pytest

# Load example matrices from JSON file.
matrices: dict[str, dict]
with Path("test_matrix_cases.json").open() as f:
    matrices: dict[str, dict] = json.load(f)


@pytest.fixture(params=matrices)
def matrix_init_data_fixture(
    request: pytest.FixtureRequest,
) -> tuple[list[list[float]], bool]:
    """Get initializer data for a Matrix."""
    matrix: dict = request.param
    return matrix["data"], matrix["augmented"]
