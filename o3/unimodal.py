import random
import sys

# De tilfeldig generete testene er like for hver gang du kjører koden.
# Hvis du vil ha andre tilfeldig genererte tester, så endre dette nummeret.
random.seed(123)


# x er her en unimodal liste
def find_maximum(x):
    return find_maximum_part(x, 0, len(x) - 1, x[0], x[-1], None, None)


def find_maximum_part(x, p, r, x_p, x_r, p_desc, r_desc):
    length = r - p + 1
    if length == 1:
        return x_p

    if length == 2:
        return fmax(x_p, x_r)

    c = (p + r) // 2

    c0 = x[c]
    c1 = x[c + 1]

    c_asc = c0 < c1

    p_desc = p_desc if p_desc is not None else x_p >= x[p + 1]
    r_desc = r_desc if r_desc is not None else x_r >= x[r - 1]

    if p_desc and r_desc:
        return fmax(x_p, x_r)

    if p_desc is r_desc:
        if c_asc:
            return find_maximum_part(x, c + 1, r, c1, x_r, None, r_desc)
        return find_maximum_part(x, p, c, x_p, c0, p_desc, None)

    if not p_desc and not c_asc:
        return fmax(x_r, find_maximum_part(x, p, c, x_p, c0, p_desc, None))

    if not r_desc and c_asc:
        return fmax(x_p, find_maximum_part(x, c + 1, r, c1, x_r, None, r_desc))

    if x_p >= x_r:
        if x_p > c0 or not c_asc:
            return find_maximum_part(x, p, c, x_p, c0, p_desc, None)
        else:
            return find_maximum_part(x, c + 1, r, c1, x_r, None, r_desc)

    if x_r > c0 or c_asc:
        return find_maximum_part(x, c + 1, r, c1, x_r, None, r_desc)
    else:
        return find_maximum_part(x, p, c, x_p, c0, p_desc, None)


def fmax(a, b):
    return a if a >= b else b


# Noen håndskrevne tester
tests = [
    ([1], 1),
    ([1, 3], 3),
    ([3, 1], 3),
    ([1, 2, 1], 2),
    ([1, 0, 2], 2),
    ([2, 0, 1], 2),
    ([0, 2, 1], 2),
    ([0, 1, 2], 2),
    ([2, 1, 0], 2),
    ([2, 3, 1, 0], 3),
    ([2, 3, 4, 1], 4),
    ([2, 1, 3, 4], 4),
    ([4, 2, 1, 3], 4),
]


def generate_random_test_case(length, max_value):
    test = random.sample(range(max_value), k=length)
    m = max(test)
    test.remove(m)
    t = random.randint(0, len(test))
    test = sorted(test[:t]) + [m] + sorted(test[t:], reverse=True)
    t = random.randint(0, len(test))
    test = test[t:] + test[:t]
    return (test, m)


def test_student_maximum(test_case, answer):
    student = find_maximum(test_case)
    if student != answer:
        if len(test_case) < 20:
            response = (
                    "'Find maximum' feilet for følgende input: "
                    + "(x={:}). Din output: {:}. ".format(test_case, student)
                    + "Riktig output: {:}".format(answer)
            )
        else:
            response = (
                    "Find maximum' feilet på input som er "
                    + "for langt til å vises her"
            )
        print(response)
        sys.exit()


# Testing student maximum on custom made tests
for test_case, answer in tests:
    test_student_maximum(test_case, answer)

# Testing student maximum on random test cases
for i in range(40):
    test_case, answer = generate_random_test_case(random.randint(1, 10), 20)
    test_student_maximum(test_case, answer)
