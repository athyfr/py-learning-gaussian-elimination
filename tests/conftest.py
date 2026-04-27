import random

import pytest

import matrix
import matrix_types_for_tests as mtft
from matrix_test_cases import matrices


@pytest.fixture(
    scope="session",
    params=matrices.values(),
    ids=list(matrices.keys()),
)
def matrix_info_fixture(
    request: pytest.FixtureRequest,
) -> mtft.Info:
    """Get initializer data for a Matrix."""
    matrix_dict: dict = request.param
    matrix_dict.setdefault("augmented", False)
    return matrix_dict


@pytest.fixture
def matrix_class_with_info_fixture(
    matrix_info_fixture: mtft.Info,
) -> mtft.ClassWithInfo:
    """Get a pre-initialized Matrix along with init data."""
    inf = matrix_info_fixture.copy()
    return matrix.Matrix(inf["data"], inf["augmented"]), inf


@pytest.fixture
def matrix_class_with_1_row_index_fixture(
    matrix_class_with_info_fixture: mtft.ClassWithInfo,
) -> mtft.ClassWith1Random:
    """Get a pre-initialized matrix with 1 random row index."""
    matrix = matrix_class_with_info_fixture[0]
    rng = random.Random()

    row = rng.choice(range(matrix.size[1]))

    return matrix, row


@pytest.fixture
def matrix_class_with_2_row_indices_fixture(
    matrix_class_with_info_fixture: mtft.ClassWithInfo,
) -> mtft.ClassWith2Randoms:
    """Get a pre-initialized matrix with 2 random row indices."""
    matrix = matrix_class_with_info_fixture[0]
    rng = random.Random()

    row_a, row_b = rng.choices(range(matrix.size[1]), k=2)

    return matrix, row_a, row_b


@pytest.fixture(params=[-2.5, -0.01, 0, 0.01, 2.5])
def factor_fixture(request: pytest.FixtureRequest) -> float:
    """Get a factor; relevant edge cases chosen."""
    return request.param
