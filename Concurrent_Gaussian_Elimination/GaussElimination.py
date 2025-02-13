from decimal import Decimal, getcontext, InvalidOperation, ROUND_HALF_EVEN
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

getcontext().prec = 20


def read_file(file_name):
    with open(file_name, "r") as file:
        size = int(file.readline())
        matrix = [[Decimal(0) for _ in range(size + 2)] for _ in range(size + 1)]
        for i in range(1, size + 1):
            row = file.readline().split()
            for j in range(1, size + 1):
                matrix[i][j] = Decimal(row[j - 1])
        last_row = file.readline().split()
        for i in range(1, size + 1):
            matrix[i][size + 1] = Decimal(last_row[i - 1])
    return size, matrix


def read_result(file_name):
    with open(file_name, "r") as file:
        size = int(file.readline())
        for i in range(size):
            file.readline()
        result = file.readline().split()
    return [Decimal(x) for x in result]


def save_single_solved(matrix, size):
    with open("solved.txt", "w") as file:
        file.write(str(size) + "\n")
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                file.write(str(float(quantize_decimal(abs(matrix[i][j])))) + " ")
            file.write("\n")
        for i in range(1, size + 1):
            file.write(str(float(quantize_decimal(matrix[i][size + 1]))) + " ")
    return


def read_test(number, TESTS_FILE_PATH="tests/"):
    with open(TESTS_FILE_PATH + "test" + str(number) + ".txt", "r") as file:
        size = int(file.readline())
        matrix = [[Decimal(0) for _ in range(size + 2)] for _ in range(size + 1)]
        for i in range(1, size + 1):
            row = file.readline().split()
            for j in range(1, size + 1):
                matrix[i][j] = Decimal(row[j - 1])
        last_row = file.readline().split()
        for i in range(1, size + 1):
            matrix[i][size + 1] = Decimal(last_row[i - 1])
    return size, matrix


def read_test_result(number, TESTS_FILE_PATH="tests/"):
    with open(TESTS_FILE_PATH + "out" + str(number) + ".txt", "r") as file:
        size = int(file.readline())
        for i in range(size):
            file.readline()
        result = file.readline().split()
    return [Decimal(x) for x in result]


def save_solved(number, matrix, size, RESULTS_FILE_PATH="results/"):
    with open(RESULTS_FILE_PATH + "solved" + str(number) + ".txt", "w") as file:
        file.write(str(size) + "\n")
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                file.write(str(float(quantize_decimal(abs(matrix[i][j])))) + " ")
            file.write("\n")
        for i in range(1, size + 1):
            file.write(str(float(quantize_decimal(matrix[i][size + 1]))) + " ")
    return


def draw_diekert(size):
    edges_string = ""
    nodes_string = ""
    nodes = []
    edges = []

    # nodes
    for i in range(1, size):
        for k in range(i + 1, size + 1):
            label = "A{i=" + str(i) + ", k=" + str(k) + "}"
            nodes.append(label)
            for j in range(i, size + 2):
                label = "B{i=" + str(i) + ", j=" + str(j) + ", k=" + str(k) + "}"
                nodes.append(label)
                label = "C{i=" + str(i) + ", j=" + str(j) + ", k=" + str(k) + "}"
                nodes.append(label)

    for i in range(len(nodes)):
        nodes_string += str(i) + "[label=\"" + nodes[i] + "\"]\n"

    # edges
    for i in range(1, size):
        for k in range(i + 1, size + 1):
            for j in range(i, size + 2):
                label1 = "A{i=" + str(i) + ", k=" + str(k) + "}"
                label2 = "B{i=" + str(i) + ", j=" + str(j) + ", k=" + str(k) + "}"
                edges.append((label1, label2))
                label1 = "B{i=" + str(i) + ", j=" + str(j) + ", k=" + str(k) + "}"
                label2 = "C{i=" + str(i) + ", j=" + str(j) + ", k=" + str(k) + "}"
                edges.append((label1, label2))
    for i in range(1, size - 1):
        for k in range(i + 2, size + 1):
            label1 = "C{i=" + str(i) + ", j=" + str(i + 1) + ", k=" + str(i + 1) + "}"
            label2 = "A{i=" + str(i + 1) + ", k=" + str(k) + "}"
            edges.append((label1, label2))
            label1 = "C{i=" + str(i) + ", j=" + str(i + 1) + ", k=" + str(k) + "}"
            label2 = "A{i=" + str(i + 1) + ", k=" + str(k) + "}"
            edges.append((label1, label2))
            for j in range(i + 2, size + 2):
                label1 = "C{i=" + str(i) + ", j=" + str(j) + ", k=" + str(i + 1) + "}"
                label2 = "B{i=" + str(i + 1) + ", j=" + str(j) + ", k=" + str(k) + "}"
                edges.append((label1, label2))
                label1 = "C{i=" + str(i) + ", j=" + str(j) + ", k=" + str(k) + "}"
                label2 = "C{i=" + str(i + 1) + ", j=" + str(j) + ", k=" + str(k) + "}"
                edges.append((label1, label2))

    for edge in edges:
        edges_string += str(nodes.index(edge[0])) + " -> " + str(nodes.index(edge[1])) + "\n"

    # save to file
    with open("graph.dot", "w") as file:
        file.write("digraph g{\n")
        file.write(edges_string + '\n')
        file.write(nodes_string + '\n')
        file.write("}")

    # generate .png with graphviz app
    subprocess.run(["dot", "-Tpng", "graph.dot", "-o", "graph.png"])


