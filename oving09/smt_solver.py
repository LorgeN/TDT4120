def check(variables, constraints):
    set = Set(variables)

    for a, op, b in constraints:
        par_a, _ = set.get_parent(a)
        par_b, __ = set.get_parent(b)
        if op == "=":
            set.fuse(par_a, par_b)
        if op == "<":
            set.set_greater_than(par_a, par_b)
        if op == ">":
            set.set_greater_than(par_b, par_a)

    nodes = {variable: [set.greater[variable], False, False, set.get_parent(variable)[0]]
             for variable in variables}

    for node in nodes.values():
        if node[2]:
            continue

        if not dfs_visit(node[3], nodes):
            return False
    return True


def dfs_visit(node, nodes):
    node = nodes[node]
    if node[2]:
        return True

    if node[1]:
        return False

    node[1] = True

    stack = list(node[0])
    while stack:
        next_node = nodes[stack.pop()]
        if next_node[2]:
            continue

        if not dfs_visit(next_node[3], nodes):
            return False
    node[2] = True
    return True


class Set:
    __slots__ = "parents", "greater"

    def __init__(self, variables):
        self.parents = {v: (v, 0) for v in variables}
        self.greater = {v: set() for v in variables}

    def get_parent(self, var):
        parent = self.parents[var]
        if parent[0] == var:
            return parent
        parent = self.get_parent(parent[0])
        self.parents[var] = parent
        return parent

    def fuse(self, var1, var2):
        parent1 = self.get_parent(var1)
        parent2 = self.get_parent(var2)
        if parent1[1] < parent2[1]:
            self.parents[var1] = parent2
            self.greater[var2].update(self.greater[var1])
        elif parent1[1] > parent2[1]:
            self.parents[var2] = parent1
            self.greater[var1].update(self.greater[var2])
        else:
            parent1 = (parent1[0], parent1[1] + 1)
            self.parents[var1] = parent1
            self.parents[var2] = parent1
            self.greater[var1].update(self.greater[var2])

    def set_greater_than(self, lt, gt):
        self.greater[gt].add(lt)


tests = [
    ((["x1"], []), True),
    ((["x1", "x2"], [("x1", "=", "x2")]), True),
    ((["x1"], [("x1", ">", "x1")]), False),
    ((["x1"], [("x1", "=", "x1")]), True),
    ((["x1", "x2"], [("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x2", "<", "x1"), ("x1", "=", "x2")]), False),
    ((["x1", "x2"], [("x2", ">", "x1"), ("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x1", ">", "x2"), ("x2", ">", "x1")]), False),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x2", "<", "x3"), ("x1", ">", "x3")],
        ),
        False,
    ),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x3", "=", "x1"), ("x2", "<", "x3")],
        ),
        False,
    ),
    ((["x4", "x0", "x1"], [("x1", "<", "x0")]), True),
    ((["x5", "x8"], [("x8", "<", "x5"), ("x8", "<", "x5")]), True),
    ((["x1", "x0", "x2"], []), True),
    (
        (
            ["x4", "x8", "x5"],
            [("x4", "<", "x5"), ("x8", ">", "x5"), ("x5", "<", "x8")],
        ),
        True,
    ),
    (
        (
            ["x5", "x9", "x0"],
            [
                ("x9", ">", "x5"),
                ("x9", "=", "x0"),
                ("x0", "=", "x9"),
                ("x0", "=", "x9"),
            ],
        ),
        True,
    ),
    (
        (
            ["x0", "x6", "x7"],
            [("x7", "=", "x0"), ("x7", ">", "x0"), ("x6", ">", "x0")],
        ),
        False,
    ),
    ((["x8", "x6", "x0"], []), True),
    (
        (
            ["x8", "x7", "x0"],
            [("x8", "=", "x0"), ("x0", "=", "x8"), ("x0", "=", "x8")],
        ),
        True,
    ),
    (
        (
            ["x8", "x4"],
            [
                ("x4", ">", "x8"),
                ("x4", ">", "x8"),
                ("x8", "<", "x4"),
                ("x4", ">", "x8"),
                ("x8", "=", "x4"),
            ],
        ),
        False,
    ),
    ((["x3", "x8", "x5"], [("x3", ">", "x8")]), True),
]

for test_case, answer in tests:
    variables, constraints = test_case
    student = check(variables, constraints)
    if student != answer:
        response = (
                "Koden feilet for følgende input: "
                + "(variables={:}, constraints={:}). ".format(variables, constraints)
                + "Din output: {:}. Riktig output: {:}".format(student, answer)
        )
        print(response)
        break
