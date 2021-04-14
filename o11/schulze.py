from functools import cmp_to_key, lru_cache
from copy import deepcopy


def schulze_method(A):
    c = len(A)
    itr = list(range(c))
    if c <= 1:
        return itr

    for i in itr:
        a_i = A[i]
        for j in itr:
            if i is not j and a_i[j] <= A[j][i]:
                a_i[j] = 0

    for i in itr:
        a_i = A[i]
        for j in itr:
            a_j = A[j]
            if i is not j:
                for k in itr:
                    a_j[k] = max(a_j[k], min(a_j[i], a_i[k]))

    def comparison(x, y):
        return A[x][y] - A[y][x]

    return sorted(itr, key=cmp_to_key(comparison), reverse=True)


@lru_cache(maxsize=None)
def max(a, b):
    return a if a >= b else b


@lru_cache(maxsize=None)
def min(a, b):
    return a if a <= b else b


tests = [
    ([[0]], [0]),
    ([[0, 1], [3, 0]], [1, 0]),
    (
        [
            [0, 4, 1, 5, 5],
            [2, 0, 2, 8, 3],
            [4, 2, 0, 8, 3],
            [6, 2, 5, 0, 2],
            [11, 4, 2, 1, 0],
        ],
        [2, 4, 1, 3, 0],
    ),
    (
        [
            [0, 2, 5, 4, 3],
            [7, 0, 7, 5, 5],
            [4, 2, 0, 6, 2],
            [5, 4, 3, 0, 5],
            [6, 4, 7, 4, 0],
        ],
        [1, 4, 0, 2, 3],
    ),
    (
        [
            [0, 20, 26, 30, 22],
            [25, 0, 16, 33, 18],
            [19, 29, 0, 17, 24],
            [15, 12, 28, 0, 14],
            [23, 27, 21, 31, 0],
        ],
        [4, 0, 2, 1, 3],
    ),
]


def generate_feedback(test, expected, student):
    feedback = ""
    feedback += "Koden din feilet for input\n"
    feedback += str(test) + "\n"
    feedback += "Ditt svar er\n"
    feedback += str(student) + ",\n"
    feedback += "men riktig svar er\n"
    feedback += str(expected) + "."
    return feedback


for test, expected in tests:
    unchanged_input = deepcopy(test)
    student = schulze_method(test)
    n = len(unchanged_input)
    assert (
            len(student) == n
    ), "Listen din inneholder ikke riktig antall kandidater"
    for i in range(n):
        assert student[i] == expected[i], generate_feedback(
            unchanged_input, expected, student
        )

print("Koden din passerte alle testene.")
