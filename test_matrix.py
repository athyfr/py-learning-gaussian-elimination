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
def matrix_data(
    request: pytest.FixtureRequest,
) -> tuple[list[list[float]], bool]:
    """Gets arbitrary (parametrized) matrix init data."""
    return request.param


@pytest.fixture
def matrix(matrix_data: tuple[list[list[float]], bool]) -> Matrix:
    """Get an arbitrary (parametrized) ``Matrix``."""
    return Matrix(matrix_data[0], matrix_data[1])


def test_matrix_init(matrix_data: tuple[list[list[float]], bool]) -> None:
    """Tests whether ``Matrix.__init__()`` properly initializes data."""
    data, augmented = matrix_data

    matrix = Matrix(data, augmented)

    assert matrix.data == data
    assert matrix.augmented == augmented
    assert matrix.size[0] == len(data)
    assert matrix.size[1] == len(data[0]) - (1 if augmented else 0)
