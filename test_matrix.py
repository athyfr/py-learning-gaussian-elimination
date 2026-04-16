from matrix import Matrix


def test_init(
    matrix_init_data_fixture: tuple[list[list[float]], bool],
) -> None:
    """Test ``__init__()`` for exceptions, and correct assignments."""
    data, augmented = matrix_init_data_fixture
    matrix = Matrix(matrix_init_data_fixture[0], matrix_init_data_fixture[1])

    assert matrix.data == data
    assert matrix.augmented == augmented
