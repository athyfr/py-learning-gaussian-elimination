from matrix import Matrix


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

        choice: int
        try:
            choice = int(input("Enter number here: "))
            print("")
            if choice < 1 or choice > 9:
                print("Choice number out of range! Try again!")
                continue
        except ValueError:
            print("")
            print("That wasn't a number! Try again!")
            continue

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

                augmented: bool = False
                while True:
                    try:
                        augmented = bool(
                            input("Is this matrix augmented? (True/False): ")
                        )
                        break
                    except ValueError:
                        print("Invalid entry! Try again!")

                matrix = Matrix(data, augmented)
            case 3:  # Replace matrix cell
                cell_coord: tuple[int, int]

                while True:
                    try:
                        input_str: list[str] = input(
                            "Which cell? (x and y separated by comma): "
                        ).split(",")

                        if len(input_str) != 2:
                            raise ValueError

                        cell_coord = (int(input_str[0]), int(input_str[1]))

                        break
                    except ValueError:
                        print("Invalid entry! Try again!")

                cell_content: float

                while True:
                    try:
                        cell_content = float(
                            input("What should be the new value?: ")
                        )
                        break
                    except ValueError:
                        print("Invalid entry! Try again!")

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
