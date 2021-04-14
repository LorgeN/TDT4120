from functools import lru_cache
from heapq import heapify, heappop, _siftdown


@lru_cache(maxsize=8192)
def dist(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)


def power_grid_sparse(nodes):
    x0, y0 = nodes.pop(0)
    nodes = [[dist(x0, y0, x1, y1), x1, y1] for x1, y1 in nodes]
    heapify(nodes)

    total = 0

    while nodes:
        u = heappop(nodes)
        d0, x0, y0 = u
        total += d0
        for i, v in enumerate(nodes):
            d1, x1, y1 = v
            nd1 = dist(x0, y0, x1, y1)
            if nd1 < d1:
                nodes[i][0] = nd1
                _siftdown(nodes, 0, i)

    return total


def get_0(o):
    return o[0]


def power_grid(m, n, nodes):
    if len(nodes) < 0.1 * m * n:
        return power_grid_sparse(nodes)

    cache = {node: [*node, None, 0] for node in nodes}
    parents = {station: [station, 0] for station in nodes}
    queue = list(cache.values())

    lvl = 0
    unions = []
    q_append = queue.append
    u_append = unions.append
    clr = unions.clear
    pop = queue.pop
    s = unions.sort
    while queue:
        u = pop(0)
        u_src = u[2]
        if not u_src:
            u[2] = u
            u_src = u

        u_par = dsf_parent(parents, (u_src[0], u_src[1]))

        if u[3] != lvl:
            lvl = u[3]
            s(key=get_0)
            for d, a, b in unions:
                dsf_fuse(parents, a, b, d)
            clr()

        for v in adjacent(m, n, u, cache, q_append):
            v_src = v[2]
            if not v_src:
                v[2] = v
                v_src = v

            v_par = dsf_parent(parents, (v_src[0], v_src[1]))
            if v_par is not u_par:
                union = (u[3] + v[3] + 1, u_par[0], v_par[0])
                u_append(union)

    s(key=get_0)
    for d, a, b in unions:
        dsf_fuse(parents, a, b, d)

    return dsf_parent(parents, nodes[0])[1]


def adjacent(m, n, node, cache, queue):
    x, y = node[0], node[1]
    lst = []
    append = lst.append
    par = node[2]
    adjacent_legal(m, n, x + 1, y, par, cache, append, node, queue)
    adjacent_legal(m, n, x - 1, y, par, cache, append, node, queue)
    adjacent_legal(m, n, x, y + 1, par, cache, append, node, queue)
    adjacent_legal(m, n, x, y - 1, par, cache, append, node, queue)
    return lst


def adjacent_legal(m, n, x, y, par, cache, append, node, queue):
    if 0 <= x < m and 0 <= y < n:
        if (x, y) in cache:
            append(cache[x, y])
        else:
            node = [x, y, par, node[3] + 1]
            cache[x, y] = node
            queue(node)


def dsf_parent(parents, station):
    par = parents[station]
    if station == par[0]:
        return par
    else:
        parents[station] = dsf_parent(parents, par[0])
        return parents[station]


def dsf_fuse(parents, station1, station2, d):
    par1 = dsf_parent(parents, station1)
    par2 = dsf_parent(parents, station2)
    if par1 is par2:
        return

    par1[1] += d + par2[1]
    parents[par2[0]] = par1


tests = [
    ((2, 2, [(1, 1)]), 0),
    ((2, 2, [(0, 0), (1, 1)]), 2),
    ((2, 2, [(0, 0), (0, 1), (1, 0)]), 2),
    ((2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]), 3),
    ((3, 3, [(0, 2), (2, 0)]), 4),
    ((3, 3, [(0, 0), (1, 1), (2, 2)]), 4),
    ((3, 3, [(1, 1), (0, 1), (2, 1)]), 2),
    ((3, 3, [(1, 2)]), 0),
    ((3, 3, [(2, 0), (1, 1), (0, 1)]), 3),
    ((2, 3, [(1, 1)]), 0),
    ((2, 2, [(0, 1), (1, 0), (1, 1), (0, 0)]), 3),
    ((2, 2, [(0, 1), (1, 0), (1, 1), (0, 0)]), 3),
    ((3, 3, [(0, 1), (0, 2), (2, 1), (2, 2)]), 4),
    ((3, 3, [(0, 1), (0, 2), (1, 2), (2, 1)]), 4),
    ((2, 3, [(1, 0), (1, 1), (0, 2)]), 3),
    ((2, 3, [(1, 0)]), 0),
    ((3, 2, [(1, 0), (2, 1), (0, 0)]), 3),
    ((3, 3, [(0, 1), (1, 1), (2, 1), (0, 0)]), 3),
    ((3, 3, [(0, 2)]), 0),
]

for test_case, answer in tests:
    m, n, substations = test_case
    student = power_grid(m, n, substations)
    if student != answer:
        response = (
                "Koden feilet for følgende input: "
                + "(m={:}, n={:}, substations={:}). ".format(m, n, substations)
                + "Din output: {:}. Riktig output: {:}".format(student, answer)
        )
        print(response)
        break
