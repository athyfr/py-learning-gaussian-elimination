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
                if additional_conditions[condition]:
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


def main():
    running: bool = True

    matrix: Matrix = Matrix([[1.0, 0.0], [0.0, 1.0]], False)

    while running:
        print("")
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
                "\nChoice number out of range! Try again!": lambda val: val
                <= 0
                or val > 9
            },
            error_message="\nThat wasn't a number! Try again!",
        )
        
        if choice is None:
            print("Goodbye!")
            break

        match choice:
            case 1:  # Check current matrix
                print("Printing matrix...")

                for row in range(matrix.size[1]):
                    print("[", end="  ")
                    for col in range(matrix.size[0]):
                        print(matrix.data[col][row], sep="", end="  ")
                    if matrix.augmented:
                        print(
                            "|",
                            matrix.data[matrix.size[0]][row],
                            "]",
                            sep="  ",
                        )
                    else:
                        print("]")
            case 2:  # Replace matrix
                data: list[list[float]] = []

                print("Enter each element of each row, separated by commas.")
                print("Press enter to start a new row.")
                print("Enter the word 'end' to end the matrix.")

                while True:
                    input_str: str = input()

                    if input_str.find("end") != -1:
                        break

                    new_row_str: list[str] = input_str.split(",")
                    new_row: list[float] = []

                    for cell in new_row_str:
                        try:
                            new_row.append(float(cell))
                        except ValueError:
                            print(
                                "Something entered wasn't castable to float!"
                            )
                            print("Try again!")
                            continue

                    data.append(new_row)

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
                    print("Cancelling replace matrix cell..")
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
