def find_path(weights):
    if not weights:
        return []

    rows = len(weights)
    columns = len(weights[0])

    for y in range(1, rows):
        next_row = weights[y - 1]
        row = weights[y]
        for x in range(columns):
            val = next_row[x]

            if x > 0:
                x_sub_1 = x - 1
                poss = next_row[x_sub_1]
                if poss < val:
                    val = poss

            x_add_1 = x + 1
            if x_add_1 < columns:
                poss = next_row[x_add_1]
                if poss < val:
                    val = poss

            row[x] += val

    last_row = weights[-1]
    x = min(range(columns), key=last_row.__getitem__)

    res = [None] * rows
    res[rows - 1] = (x, rows - 1)

    for y in range(rows - 2, -1, -1):
        row = weights[y]

        val = row[x]
        next_x = x

        if x > 0:
            x_sub_1 = x - 1
            poss = row[x_sub_1]
            if poss < val:
                val = poss
                next_x = x_sub_1

        x_add_1 = x + 1
        if x_add_1 < columns:
            poss = row[x_add_1]
            if poss < val:
                next_x = x_add_1

        x = next_x
        res[y] = (x, y)
    return res


# Tester på formatet (vekter, minste mulige vekt på sti).
tests = [
    ([[1]], 1),
    ([[1, 1]], 1),
    ([[1], [1]], 2),
    ([[2, 1], [2, 1]], 2),
    ([[1, 1], [1, 1]], 2),
    ([[2, 1], [1, 2]], 2),
    ([[3, 2, 1], [1, 3, 2], [2, 1, 3]], 4),
    ([[1, 10, 3, 3], [1, 10, 3, 3], [10, 10, 3, 3]], 9),
    ([[1, 2, 7, 4], [9, 3, 2, 5], [5, 7, 8, 3], [1, 3, 4, 6]], 10),
]


# Verifiserer at en løsning er riktig gitt vektene, stien og den minst
# mulige vekten man kan ha på en sti.
def verify(weights, path, optimal):
    if len(path) != len(weights):
        return False, "Stien er enten for lang eller for kort."

    last = -1
    for index, element in enumerate(path):
        if type(element) != tuple:
            return False, "Stien består ikke av tupler."
        if len(element) != 2:
            return False, "Stien består ikke av tupler på formatet (x,y)."
        if index != element[1]:
            return False, "Stien er ikke vertikal."
        if element[0] < 0 or element[0] >= len(weights[0]):
            return False, "Stien går utenfor bildet."
        if last != -1 and not last - 1 <= element[0] <= last + 1:
            return False, "Stien hopper mer enn en piksel per rad."
        last = element[0]

    weight = sum(weights[y][x] for x, y in path)
    if weight != optimal:
        return (
            False,
            "Stien er ikke optimal. En optimal sti ville hatt"
            + "vekten {:}, mens din hadde vekten {:}".format(optimal, weight),
        )

    return True, ""


failed = False

for test, optimal_weight in tests:
    answer = find_path([row[:] for row in test])
    correct, error_message = verify(test, answer, optimal_weight)
    if not correct:
        failed = True
        print(
            'Feilet med feilmeldingen "{:}" for testen '.format(error_message)
            + "{:}. Ditt svar var {:}.".format(test, answer)
        )

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")
