from typing import Any
from collections.abc import Callable

from matrix import Matrix


def cast_input(
    prompt: str,
    in_type: Callable,
    cancel_str: str = "cancel",
    additional_conditions: dict[str, Callable] = {},
    error_message: str = "Invalid entry! Try again!",
) -> Any | None:
    while True:
        try:
            input_str = input(prompt)

            if cancel_str != "" and input_str.lower().find(cancel_str) != -1:
                return None

            input_val = in_type(input_str)

            success: bool = True
            for condition in additional_conditions.keys():
                if not additional_conditions[condition](input_val):
                    print(condition)
                    success = False

            if not success:
                continue

            return input_val
        except ValueError:
            print(error_message)


def cast_input_list(
    prompt: str,
    in_type: Callable,
    num_val: int = -1,
    cancel_str: str = "cancel",
    additional_conditions: dict[str, Callable] = {},
    error_message: str = "Invalid entry! Try again!",
) -> list[Any] | None:
    while True:
        try:
            input_str = input(prompt)

            if cancel_str != "" and input_str.lower().find(cancel_str) != -1:
                return None

            input_str_list: list[str] = input_str.split(",")

            if num_val > -1 and len(input_str_list) != num_val:
                raise ValueError

            input_val: list[Any] = []
            for substr in input_str_list:
                input_val.append(in_type(substr))

            success: bool = True
            for condition in additional_conditions.keys():
                if not additional_conditions[condition](input_val):
                    print(condition)
                    success = False

            if not success:
                continue

            return input_val
        except ValueError:
            print(error_message)


def num_to_str(num: int | float) -> str:
    if num is int:
        return str(num)

    output: str = str(num).removesuffix(".0")

    if output == "-0":
        output = "0"

    return output


def case_check_matrix(given_matrix: Matrix) -> Matrix:
    print("Printing matrix...")

    # - Find each column's width
    num_col: int = given_matrix.get_row_length()
    column_width: list[int] = [0 for i in range(num_col)]

    for col in range(given_matrix.get_row_length()):
        for cell in given_matrix.data[col]:
            column_width[col] = max(
                column_width[col], len(num_to_str(cell))
            )

    # - Print
    for row in range(given_matrix.size[1]):
        print(end="[")
        for col in range(given_matrix.size[0]):
            print(end=" ")
            print(
                num_to_str(given_matrix.data[col][row]).rjust(
                    column_width[col]
                ),
                end=" ",
            )
        if given_matrix.augmented:
            print(
                "|",
                num_to_str(given_matrix.data[given_matrix.size[0]][row]).rjust(
                    column_width[-1]
                ),
                "]",
                sep=" ",
            )
        else:
            print("]")

    return given_matrix


def case_replace_matrix(given_matrix: Matrix) -> Matrix:
    data: list[list[float]]

    #TODO: Modify case to use new Matrix reflect initializer argument.

    num_columns: int | None = cast_input(
        "How many columns does the matrix have?: ", int
    )

    if num_columns is None:
        print("Cancelling operation...")
        return given_matrix

    data = [[] for i in range(num_columns)]

    print()
    print("Enter each element of each row, separated by commas.")
    print("Press enter to start a new row.")
    print("Enter the word 'end' to end the matrix.")

    while True:
        input_str: str = input()

        if input_str.find("end") != -1:
            break

        new_row_str: list[str] = input_str.split(",")

        if len(new_row_str) != num_columns:
            print("Wrong number of values in row! Try again!")
            print("('cancel' to cancel matrix replacement)")
            continue

        new_row: list[float] = []
        failure: bool = False

        for cell in new_row_str:
            try:
                new_row.append(float(cell))
            except ValueError:
                print(
                    "Something entered wasn't castable to float!"
                )
                print("Try again!")
                failure = True
                break

        if failure:
            continue

        for i in range(num_columns):
            data[i].append(new_row[i])

    augmented: bool | None = cast_input(
        "Is this matrix augmented? (True/False): ", bool
    )

    if augmented is None:
        print("Cancelling operation...")
        return given_matrix

    return Matrix(data, augmented)


def case_replace_matrix_cell(given_matrix: Matrix) -> Matrix:
    num_col: int = given_matrix.get_row_length()
    num_row: int = given_matrix.size[1]
    cell_coord: list[int] | None = cast_input_list(
        "Which cell? (x and y separated by comma): ", int, 2, additional_conditions = {
            f"x must be within range (0 - {num_col-1})":
                lambda val: val[0] < 0 or val[0] >= num_col,
            f"y must be within range (0 - {num_row-1})":
                lambda val: val[1] < 0 or val[1] >= num_row
        }
    )

    cell_content: float | None = cast_input(
        "What should be the new value?: ", float
    )

    if cell_coord is None or cell_content is None:
        print("Cancelling replace matrix cell...")
        return given_matrix

    given_matrix.data[cell_coord[0]][cell_coord[1]] = cell_content

    return given_matrix


