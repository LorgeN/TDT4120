import functools
import random


# De tilfeldig generete testene er like for hver gang du kjører koden.
# Hvis du vil ha andre tilfeldig genererte tester, så endre dette nummeret.
# random.seed(123)

@functools.lru_cache(maxsize=None)
def occurrences(string, sub):
    count = start = 0
    look = string.find
    while True:
        start = look(sub, start) + 1
        if start > 0:
            count += 1
        else:
            return count


def string_match(dna, segments):
    count = 0
    for segment in segments:
        count += occurrences(dna, segment)
    return count


def naive_count(dna, segments):
    counter = 0
    for segment in segments:
        for i in range(len(dna) - len(segment) + 1):
            if dna[i: i + len(segment)] == segment:
                counter += 1
    return counter


class Node:
    def __init__(self):
        self.children = {}
        self.count = 0

    def __str__(self):
        return (
                f"{{count: {self.count}, children: {{"
                + ", ".join(
            [f"'{c}': {node}" for c, node in self.children.items()]
        )
                + "}"
        )


def generate_match_tests():
    # Custom made match tests
    tests = [
        (("A", []), 0),
        (("AAAA", ["A"]), 4),
        (("ACTTACTGG", ["A", "ACT", "GG"]), 5),
        ((20 * "A", ["A"]), 20),
        ((20 * "A", ["AA"]), 19),
        ((20 * "A", ["A", "A"]), 40),
        ((20 * "A", ["A", "AA"]), 39),
        ((10 * "AB", ["AB"]), 10),
        ((10 * "AB", ["A", "AB"]), 20),
        ((10 * "AB", ["A", "B"]), 20),
    ]
    for test in tests:
        yield test

    # Some small random rests
    for i in range(2000):
        d = "".join(
            random.choices(["A", "G", "T", "C"], k=random.randint(0, 200))
        )
        e = [
            "".join(
                random.choices(["A", "G", "T", "C"], k=random.randint(1, 20))
            )
            for i in range(random.randint(0, 200))
        ]
        answer = naive_count(d, e)
        yield ((d, e), answer)


for test_case, answer in generate_match_tests():
    dna, segments = test_case
    student = string_match(dna, segments)
    if student != answer:
        print(
            "Input: (dna={:}, segments={:}) ".format(dna, segments)
            + "Ditt svar: {:} Riktig: {:}".format(student, answer)
        )
        break
