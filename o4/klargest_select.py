def select_list(A, p, r, k):
    n = r - p
    if n <= 1:
        return A[p:r]

    m = n // 5
    m_5 = m * 5
    B = []
    for b in range(0, m_5, 5):
        B.append(find_median(A, p + b, 5))

    if n % 5 != 0:
        B.append(find_median(A, p + m_5, n % 5))
        m += 1

    pivot = select(B, 0, m - 1, m // 2)

    low_end_index, x_end_index = partition_around(A, p, r, pivot)

    pos_low = low_end_index - p
    pos_hi = x_end_index - p

    if pos_low <= k <= pos_hi:
        return A[(p + k):r]
    elif pos_low > k:
        tmp = A[low_end_index:r]
        return tmp + select_list(A, p, low_end_index, k)
    else:
        return select_list(A, x_end_index, r, k - pos_hi)


def select(A, p, r, k):
    n = r - p
    if n <= 1:
        return A[p]

    m = n // 5
    m_5 = m * 5
    B = []
    for b in range(0, m_5, 5):
        B.append(find_median(A, p + b, 5))

    if n % 5 != 0:
        B.append(find_median(A, p + m_5, n % 5))
        m += 1

    pivot = select(B, 0, m - 1, m // 2)

    low_end_index, x_end_index = partition_around(A, p, r, pivot)

    pos_low = low_end_index - p
    pos_hi = x_end_index - p

    if pos_low <= k <= pos_hi:
        return A[low_end_index]
    elif pos_low > k:
        return select(A, p, low_end_index, k)
    else:
        return select(A, x_end_index, r, k - pos_hi)


def partition_around(A, p, r, x):
    low_end_index, x_end_index = p, p
    for i in range(p, r):
        a = A[i]
        if a == x:
            A[i] = A[x_end_index]
            A[x_end_index] = a
            x_end_index += 1
        elif a < x:
            A[i] = A[x_end_index]
            A[x_end_index] = A[low_end_index]
            A[low_end_index] = a
            low_end_index += 1
            x_end_index += 1

    return low_end_index, x_end_index


def find_median(A, p, n):
    for j in range(p + 1, n):
        key = A[j]

        i = j - 1
        while i > 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key
    return A[p + (n // 2)]


def k_largest(A, k):
    if k == 0:
        return []

    if len(A) <= k:
        return A

    return select_list(A, 0, len(A), len(A) - k)


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
