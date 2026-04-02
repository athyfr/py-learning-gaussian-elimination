import pytest

from matrix import Matrix


# --- UTILITIES ---


def duplicate_by_integers[_T](items: list[_T], integers: list[int]):
    output: list[_T] = []
    for i in range(len(items)):
        output += [items[i] for x in range(integers[i])]
    return output


# --- FIXTURES ---


matrices: list[list[list[float]]] = [
    [
        [  1,  2,  1, -1],  # Column 1
        [  1,  0,  0, -1],  # Column 2
        [  1,  0, -1,  1],  # Column 3
        [  1, -1,  0,  1],  # Column 4
        [100,  0, 10,  0],  # Augmented column
    ],
]

matrices_augmented: list[bool] = [
    True,
]

matrices_width: list[int] = [len(m[0]) for m in matrices]

matrices_height: list[int] = [len(m) for m in matrices]

matrices_per_row: list[list[list[float]]]


@pytest.fixture(
    scope="session",
    params=zip(matrices, matrices_augmented, strict=True),
)
def matrix_data_fixture(
    request: pytest.FixtureRequest,
) -> tuple[list[list[float]], bool]:
    """Gets arbitrary (parametrized) matrix init data."""
    return request.param


@pytest.fixture
def matrix_fixture(
    matrix_data_fixture: tuple[list[list[float]], bool],
) -> tuple[Matrix, list[list[float]], bool]:
    """Get an arbitrary (parametrized) ``Matrix``."""
    data, augmented = matrix_data_fixture

    return (
        Matrix(data, augmented),
        data,
        augmented,
    )


@pytest.fixture(
    scope="session",
    params=zip(
        duplicate_by_integers(matrices, matrices_height),
        duplicate_by_integers(matrices_augmented, matrices_height),
        itertools.chain.from_iterable([range(x) for x in matrices_height]),
        strict=True,
    ),
)
def matrix_data_with_row_fixture(
    request: pytest.FixtureRequest,
) -> tuple[list[list[float]], bool, int]:
    """Get an arbitrary (parametrized) ``Matrix``, along with a row index."""
    return request.param


@pytest.fixture
def matrix_with_row_fixture(
    matrix_data_with_row_fixture: tuple[list[list[float]], bool, int],
) -> tuple[Matrix, list[list[float]], bool, int]:
    """Get an arbitrary (parametrized) ``Matrix``, along with a row index."""
    data, augmented, row = matrix_data_with_row_fixture

    return (
        Matrix(data, augmented),
        data,
        augmented,
        row,
    )


# --- TESTS ---


def test_init_data(
    matrix_fixture: tuple[Matrix, list[list[float]], bool],
) -> None:
    """Test ``__init__`` to ensure data is passed along."""
    matrix, data, augmented = matrix_fixture

    assert matrix.data == data
    assert matrix.augmented == augmented
    assert matrix.size[0] == len(data)
    assert matrix.size[1] == len(data[0]) - (1 if augmented else 0)
