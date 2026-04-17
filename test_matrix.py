"""Test module for the Matrix class."""
import matrix


def test_init(
    matrix_init_data_fixture: tuple[list[list[float]], bool],
) -> None:
    """Test ``__init__()`` for exceptions, and correct assignments."""
    data, augmented = matrix_init_data_fixture

    test_matrix = matrix.Matrix(data, augmented)

    assert test_matrix.data == data
    assert test_matrix.augmented == augmented
