def longest_decreasing_subsequence(s):
    if not s:
        return s

    n = len(s)
    M = [None] * n
    P = [None] * n

    max_len_seq = 1
    M[0] = 0

    for i in range(1, n):
        seq_i = s[i]

        if s[M[max_len_seq - 1]] > seq_i:
            P[i] = M[max_len_seq - 1]
            M[max_len_seq] = i
            max_len_seq += 1
            continue

        lo = 0
        hi = max_len_seq
        while hi - lo > 1:
            mid = (hi + lo) // 2
            if s[M[mid - 1]] > seq_i:
                lo = mid
            else:
                hi = mid

        P[i] = M[lo - 1]

        if seq_i > s[M[lo]]:
            M[lo] = i
            max_len_seq = max(max_len_seq, lo + 1)

    result = [None] * max_len_seq
    pos = M[max_len_seq - 1]
    for i in range(max_len_seq - 1, -1, -1):
        result[i] = s[pos]
        pos = P[pos]

    return result


# Teste på formatet (følge, riktig lengde på svar)
tests = [
    ([1], 1),
    ([1, 2], 1),
    ([1, 2, 3], 1),
    ([2, 1], 2),
    ([3, 2, 1], 3),
    ([1, 3, 2], 2),
    ([3, 1, 2], 2),
    ([1, 1], 1),
    ([1, 2, 1], 2),
    ([8, 7, 3, 6, 2, 6], 4),
    ([10, 4, 2, 1, 7, 5, 3, 2, 1], 6),
    ([3, 7, 2, 10, 3, 3, 3, 9], 2),
]


def verify(sequence, subsequence, optimal_length):
    # Test if the subsequence is actually a subsequence
    index = 0
    for element in sequence:
        if element == subsequence[index]:
            index += 1
            if index == len(subsequence):
                break

    if index < len(subsequence):
        return False, "Svaret er ikke en delfølge av følgen."

    # Test if the subsequence is decreasing
    for index in range(1, len(subsequence)):
        if subsequence[index] >= subsequence[index - 1]:
            return False, "Den gitte delfølgen er ikke synkende."

    # Test if the solution is optimal
    if len(subsequence) != optimal_length:
        return (
            False,
            "Delfølgen har ikke riktig lengde. Riktig lengde er"
            + "{:}, mens delfølgen har lengde ".format(optimal_length)
            + "{:}".format(len(subsequence)),
        )

    return True, ""


failed = False

for test, optimal_length in tests:
    answer = longest_decreasing_subsequence(test[:])
    correct, error_message = verify(test, answer, optimal_length)

    if not correct:
        failed = True
        print(
            'Feilet med feilmeldingen "{:}" for testen '.format(error_message)
            + "{:}. Ditt svar var {:}.".format(test, answer)
        )

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")
