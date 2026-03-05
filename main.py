from typing import Any, Callable

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
                if additional_conditions[condition](input_val):
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


def main():
    running: bool = True

    matrix: Matrix = Matrix(
        [
            [1, 2, 1, -1], # Column 1
            [1, 0, 0, -1], # Column 2
            [1, 0, -1, 1], # Column 3
            [1, -1, 0, 1], # Column 4
            [100, 0, 10, 0] # Augmented column
        ],
        augmented=True
    )

    while running:
        print()
        print("What would you like to do?")
        print("1: Check current matrix")
        print("2: Replace matrix")
        print("3: Replace matrix cell")
        print("4: Add row")
        print("5: Subtract row")
        print("6: Multiply row")
        print("7: Divide row")
        print("8: Swap row")
        print("9: Gaussian elimination")
        print("Cancel: Shut down program")

        choice: int | None = cast_input(
            "Enter number here: ",
            int,
            additional_conditions={
                "\nChoice number out of range! Try again!":
                    lambda val: val <= 0 or val > 9
            },
            error_message="\nThat wasn't a number! Try again!",
        )

        print()

        if choice is None:
            print("Goodbye!")
            break

        match choice:
            case 1:  # Check current matrix
                print("Printing matrix...")

                # - Find each column's width
                num_col: int = matrix._get_row_length()
                column_width: list[int] = [0 for i in range(num_col)]

                for col in range(matrix._get_row_length()):
                    for cell in matrix.data[col]:
                        column_width[col] = max(
                            column_width[col], len(num_to_str(cell))
                        )

                # - Print
                for row in range(matrix.size[1]):
                    print(end="[")
                    for col in range(matrix.size[0]):
                        print(end=" ")
                        print(
                            num_to_str(matrix.data[col][row]).rjust(
                                column_width[col]
                            ),
                            end=" ",
                        )
                    if matrix.augmented:
                        print(
                            "|",
                            num_to_str(matrix.data[matrix.size[0]][row]).rjust(
                                column_width[-1]
                            ),
                            "]",
                            sep=" ",
                        )
                    else:
                        print("]")
            case 2:  # Replace matrix
                data: list[list[float]]

                num_columns: int | None = cast_input(
                    "How many columns does the matrix have?: ", int
                )

                if num_columns is None:
                    print("Cancelling replace matrix...")
                    continue

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
                    print("Cancelling matrix replacement.")
                    continue

                matrix = Matrix(data, augmented)
            case 3:  # Replace matrix cell
                cell_coord: list[int] | None = cast_input_list(
                    "Which cell? (x and y separated by comma): ", int, 2
                )

                cell_content: float | None = cast_input(
                    "What should be the new value?: ", float
                )

                if cell_coord is None or cell_content is None:
                    print("Cancelling replace matrix cell...")
                    continue

                matrix.data[cell_coord[0]][cell_coord[1]] = cell_content

            case 4:  # Add row
                print("Not yet implemented..")
            case 5:  # Subtract row
                print("Not yet implemented..")
            case 6:  # Multiply row
                print("Not yet implemented..")
            case 7:  # Divide row
                print("Not yet implemented..")
            case 8:  # Swap row
                print("Not yet implemented..")
            case 9:  # Gaussian elimination
                free_vars: int = matrix.gaussian_elimination()

                if not matrix.augmented:
                    continue

                match free_vars:
                    case -1:
                        print("Finished! There are no solutions.")
                    case 0:
                        print("Finished! There is one solution.")
                    case _:
                        print(
                            f"Finished! There are {free_vars} free variables."
                        )


if __name__ == "__main__":
    main()
