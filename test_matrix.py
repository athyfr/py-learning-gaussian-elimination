"""Test module for the Matrix class."""

import matrix
import matrix_types_for_tests as mtft


def test_init(
    matrix_init_data_fixture: mtft.InitData,
) -> None:
    """Test ``__init__()`` for exceptions, and correct assignments."""
    data, augmented = matrix_init_data_fixture

    test_matrix = matrix.Matrix(data, augmented)

    assert test_matrix.data == data
    assert test_matrix.augmented == augmented


def test_get_row_length(
    matrix_class_with_init_data_fixture: mtft.ClassWithInitData,
) -> None:
    """Test ``get_row_length()`` for incorrect output."""
    test_matrix, (data, _) = matrix_class_with_init_data_fixture

    assert test_matrix.get_row_length() == len(data)


def test_add_row(
    matrix_class_with_2_row_indices_fixture: mtft.ClassWith2Randoms,
    factor_fixture: float,
) -> None:
    """Test ``add_row()``, ensuring the resulting Matrix is correct."""
    test_matrix, row_a, row_b = matrix_class_with_2_row_indices_fixture

    expected_row_a: mtft.Slice = [
        x[row_a] + x[row_b] * factor_fixture for x in test_matrix.data
    ]

    test_matrix.add_row(row_a, row_b, factor_fixture)

    new_row_a: mtft.Slice = [x[row_a] for x in test_matrix.data]

    assert all(
        new_row_a[i] == expected_row_a[i] for i in range(test_matrix.size[0])
    )
