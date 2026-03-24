import logging

VALIDATE: bool = True

class Matrix:
    """A uniform mathematical matrix.

    Can represent an augmented matrix, or a regular (uniform) matrix.
    In order to create an augmented matrix, there must be one more
    column in the initializer than rows.

    Attributes:
        data: The core matrix data that is operated upon.
        dimensions: The size of the matrix data

    """

    data: list[list[float]]  # outer list is columns.
    size: tuple[int, int]  # Excludes the augmented row if there is one.
    augmented: bool
    _is_rref: bool = False

    def __init__(self, data: list[list[float]], augmented: bool = False):
        """Initializes the matrix with the given matrix data."""

        # ---- Validate
        if VALIDATE:
            # - 1. Type and size check

            # Make sure data is a list (supports duck-typing)
            try:
                data = list(data)
            except ValueError:
                logging.warning("Initializer data is not castable to list")
                raise ValueError("Initializer data is not castable to list")

            # Check dimensions
            dimensions: tuple[int, int] = (len(data), len(data[0]))

            # Loop through columns
            for col in range(dimensions[0]):
                # Make sure columns is list
                try:
                    data[col] = list(data[col])
                except ValueError:
                    logging.warning("Matrix column %s is not castable to list", col)
                    raise ValueError(
                        "Matrix column", col, "is not castable to list"
                    )

                # Make sure column is correct size
                if len(data[col]) != dimensions[1]:
                    logging.warning("Matrix has inconsistent column size")
                    raise ValueError("Matrix has inconsistent column size")

                for cell in range(dimensions[1]):
                    # Make sure cell is correct type
                    try:
                        data[col][cell] = float(data[col][cell])
                    except ValueError:
                        logging.warning("Matrix cell is not castable to float")
                        raise ValueError(
                            "Matrix cell is not castable to float"
                        )

            self.size = (
                dimensions[0] - (1 if augmented else 0),
                dimensions[1],
            )
            self.augmented = augmented

        # --- Load

        self.data = data

    def get_row_length(self) -> int:
        """Gets the row length of the Matrix including any augmented row"""
        return self.size[0] + (1 if self.augmented else 0)

    def add_row(self, row_a: int, row_b: int, factor: float) -> None:
        """Adds row ``row_b`` * ``factor`` to row ``row_a`` (replacing row ``row_a``) in the Matrix

        Performs Elementary Row Operation 1 on row ``row_a``, adding row ``row_b`` with a factor of ``factor``.

        The math expression this represents is as follows:
        .. math::
            $$\\verb|factor| \\cdot R_{\\verb|row_b|} + R_{\\verb|row_a|} \\rightarrow R_{\\verb|row_a|}$$

        Row arguments indicate indices.

        Args:
            row_a: The index of the row to add to, (and change).
            row_b: The index of addend row.
            factor: What to multiply row ``row_b`` by before adding to row ``row_a``.
        """

        for col in range(self.get_row_length()):
            self.data[col][row_a] += self.data[col][row_b] * factor

    def subtract_row(self, row_a: int, row_b: int, factor: float) -> None:
        for col in range(self.get_row_length()):
            self.data[col][row_a] -= self.data[col][row_b] * factor

    def multiply_row(self, row: int, factor: float) -> None:
        """Multiplies row ``row`` by ``factor``.

        Performs Elementary Row Operation 2 on row ``row``, the nonzero scalar being ``factor``.

        ..math::
            $$\\verb|factor| \\cdot R_{\\verb|row|} \\rightarrow R_{\\verb|row|}$$

        Args:

        """

        for col in range(self.get_row_length()):
            self.data[col][row] *= factor

    def divide_row(self, row: int, divisor: float) -> None:
        for col in range(self.get_row_length()):
            self.data[col][row] /= divisor

    def swap_row(self, row_a: int, row_b: int) -> None:
        for col in range(self.get_row_length()):
            row_a_dat: float = self.data[col][row_a]
            self.data[col][row_a] = self.data[col][row_b]
            self.data[col][row_b] = row_a_dat

    def gaussian_elimination(self) -> None:
        """Performs Gaussian Elimination to bring the matrix to RREF."""
        logging.info("Function `gaussian_elimination` called...")
        # -- Forward steps
        active_row: int = 0

        leading_1_x_per_row: list[int] = []

        for active_col in range(self.size[0]):
            logging.info("Performing forward steps on column %s.", active_col)
            # Step 1: Swap out zero entries
            if self.data[active_col][active_row] == 0.0:
                logging.info("This cell is zero! Attempting to swap rows..")
                found_row: int = -1
                # Look for a nonzero below
                for row in range(active_row + 1, self.size[1]):
                    if self.data[active_col][row] != 0:
                        found_row = row
                        break
                if found_row > -1:
                    # Swap, to get a nonzero here
                    self.swap_row(active_row, found_row)
                else:
                    logging.info(f"Giving up on column {active_col}.")
                    # Give up on this column.
                    break

            # Step 2: Normalize
            if self.data[active_col][active_row] != 1:
                logging.info("Normalizing cell...")
                self.divide_row(active_row, self.data[active_col][active_row])

            # Step 3: Eliminate numbers under the active cell
            logging.info("Eliminating zeroes...")
            for row in range(active_row + 1, self.size[1]):
                if self.data[active_col][row] != 0:
                    self.subtract_row(
                        row, active_row, self.data[active_col][row]
                    )

            leading_1_x_per_row.append(active_col)
            active_row += 1

        # -- Backward steps
        for leading_1_y in range(len(leading_1_x_per_row)):
            active_col: int = leading_1_x_per_row[leading_1_y]

            logging.info("Performing backward steps on column %s.", active_col)
            # Eliminate numbers over the active cell
            logging.info("Eliminating zeros...")
            for row in range(leading_1_y):
                if self.data[active_col][row] != 0:
                    self.subtract_row(
                        row, leading_1_y, self.data[active_col][row]
                    )
