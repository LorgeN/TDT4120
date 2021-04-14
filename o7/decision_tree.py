from heapq import heappush, heappop, heapify


def build_decision_tree(decisions):
    decisions = [(dec[1], dec[0], None, None) for dec in decisions]
    heapify(decisions)
    n = len(decisions)

    for i in range(n - 1):
        left = heappop(decisions)
        right = heappop(decisions)
        freq = left[0] + right[0]
        heappush(decisions, (freq, left[1] + right[1], left, right))

    res = {}
    encoding_part("", res, heappop(decisions))
    return res


def encoding_part(prefix, res, node):
    if node[2] or node[3]:
        encoding_part(prefix + "0", res, node[2])
        encoding_part(prefix + "1", res, node[3])
        return

    res[node[1]] = prefix


def test_expected(root, decisions, functions):
    expectance = 0
    for name, prob in decisions:
        questions = 0
        node = root
        while isinstance(node, TestNode):
            questions += 1
            if functions[node.function](name):
                node = node.true
            else:
                node = node.false
        expectance += prob * questions
    return expectance


def build_decision_tree_highscore(decisions, tests):
    n = len(decisions)
    functions = tests
    tests = list(enumerate(tests))
    p, r = 0, n

    best_tree = None
    for i, test in tests:
        test_copy = tests[:]
        test_copy.remove((i, test))

        start_false = partition_on_test(decisions, p, r, test)
        # Find a test with different results for values
        if (not start_false) or start_false == r:
            continue

        root = TestNode(i)
        root.true = build_partial_tree_recursive(decisions, p, start_false, test_copy[:])
        root.false = build_partial_tree_recursive(decisions, start_false, r, test_copy)
        best_tree = root if not best_tree else min(best_tree, root,
                                                   key=lambda tree: test_expected(tree, decisions, functions))
    return best_tree


def build_partial_tree_recursive(decisions, p, r, tests):
    if (r - p) <= 1:
        return LeafNode(decisions[p][0])

    dec_tot = sum(dec[1] for dec in decisions[p:r])
    sort_order = lambda t: abs(sum(t[1](name) * freq for name, freq in decisions[p:r]) / dec_tot - 0.5)
    tests.sort(key=sort_order)

    i, test = tests.pop(0)
    start_false = partition_on_test(decisions, p, r, test)
    # Find a test with different results for values
    if (not start_false) or start_false == r:
        return build_partial_tree_recursive(decisions, p, r, tests)

    root = TestNode(i)
    root.true = build_partial_tree_recursive(decisions, p, start_false, tests[:])
    root.false = build_partial_tree_recursive(decisions, start_false, r, tests)
    return root


def partition_on_test(decisions, p, r, test):
    i = p
    for j in range(p, r):
        if test(decisions[j][0]):
            decisions[i], decisions[j] = decisions[j], decisions[i]
            i += 1
    return i


tests = [
    ([("a", 0.5), ("b", 0.5)], 1),
    ([("a", 0.99), ("b", 0.01)], 1),
    ([("a", 0.5), ("b", 0.25), ("c", 0.25)], 1.5),
    ([("a", 0.33), ("b", 0.33), ("c", 0.34)], 1.66),
    ([("a", 0.25), ("b", 0.25), ("c", 0.25), ("d", 0.25)], 2),
    ([("a", 0.4), ("b", 0.2), ("c", 0.2), ("d", 0.2)], 2),
    ([("a", 0.3), ("b", 0.25), ("c", 0.25), ("d", 0.2)], 2),
    ([("a", 0.3), ("b", 0.2), ("c", 0.2), ("d", 0.2), ("e", 0.1)], 2.3),
]


def check_overlap_and_add_to_tree(tree, value):
    is_valid = len(tree) == 0
    for v in value:
        if v in tree:
            tree = tree[v]
        else:
            if len(tree) == 0 and not is_valid:
                return False
            tree[v] = {}
            tree = tree[v]
            is_valid = True

    return is_valid


def test_answer(student, test_case, correct_answer):
    if len(test_case) <= 20:
        feedback = "Feilet for tilfellet {:}.".format(
            test_case
        ) + " Ditt svar var {:}.\n".format(student)
    else:
        feedback = "Koden returnerte et galt svar:\n"

    if not isinstance(student, dict):
        feedback += "Funksjonen skal returnere en oppslagstabell (dictionary)."
        print(feedback)
        return False

    tree = {}
    expectance = 0
    for value, prob in test_case:
        if value not in student:
            feedback += "Beslutningen {:} er ikke med i treet.".format(value)
            print(feedback)
            return False

        encoding = student[value]
        if not isinstance(encoding, str) or not set(encoding) <= {"1", "0"}:
            feedback += (
                    "Hver beslutning skal ha en streng av nuller og "
                    + "enere knyttet til seg. "
            )
            print(feedback)
            return False

        if not check_overlap_and_add_to_tree(tree, encoding):
            feedback += "En av beslutningene er en internnode."
            print(feedback)
            return False

        expectance += prob * len(encoding)

    if expectance > correct_answer + 0.0000001:
        feedback += (
                "Beslutningstreet ditt er ikke optimalt. Det skulle "
                + "hatt en forventning på {:}".format(correct_answer)
                + " spørsmål, men har en forventning på "
                + str(expectance)
        )
        print(feedback)
        return False

    return True


passed = True
for test_case, answer in tests:
    student = build_decision_tree(test_case)
    passed &= test_answer(student, test_case, answer)

if passed:
    print("Passerte alle testene")