def case_add_row(given_matrix: Matrix) -> Matrix:
    num_row: int = given_matrix.size[1]

    row_a: int | None = cast_input(
        "Which row will be added to?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val < 0 or val >= num_row
        }
    )

    if row_a is None:
        print("Cancelling operation...")
        return given_matrix

    row_b: int | None = cast_input(
        f"Which row will be added to row {row_a}?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val < 0 or val >= num_row
        }
    )

    if row_b is None:
        print("Cancelling operation...")
        return given_matrix

    factor: float | None = cast_input(
        f"What will row {row_b} be multiplied by before being added to {row_a}?: ",
        float,
    )

    if factor is None:
        print("Cancelling operation...")
        return given_matrix

    given_matrix.add_row(row_a, row_b, factor)

    print(f"Added row {row_b} * {factor} to row {row_a}.")

    return given_matrix


def case_subtract_row(given_matrix: Matrix) -> Matrix:
    num_row: int = given_matrix.size[1]

    row_a: int | None = cast_input(
        "Which row will be subtracted from?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val < 0 or val >= num_row
        }
    )

    if row_a is None:
        print("Cancelling operation...")
        return given_matrix

    row_b: int | None = cast_input(
        f"Which row will be subtracted from row {row_a}?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val >= 0 and val < num_row
        }
    )

    if row_b is None:
        print("Cancelling operation...")
        return given_matrix

    factor: float | None = cast_input(
        f"What will row {row_b} be multiplied by before being subtracted from {row_a}?: ",
        float,
    )

    if factor is None:
        print("Cancelling operation...")
        return given_matrix

    given_matrix.subtract_row(row_a, row_b, factor)

    print(f"Subtracted row {row_b} * {factor} from row {row_a}.")

    return given_matrix


def case_multiply_row(given_matrix: Matrix) -> Matrix:
    num_row: int = given_matrix.size[1]

    print(num_row)

    row: int | None = cast_input(
        "Which row will be multiplied?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val >= 0 and val < num_row
        }
    )

    if row is None:
        print("Cancelling operation...")
        return given_matrix

    factor: float | None = cast_input(
        f"What will row {row} be multiplied by?: ", float
    )

    if factor is None:
        print("Cancelling operation...")
        return given_matrix

    given_matrix.multiply_row(row, factor)

    print(f"Multiplied row {row} by {factor}.")

    return given_matrix


def case_divide_row(given_matrix: Matrix) -> Matrix:
    num_row = given_matrix.size[1]

    row: int | None = cast_input(
        "Which row will be divided?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val >= 0 and val < num_row
        }
    )

    if row is None:
        print("Cancelling operation...")
        return given_matrix

    factor: float | None = cast_input(
        f"What will row {row} be divided by?: ", float
    )

    if factor is None:
        print("Cancelling operation...")
        return given_matrix

    given_matrix.divide_row(row, factor)

    print(f"Divided row {row} by {factor}.")

    return given_matrix


def case_swap_row(given_matrix: Matrix) -> Matrix:
    num_row: int = given_matrix.size[1]

    row_a: int | None = cast_input(
        "What is the first row to be swapped?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val >= 0 and val < num_row
        }
    )

    if row_a is None:
        print("Cancelling operation...")
        return given_matrix

    row_b: int | None = cast_input(
        f"What row will row {row_a} be swapped with?: ", int,
        additional_conditions = {
            f"Row must be within range (0 - {num_row-1})":
                lambda val: val >= 0 and val < num_row
        }
    )

    if row_b is None:
        print("Cancelling operation...")
        return given_matrix

    given_matrix.swap_row(row_a, row_b)

    print(f"Swapped rows {row_a} and {row_b}.")

    return given_matrix


def case_gaussian_elimination(given_matrix: Matrix) -> Matrix:
    given_matrix.gaussian_elimination()

    if not given_matrix.augmented:
        print("Finished!")

        return given_matrix

    print("Finished!")

    return given_matrix


def main():
    running: bool = True

    current_matrix: Matrix = Matrix(
        [
            [1, 2, 1, -1], # Column 1
            [1, 0, 0, -1], # Column 2
            [1, 0, -1, 1], # Column 3
            [1, -1, 0, 1], # Column 4
            [100, 0, 10, 0] # Augmented column
        ],
        augmented=True
    )

    options: dict[str, Callable[[Matrix], Matrix]] = {
        "Check current matrix": case_check_matrix,
        "Replace matrix": case_replace_matrix,
        "Replace matrix cell": case_replace_matrix_cell,
        "Add row": case_add_row,
        "Subtract row": case_subtract_row,
        "Multiply row": case_multiply_row,
        "Divide row": case_divide_row,
        "Swap row": case_swap_row,
        "Gaussian elimination": case_gaussian_elimination
    }
    option_keys: list[str] = list(options.keys())
    option_values: list[Callable[[Matrix], Matrix]] = list(options.values())

    while running:
        print()
        print("What would you like to do?")
        for i in range(len(options)):
            print(f"{i}: {option_keys[i]}")
        print("Cancel: Shut down program")

        choice: int | None = cast_input(
            "Enter number here: ",
            int,
            additional_conditions={
                "\nChoice number out of range! Try again!":
                    lambda val: val >= 0 and val < len(options)
            },
            error_message="\nThat wasn't a number! Try again!",
        )

        print()

        if choice is None:
            print("Goodbye!")
            break

        current_matrix = option_values[choice](current_matrix)


if __name__ == "__main__":
    main()
