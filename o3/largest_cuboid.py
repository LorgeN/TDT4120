import random
import sys

# De tilfeldig generete testene er like for hver gang du kjører koden.
# Hvis du vil ha andre tilfeldig genererte tester, så endre dette nummeret.
random.seed(123)


def largest_cuboid(x):
    checked = dict()
    return partial_cuboid(x, 0, 0, len(x), len(x[0]), checked)


def partial_cuboid(x, row_min, col_min, row_max, col_max, checked, abs_min=None):
    prev = checked.get((row_min, col_min, row_max, col_max))
    if prev:
        return prev

    if row_max == row_min or col_max == col_min:
        checked[(row_min, col_min, row_max, col_max)] = 0
        return 0

    e = (row_max - row_min) * (col_max - col_min)
    if e == 1:
        val = x[row_min][col_min]
        checked[(row_min, col_min, row_max, col_max)] = val
        return val

    m0, m1, min_depth = find_min(x, row_min, col_min, row_max, col_max, abs_min)
    if not abs_min:
        abs_min = min_depth

    a0 = e * min_depth
    a1 = partial_cuboid(x, row_min, col_min, m0, col_max, checked, abs_min=abs_min)
    a2 = partial_cuboid(x, row_min, col_min, row_max, m1, checked, abs_min=abs_min)
    a3 = partial_cuboid(x, m0 + 1, col_min, row_max, col_max, checked, abs_min=abs_min)
    a4 = partial_cuboid(x, row_min, m1 + 1, row_max, col_max, checked, abs_min=abs_min)

    max_a = max(a0, a1, a2, a3, a4)
    checked[(row_min, col_min, row_max, col_max)] = max_a
    return max_a


def find_min(x, row_min, col_min, row_max, col_max, abs_min):
    min_depth = None
    m0, m1 = None, None
    for r in range(row_min, row_max):
        for c in range(col_min, col_max):
            depth = x[r][c]
            if min_depth is None or depth < min_depth:
                if depth == abs_min:
                    return r, c, abs_min

                min_depth = depth
                m0, m1 = r, c
    return m0, m1, min_depth


def a123(x, x0, y0, x1, y1):
    A = float('inf')
    for B in range(x0, x1 + 1):
        for C in range(y0, y1 + 1): A = min(A, x[B][C])
    return A


def bruteforce(x):
    A = 0
    for B in range(len(x)):
        for C in range(len(x[0])):
            for D in range(B, len(x)):
                for E in range(C, len(x[0])): A = max(A, (D - B + 1) * (E - C + 1) * a123(x, B, C, D, E))
    return A


# Some håndskrevne tester
tests = [
    ([[1]], 1),
    ([[1, 1], [2, 1]], 4),
    ([[1, 1], [5, 1]], 5),
    ([[0, 0], [0, 0]], 0),
    ([[10, 0], [0, 10]], 10),
    ([[10, 6], [5, 10]], 20),
    ([[100, 100], [40, 55]], 200),
]


def generate_random_test_case(length, max_value):
    test_case = [
        [random.randint(0, max_value) for i in range(length)]
        for j in range(length)
    ]
    return test_case, bruteforce(test_case)


def test_student_algorithm(test_case, answer):
    student = largest_cuboid(test_case)
    if student != answer:
        if len(test_case) < 4:
            response = "Koden feilet for følgende input: (x={:}).".format(
                test_case
            ) + " Din output: {:}. Riktig output: {:}".format(student, answer)
        else:
            response = "Koden feilet på input som er for langt til å vises her"
        print(response)
        sys.exit()


# Tester funksjonen på håndskrevne tester
for test_case, answer in tests:
    test_student_algorithm(test_case, answer)

# Tester funksjonen på tilfeldig genererte tester
for i in range(20):
    test_case, answer = generate_random_test_case(random.randint(1, 3), 10)
    test_student_algorithm(test_case, answer)
for i in range(10):
    test_case, answer = generate_random_test_case(
        random.randint(1, 20), 100000
    )
    test_student_algorithm(test_case, answer)
