from math import inf


def least_energy(reactions, start, goal, laws_of_thermodynamics=True):
    adjacency = {}
    distance = {}
    previous = {}
    parents = {}
    for a, b, e in reactions:
        if a in adjacency:
            adjacency_list = adjacency[a]
            adjacency_list.append((b, e))
        else:
            adjacency_list = [(b, e)]
            adjacency[a] = adjacency_list

        distance[a] = inf
        distance[b] = inf
        parents[a] = []
        parents[b] = []

    distance[start] = 0
    previous[start] = None

    queue = [start]
    while len(queue) > 0:
        node = queue.pop()

        try:
            for neighbour, e in adjacency[node]:
                w = distance[node] + e
                if distance[neighbour] > w and (laws_of_thermodynamics or neighbour not in parents[node]):
                    parents[neighbour] = parents[node] + [node]
                    previous[neighbour] = node
                    distance[neighbour] = w

                    if neighbour not in queue:
                        queue.append(neighbour)

        except KeyError:
            pass

    path = []
    prev = goal
    while prev:
        path.insert(0, prev)
        prev = previous[prev]
    return path


tests = [
    (([("A", "B", 100)], "A", "B"), 100),
    (([("B", "A", -100)], "B", "A"), -100),
    (([("A", "B", 100), ("B", "A", -100)], "A", "B"), 100),
    (([("A", "B", 100), ("B", "A", -100)], "B", "A"), -100),
    (([("A", "B", 100), ("B", "C", -50), ("A", "C", 70)], "A", "C"), 50),
    (([("A", "B", 100), ("B", "C", -20), ("A", "C", 70)], "A", "C"), 70),
    (
        (
            [
                ("A", "C", -100),
                ("B", "C", -100),
                ("A", "C", -201),
                ("B", "A", 100),
            ],
            "A",
            "C",
        ),
        -201,
    ),
    (([("Y", "N", 11), ("N", "Y", -10)], "Y", "N"), 11),
    (
        (
            [
                ("E", "K", 68),
                ("F", "K", 21),
                ("K", "F", -21),
                ("F", "E", 50),
                ("K", "E", 10),
                ("E", "F", -1),
            ],
            "E",
            "F",
        ),
        -1,
    ),
    (
        (
            [("C", "V", 36), ("C", "B", 18), ("B", "C", -17), ("V", "B", 54)],
            "C",
            "B",
        ),
        18,
    ),
    (
        (
            [
                ("P", "G", 47),
                ("G", "T", 52),
                ("T", "P", 20),
                ("P", "T", -19),
                ("G", "P", 30),
            ],
            "T",
            "G",
        ),
        67,
    ),
    (
        (
            [
                ("F", "Y", 69),
                ("U", "F", 47),
                ("Y", "U", -5),
                ("Y", "F", 18),
                ("U", "Y", 6),
            ],
            "U",
            "Y",
        ),
        6,
    ),
    (
        (
            [
                ("K", "G", -27),
                ("A", "G", 52),
                ("G", "A", 18),
                ("K", "A", -17),
                ("A", "K", 17),
            ],
            "K",
            "A",
        ),
        -17,
    ),
    (
        (
            [
                ("X", "H", 2),
                ("X", "U", 48),
                ("H", "X", -1),
                ("U", "H", 41),
                ("H", "U", 36),
                ("U", "X", 49),
            ],
            "X",
            "U",
        ),
        38,
    ),
    (([("V", "L", 11), ("L", "V", -10)], "V", "L"), 11),
    (([("C", "W", 23), ("W", "C", -22)], "W", "C"), -22),
    (
        (
            [("K", "P", 30), ("I", "P", 21), ("I", "K", 19), ("P", "I", -20)],
            "P",
            "K",
        ),
        -1,
    ),
]


def get_feedback(student, answer, reactions, start, goal):
    if len(student) < 2:
        return "Du returnerte en liste med færre en to elementer"
    if student[0] != start:
        return "Listen din starter ikke med startstoffet"
    if student[-1] != goal:
        return "Listen din ender ikke med målstoffet"
    costs = {}
    for a, b, e in reactions:
        costs[(a, b)] = e
    cost = 0
    for i in range(len(student) - 1):
        if (student[i], student[i + 1]) not in costs:
            return "Du gjør en reaksjon som ikke er lov"
        cost += costs[(student[i], student[i + 1])]
    if cost > answer:
        return "Du lager ikke stoffet på den mest energieffektive måten"


failed = False

for test_case, answer in tests:
    reactions, start, goal = test_case
    student = least_energy(reactions[:], start, goal)
    response = get_feedback(student, answer, reactions, start, goal)
    if response is not None:
        failed = True
        response = (
                "Koden feilet for følgende input: "
                + "(reactions={:}, start={:}, ".format(reactions, start)
                + "goal={:}. Din output: {:}. ".format(goal, student)
                + response
        )
        print(response)
        break

if not failed:
    print("Koden fungerte for alle eksempeltestene.")
