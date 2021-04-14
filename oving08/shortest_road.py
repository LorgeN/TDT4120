from math import sqrt
from queue import PriorityQueue

WHITE = 0
GRAY = 1
BLACK = 2


def shortest_road(build_map, start, end):
    e = Node(*end, None, None)
    s = Node(*start, e, None)

    queue = PriorityQueue()
    queue.put(s)
    cache = {start: s, end: e}

    while not queue.empty():
        u = queue.get()
        for v in get_adjacent(u, build_map, cache, e):
            relax(u, v, queue)

            if v == e:
                v.predecessor = u
                queue.queue.clear()
                break

            if v.color == WHITE:
                v.color = GRAY
                queue.put(v)
        u.color = BLACK

    if not e.predecessor:
        return None

    path = []
    while e:
        path.append((e.x, e.y))
        e = e.predecessor
    return path


def get_adjacent(node, build_map, cache, e):
    adj = []
    add_adjacent(node, build_map, cache, adj, 0, 1, e)
    add_adjacent(node, build_map, cache, adj, 0, -1, e)
    add_adjacent(node, build_map, cache, adj, 1, 0, e)
    add_adjacent(node, build_map, cache, adj, -1, 0, e)
    return adj


def add_adjacent(node, build_map, cache, adj, x, y, e):
    x += node.x
    y += node.y
    if (x, y) in cache:
        if e.x == x and e.y == y:
            adj.append(e)
        return

    if x < 0 or y < 0:
        return

    width = len(build_map)
    if x >= width:
        return

    height = len(build_map[x])
    if y >= height:
        return

    if not build_map[x][y]:
        return

    new_node = Node(x, y, e, node)
    cache[x, y] = new_node
    adj.append(new_node)


def relax(u, v, queue):
    if v.rank > u.rank + 1:
        v.rank = u.rank + 1
        v.predecessor = u

        while True:
            x = queue.get()
            queue.put(x)
            if x == v:
                break


class Node:
    __slots__ = "color", "predecessor", "x", "y", "rank", "estimate"

    def __init__(self, x, y, goal, predecessor):
        self.x = x
        self.y = y
        self.estimate = 0 if not goal else sqrt((x - goal.x) ** 2 + (y - goal.y) ** 2)
        self.rank = 0 if not predecessor else predecessor.rank + 1
        self.predecessor = predecessor
        self.color = WHITE

    def __eq__(self, o):
        if isinstance(o, Node):
            return o.x == self.x and o.y == self.y
        return NotImplemented

    def __lt__(self, other):
        return (self.rank + self.estimate) < (other.rank + other.estimate)


# Disjoint-set forest
class Set:
    def __init__(self):
        self.__p = self
        self.rank = 0

    @property
    def p(self):
        if self.__p != self:
            self.__p = self.__p.p
        return self.__p

    @p.setter
    def p(self, value):
        self.__p = value.p


def union(x, y):
    x = x.p
    y = y.p
    if x.rank > y.rank:
        y.p = x
    else:
        x.p = y
        y.rank += x.rank == y.rank


tests = [
    (([[True, True]], (0, 1), (0, 0)), 2),
    (([[True, False, True]], (0, 0), (0, 2)), None),
    (([[True, True, True]], (0, 0), (0, 2)), 3),
    (([[True, True, False]], (0, 1), (0, 0)), 2),
    (([[True], [True]], (1, 0), (0, 0)), 2),
    (([[True, False], [True, True]], (0, 0), (1, 1)), 3),
    (([[False, True], [True, True]], (0, 1), (1, 0)), 3),
    (([[True, True], [True, True]], (1, 1), (0, 0)), 3),
    (([[False, False, True], [True, False, True]], (1, 2), (0, 2)), 2),
    (([[False, False], [True, True], [False, False]], (1, 1), (1, 0)), 2),
    (([[True, False], [True, False]], (0, 0), (1, 0)), 2),
    (([[True, False], [False, False], [True, True]], (0, 0), (2, 1)), None),
    (([[False, False, True], [False, False, True], [True, False, True]], (0, 2), (2, 2)), 3),
    (([[False, False], [True, True], [False, False]], (1, 1), (1, 0)), 2),
    (([[True, True, True], [False, False, False]], (0, 2), (0, 1)), 2),
    (([[True, False, True], [True, False, False]], (0, 2), (1, 0)), None),
    (([[True, True], [False, False], [False, True]], (0, 0), (0, 1)), 2),
    (([[False, True, False], [False, True, False]], (1, 1), (0, 1)), 2),
]

for test_case, answer in tests:
    build_map, start, end = test_case
    student_map = [i[:] for i in build_map]
    student = shortest_road(student_map, start, end)
    response = None
    if answer is None and student is not None:
        response = (
            "Du returnerte en liste med posisjoner når riktig svar var None."
        )
    elif student is None and answer is not None:
        response = "Du returnerte None, selv om det finnes en løsning."
    elif student is not None and answer < len(student):
        response = "Det finnes en liste med færre koordinater som fortsatt danner en gyldig vei."
    elif student is not None:
        for pos in student:
            if not (
                    0 <= pos[0] < len(build_map)
                    and 0 <= pos[1] < len(build_map[0])
            ):
                response = "Du prøver å bygge utenfor kartet."
                break
            if not build_map[pos[0]][pos[1]]:
                response = (
                    "Du prøver å bygge en plass der det ikke er mulig å bygge."
                )
                break
        else:
            disjoint_set = {pos: Set() for pos in student}
            for pos in student:
                for i, j in [
                    (pos[0] + 1, pos[1]),
                    (pos[0] - 1, pos[1]),
                    (pos[0], pos[1] + 1),
                    (pos[0], pos[1] - 1),
                ]:
                    if (i, j) in disjoint_set and disjoint_set[
                        (i, j)
                    ].p != disjoint_set[pos].p:
                        union(disjoint_set[pos], disjoint_set[(i, j)])
            if start not in disjoint_set:
                response = "Du har ikke med startlandsbyen i listen."
            if end not in disjoint_set:
                response = "Du har ikke med sluttlandsbyen i listen."
            if disjoint_set[start].p != disjoint_set[end].p:
                response = "Listen din gir ikke en sammenhengende vei."
    if response is not None:
        response += " Input: (build_map={:}, start={:}, ".format(
            build_map, start
        )
        response += "end={:}). Ditt svar: {:}".format(end, student)
        print(response)
        break
