def ch_to_int(word, pos):
    if len(word) <= pos:
        return 0
    return ord(word[pos]) - 96


def counting_sort_range(A, start, end, pos):
    B = [None] * (end - start)
    if (end - start) == 1:
        return

    # This might be somewhat faster than using [0] * 26
    C = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for j in range(start, end):
        C[ch_to_int(A[j], pos)] += 1

    for i in range(1, len(C)):
        C[i] += C[i - 1]

    for j in range(len(B) - 1, -1, -1):
        a_j = A[start + j]
        rep = ch_to_int(a_j, pos)
        B[C[rep] - 1] = a_j
        C[rep] -= 1

    for i in range(len(B)):
        A[start + i] = B[i]


def flexradix(A, d):
    return flexradix_range(A, d, 0, 0, len(A))


def flexradix_range(A, d, pos, p, q):
    length = q - p
    if length <= 1:
        return A

    counting_sort_range(A, p, q, pos)
    start = p
    ch_start = A[start][pos]

    for i in range(p, q):
        curr_str = A[i]
        ch_curr = curr_str[pos]

        if not ch_curr == ch_start:
            A = flexradix_range(A, d, pos + 1, start, i)
            start = i
            ch_start = ch_curr

        if len(curr_str) <= (pos + 1):
            tmp = A[start]
            A[start] = curr_str
            A[i] = tmp
            start += 1

    return flexradix_range(A, d, pos + 1, start, q)


tests = (
    (([], 1), []),
    ((["a"], 1), ["a"]),
    ((["a", "b"], 1), ["a", "b"]),
    ((["b", "a"], 1), ["a", "b"]),
    ((["ba", "ab"], 2), ["ab", "ba"]),
    ((["b", "ab"], 2), ["ab", "b"]),
    ((["ab", "a"], 2), ["a", "ab"]),
    ((["abc", "b"], 3), ["abc", "b"]),
    ((["abc", "b"], 4), ["abc", "b"]),
    ((["abc", "b", "bbbb"], 4), ["abc", "b", "bbbb"]),
    ((["abcd", "abcd", "bbbb"], 4), ["abcd", "abcd", "bbbb"]),
    ((["a", "b", "c", "babcbababa"], 10), ["a", "b", "babcbababa", "c"]),
    ((["a", "b", "c", "babcbababa"], 10), ["a", "b", "babcbababa", "c"]),
)

for test, solution in tests:
    student_answer = flexradix(test[0], test[1])
    if student_answer != solution:
        print(
            "Feilet for testen {:}, resulterte i listen ".format(test)
            + "{:} i stedet for {:}.".format(student_answer, solution)
        )
