import json
import random
from pathlib import Path

import pytest

import matrix
import matrix_types_for_tests as mtft

# Load example matrices from JSON file.
matrices: dict[str, dict]
with Path("test_matrix_cases.json").open() as f:
    matrices: dict[str, dict] = json.load(f)


@pytest.fixture(params=matrices.values(), ids=matrices.keys())
def matrix_init_data_fixture(
    request: pytest.FixtureRequest,
) -> mtft.InitData:
    """Get initializer data for a Matrix."""
    matrix_dict: dict = request.param
    matrix_dict.setdefault("augmented", False)
    return matrix_dict["data"], matrix_dict["augmented"]


@pytest.fixture
def matrix_class_with_init_data_fixture(
    matrix_init_data_fixture: mtft.InitData,
) -> mtft.ClassWithInitData:
    """Get a pre-initialized Matrix along with init data."""
    data, augmented = matrix_init_data_fixture

    return matrix.Matrix(data, augmented), (data, augmented)


@pytest.fixture
def matrix_class_with_1_row_index_fixture(
    matrix_class_with_init_data_fixture: mtft.ClassWithInitData,
) -> mtft.ClassWith1Random:
    """Get a pre-initialized matrix with 1 random row index."""
    matrix = matrix_class_with_init_data_fixture[0]
    rng = random.Random()

    row = rng.choice(range(matrix.size[1]))

    return matrix, row


@pytest.fixture
def matrix_class_with_2_row_indices_fixture(
    matrix_class_with_init_data_fixture: mtft.ClassWithInitData,
) -> mtft.ClassWith2Randoms:
    """Get a pre-initialized matrix with 2 random row indices."""
    matrix = matrix_class_with_init_data_fixture[0]
    rng = random.Random()

    row_a, row_b = rng.choices(range(matrix.size[1]), k=2)

    return matrix, row_a, row_b


@pytest.fixture(params=[-2.5, -0.01, 0, 0.01, 2.5])
def factor_fixture(request: pytest.FixtureRequest) -> float:
    """Get a factor; relevant edge cases chosen."""
    return request.param
