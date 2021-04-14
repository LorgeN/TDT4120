import random


# De tilfeldig generete testene er like for hver gang du kjører koden.
# Hvis du vil ha andre tilfeldig genererte tester, så endre dette nummeret.
# random.seed(123)

def check_tree(val, node, dna, cache):
    if dna in cache:
        return cache[dna]

    count = val
    for ch in dna:
        if ch not in node:
            break
        node = node[ch]
        count += node['V']

    cache[dna] = count
    return count


def make_tree(dna, segments):
    root, d = {'V': 0}, 0

    for segment in segments:
        if segment not in dna:
            continue

        curr = root
        seg_len = len(segment)
        if seg_len > d:
            d = seg_len

        for ch in segment:
            if ch in curr:
                curr = curr[ch]
            else:
                curr[ch] = curr = {'V': 0}
        curr['V'] += 1
    return root['V'], root, d


def string_match(dna, segments):
    count, n = 0, len(dna)
    val, children, d = make_tree(dna, segments)

    if len(children) == 1:
        return 0

    cache = {}
    n_d = 0 if n < d else n - d
    k = d
    for i in range(n_d):
        count += check_tree(val, children, dna[i:k], cache)
        k += 1
    for i in range(n_d, n):
        count += check_tree(val, children, dna[i:], cache)

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
