"""Test module for the Matrix class."""
from matrix import Matrix


def test_init(
    matrix_init_data_fixture: tuple[list[list[float]], bool],
) -> None:
    """Test ``__init__()`` for exceptions, and correct assignments."""
    data, augmented = matrix_init_data_fixture

    matrix = Matrix(data, augmented)

    assert matrix.data == data
    assert matrix.augmented == augmented
