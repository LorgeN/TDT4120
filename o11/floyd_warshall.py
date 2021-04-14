from operator import add, mul
from copy import deepcopy


def general_floyd_warshall(D, f, g):
    n = len(D)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                D[i][j] = f(D[i][j], g(D[i][k], D[k][j]))


def transitive_closure(T, general_floyd_warshall):
    # Velg funksjoner til Floyd-Warshall
    def f(x, y):
        return x or y

    def g(x, y):
        return x and y

    general_floyd_warshall(T, f, g)


tests = [
    (
        [
            [1, 1, float("inf")],
            [float("inf"), 1, 1],
            [1, float("inf"), 1],
        ],
        min,
        add,
        [[1, 1, 2], [2, 1, 1], [1, 2, 1]],
    ),
    (
        [
            [0, 3, 8, float("inf"), -4],
            [float("inf"), 0, float("inf"), 1, 7],
            [float("inf"), 4, 0, float("inf"), float("inf")],
            [2, float("inf"), -5, 0, float("inf")],
            [float("inf"), float("inf"), float("inf"), 6, 0],
        ],
        min,
        add,
        [
            [0, 1, -3, 2, -4],
            [3, 0, -4, 1, -1],
            [7, 4, 0, 5, 3],
            [2, -1, -5, 0, -2],
            [8, 5, 1, 6, 0],
        ],
    ),
    (
        [
            [1, 3, 8, 3, 4],
            [3, 1, 4, 2, 7],
            [2, 4, 1, 7, 1],
            [2, 2, 5, 1, 7],
            [3, 9, 2, 6, 1],
        ],
        min,
        mul,
        [
            [1, 3, 8, 3, 4],
            [3, 1, 4, 2, 4],
            [2, 4, 1, 6, 1],
            [2, 2, 5, 1, 5],
            [3, 8, 2, 6, 1],
        ],
    ),
]


def generate_feedback(test, f, g, answer, expected):
    feedback = ""
    feedback += "Koden din gir feil svar på input\n"
    feedback += str(test)
    feedback += f"\nmed f={f.__name__} og g={g.__name__}.\n"
    feedback += "Ditt svar var\n"
    feedback += str(student)
    feedback += ",\nmen forventet resultat er\n"
    feedback += str(expected)
    return feedback


for test, f, g, expected in tests:
    student = deepcopy(test)
    general_floyd_warshall(student, f, g)
    n = len(expected)
    assert (
            len(student) == n
    ), "Svaret ditt har ikke samme dimensjoner som input"
    for row in range(n):
        for col in range(n):
            assert student[row][col] == expected[row][col], generate_feedback(
                test, f, g, student, expected
            )

print("Koden din passerte alle testene.")