def quantize_decimal(value, decimal_places=8):
    try:
        return value.quantize(Decimal(f'1e-{decimal_places}'), rounding=ROUND_HALF_EVEN)
    except InvalidOperation:
        return value


def compare(solution, result):
    size = len(solution)
    decimal_places = 8
    for i in range(size):
        try:
            if not quantize_decimal(solution[i], decimal_places) == quantize_decimal(result[i], decimal_places):
                return False
        except InvalidOperation:
            return False
    return True


def A(matrix, i, k, m):
    m[k][i] = matrix[k][i] / matrix[i][i]
    return


def B(matrix, i, j, k, m, n):
    n[i][j][k] = matrix[i][j] * m[k][i]
    return


def C(matrix, i, j, k, n):
    matrix[k][j] -= n[i][j][k]
    return


def normalise_matrix(matrix, size):
    for i in range(1, size + 1):
        diag = matrix[i][i]
        for j in range(i, size + 2):
            matrix[i][j] /= diag
    return matrix


def solve(size, matrix):
    m = [[Decimal(0) for _ in range(size + 1)] for _ in range(size + 1)]
    n = [[[Decimal(0) for _ in range(size + 1)] for _ in range(size + 2)] for _ in range(size + 1)]

    with ThreadPoolExecutor() as executor:
        futures = []

        for i in range(1, size + 1):
            for k in range(i + 1, size + 1):
                futures.append(executor.submit(A, matrix, i, k, m))
                for j in range(i, size + 2):
                    futures.append(executor.submit(B, matrix, i, j, k, m, n))
                    futures.append(executor.submit(C, matrix, i, j, k, n))

        for future in as_completed(futures):
            future.result()

        matrix = normalise_matrix(matrix, size)

        futures.clear()

        for i in range(size, 0, -1):
            for k in range(i):
                futures.append(executor.submit(A, matrix, i, k, m))
                for j in range(i, size + 2):
                    futures.append(executor.submit(B, matrix, i, j, k, m, n))
                    futures.append(executor.submit(C, matrix, i, j, k, n))

        for future in as_completed(futures):
            future.result()

    return matrix


def given_tests():
    passed_counter = 0
    for i in range(2):
        size, test_matrix = read_test(i, "TaskTests/")
        solved = read_test_result(i, "TaskTests/")
        my_solution = solve(size, test_matrix)
        save_solved(i, my_solution, size, "TaskTests/")
        solution_vector = [quantize_decimal(my_solution[row][size + 1]) for row in range(1, size + 1)]
        solved_vector = [quantize_decimal(solved[row]) for row in range(size)]
        if compare(solution_vector, solved_vector):
            passed_counter += 1
            print("Test", i, "passed")
        else:
            print("Test", i, "failed")
    print("Passed", passed_counter, "out of 2 tests.")


def test(last_test_number):
    passed_counter = 0
    for i in range(last_test_number + 1):
        size, test_matrix = read_test(i)
        solved = read_test_result(i)
        my_solution = solve(size, test_matrix)
        save_solved(i, my_solution, size)
        solution_vector = [quantize_decimal(my_solution[row][size + 1]) for row in range(1, size + 1)]
        solved_vector = [quantize_decimal(solved[row]) for row in range(size)]
        if compare(solution_vector, solved_vector):
            passed_counter += 1
            print("Test", i, "passed")
        else:
            print("Test", i, "failed")
    print("Passed", passed_counter, "out of", last_test_number + 1, "tests.")


def run():
    print("Hello! This is a program that shows application of trace theory to thread scheduling concurrent Gaussian elimination.")
    print("Select option that you want to run:")
    print("0 - run 2 tests given with the task.")
    print("1 - run 16 tests generated by the checking program.")
    print("2 - run the program with a custom created matrix saved in .txt format to calculate it.")
    print("3 - run the program with a custom created matrix and result saved both in .txt format to calculate and compare it with the given result.")
    print("4 - generate Diekert graph for the given size of matrix.")
    choice = input()
    if choice == "0":
        given_tests()
    elif choice == "1":
        test(15)
    elif choice == "2":
        print("Please provide the name of the .txt file with the matrix. (for example 'matrix.txt')")
        file_name = input()
        size, matrix = read_file(file_name)
        my_solution = solve(size, matrix)
        save_single_solved(my_solution, size)
        print("The solution has been saved in the file 'solved.txt'.")
    elif choice == "3":
        print("Please provide the name of the .txt file with the matrix. (for example 'matrix.txt')")
        file_name = input()
        print("Please provide the name of the .txt file with the result. (for example 'result.txt')")
        result_name = input()
        size, matrix = read_file(file_name)
        solved = read_result(result_name)
        my_solution = solve(size, matrix)
        solution_vector = [quantize_decimal(my_solution[row][size + 1]) for row in range(1, size + 1)]
        solved_vector = [quantize_decimal(solved[row]) for row in range(size)]
        if compare(solution_vector, solved_vector):
            print("Test passed")
        else:
            print("Test failed")
        save_single_solved(my_solution, size)
        print("The calculated solution has been saved in the file 'solved.txt'.")
    elif choice == "4":
        print("Please provide the size of the matrix.")
        size = int(input())
        draw_diekert(size)
    else:
        print("Invalid choice. Please provide a number from 0 to 4.")


run()
