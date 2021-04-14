import random


def select(A, p, r, i):
    if r == p:
        return A[p:]

    q = random_partition(A, p, r)
    k = q - p + 1
    if k == i:
        return A[q:]
    elif k > i:
        return select(A, p, q - 1, i)
    else:
        return select(A, q + 1, r, i - k)


def random_partition(A, p, r):
    index = random.randint(p, r)
    x = A[index]
    A[index], A[r] = A[r], x
    j = p - 1
    for i in range(p, r):
        a = A[i]
        if a <= x:
            j += 1
            A[i], A[j] = A[j], a
    j += 1
    A[j], A[r] = A[r], A[j]
    return j


def k_largest(A, k):
    if k == 0:
        return []

    n = len(A)
    if n <= k:
        return A

    return select(A, 0, n - 1, n - k + 1)


# Sett med tester.
tests = [
    (([], 0), []),
    (([1], 0), []),
    (([1], 1), [1]),
    (([1, 2], 1), [2]),
    (([-1, -2], 1), [-1]),
    (([-1, -2, 3], 2), [-1, 3]),
    (([1, 2, 3], 2), [2, 3]),
    (([3, 2, 1], 2), [2, 3]),
    (([3, 3, 3, 3], 2), [3, 3]),
    (([4, 1, 3, 2, 3], 2), [3, 4]),
    (([4, 5, 1, 3, 2, 3], 4), [3, 3, 4, 5]),
    (([9, 3, 6, 1, 7, 3, 4, 5], 4), [5, 6, 7, 9]),
]

for test, solution in tests:
    student_answer = k_largest(*test)
    if type(student_answer) != list:
        print("Metoden må returnere en liste")
    else:
        student_answer.sort()
        if student_answer != solution:
            print(
                "Feilet for testen {:}, resulterte i listen ".format(test)
                + "{:} i stedet for {:}.".format(student_answer, solution)
            )
