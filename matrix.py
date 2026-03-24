import logging


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

    def __init__(
        self,
        data: list[list[float]],
        augmented: bool = False,
        reflect_data: bool = False,
    ):
        """Initializes the matrix with the given matrix data."""

        # -- Reflect data (if needed)

        if reflect_data:
            old_data: list[list[float]] = data
            data = [[] for i in range(len(old_data[0]))]

            for row in range(len(old_data)):
                for col in range(len(old_data[0])):
                    data[col].append(old_data[row][col])

        # -- Initialize class variables

        dimensions: tuple[int, int] = (len(data), len(data[0]))

        self.size = (
            dimensions[0] - (1 if augmented else 0),
            dimensions[1],
        )
        self.augmented = augmented

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
        """Subtracts row `row_b` \* `factor` from row `row_a`"""
        for col in range(self.get_row_length()):
            self.data[col][row_a] -= self.data[col][row_b] * factor

    def multiply_row(self, row: int, factor: float) -> None:
        """Multiplies row ``row`` by ``factor``."""

        for col in range(self.get_row_length()):
            self.data[col][row] *= factor

    def divide_row(self, row: int, divisor: float) -> None:
        """Divides row `row` by `divisor`."""
        for col in range(self.get_row_length()):
            self.data[col][row] /= divisor

    def swap_row(self, row_a: int, row_b: int) -> None:
        """Swaps rows ``row_a`` and ``row_b``."""
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

        # -- Remember that this is RREF
        _is_rref = True
