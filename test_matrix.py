"""Test module for the Matrix class."""
import matrix
import matrix_types_for_tests as mtft


def test_init(
    matrix_init_data_fixture: mtft.MatrixInitData,
) -> None:
    """Test ``__init__()`` for exceptions, and correct assignments."""
    data, augmented = matrix_init_data_fixture

    test_matrix = matrix.Matrix(data, augmented)

    assert test_matrix.data == data
    assert test_matrix.augmented == augmented


def test_get_row_length(
    matrix_class_with_init_data_fixture: mtft.MatrixWithInitData,
) -> None:
    """Test ``get_row_length()`` for incorrect output."""
    test_matrix, (data, augmented) = matrix_class_with_init_data_fixture

    assert test_matrix.get_row_length() == len(data)
