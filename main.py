from matrix import Matrix

running: bool = True

matrix: Matrix = Matrix([[1.0, 0.0], [0.0, 1.0]], False)

while running:
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
        if choice < 1 or choice > 9:
            print("Choice number out of range! Try again!")
            continue
    except ValueError:
        print("That wasn't a number! Try again!")
        continue

    match choice:
        case 1:
            print("Printing matrix...")

            for row in range(matrix.size[1]):
                print("[", end="  ")
                for col in range(matrix.size[0]):
                    print(matrix.data[col][row], sep="", end="  ")
                if matrix.augmented:
                    print("|", matrix.data[matrix.size[0]][row], "]")
                else:
                    print("]")
        case 2:
            print("Not yet implemented..")
        case 3:
            print("Not yet implemented..")
        case 4:
            print("Not yet implemented..")
        case 5:
            print("Not yet implemented..")
        case 6:
            print("Not yet implemented..")
        case 7:
            print("Not yet implemented..")
        case 8:
            print("Not yet implemented..")
        case 9:
            numsol: int = matrix.gaussian_elimination()

            if not matrix.augmented:
                break

            match numsol:
                case -1:
                    print("Finished! No solutions.")
                case 0:
                    print("Finished! One solution.")
                case _:
                    print(f"Finished! {numsol} free variables.")
