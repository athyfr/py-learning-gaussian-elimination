import pytest

from matrix import Matrix


@pytest.fixture(
    scope="module",
    params=[
        (
            [
                [1, 2, 1, -1],  # Column 1
                [1, 0, 0, -1],  # Column 2
                [1, 0, -1, 1],  # Column 3
                [1, -1, 0, 1],  # Column 4
                [100, 0, 10, 0],  # Augmented column
            ],
            True,
        ),
    ],
)
def matrix_data_fixture(
    request: pytest.FixtureRequest,
) -> tuple[list[list[float]], bool]:
    """Gets arbitrary (parametrized) matrix init data."""
    return request.param


@pytest.fixture
def matrix_fixture(
    matrix_data: tuple[list[list[float]], bool],
) -> tuple[Matrix, list[list[float]], bool]:
    """Get an arbitrary (parametrized) ``Matrix``."""
    return (
        Matrix(matrix_data[0], matrix_data[1]),
        matrix_data[0],
        matrix_data[1],
    )


def test_init_data(
    matrix_fixture: tuple[Matrix, list[list[float]], bool],
) -> None:
    """Test ``__init__`` to ensure data is passed along."""
    matrix, data, augmented = matrix_fixture

    assert matrix.data == data
    assert matrix.augmented == augmented
    assert matrix.size[0] == len(data)
    assert matrix.size[1] == len(data[0]) - (1 if augmented else 0)
