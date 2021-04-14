def counting_sort(A, B):
    C = [0] * 2048

    for j in range(len(A)):
        C[A[j]] += 1

    for i in range(1, 2048):
        C[i] += C[i - 1]

    for j in range(len(A) - 1, -1, -1):
        B[C[A[j]] - 1] = A[j]
        C[A[j]] -= 1


tests = (
    ([], []),
    ([1], [1]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([4, 3, 2, 1], [1, 2, 3, 4]),
    ([1, 1, 2, 1], [1, 1, 1, 2]),
    ([1281, 1, 2], [1, 2, 1281]),
    (
        [995, 334, 709, 999, 502, 303, 274, 488, 997, 568, 546, 756],
        [274, 303, 334, 488, 502, 546, 568, 709, 756, 995, 997, 999],
    ),
    (
        [648, 298, 568, 681, 795, 356, 603, 772, 373, 50, 253, 116],
        [50, 116, 253, 298, 356, 373, 568, 603, 648, 681, 772, 795],
    ),
)

for test, solution in tests:
    student_answer = [0] * len(test)
    counting_sort(test, student_answer)
    if student_answer != solution:
        print(
            "Feilet for testen {:}, resulterte i listen ".format(test)
            + "{:} i stedet for {:}.".format(student_answer, solution)
        )
