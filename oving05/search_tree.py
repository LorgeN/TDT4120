def search_tree(root, dna):
    curr = root
    for ch in dna:
        curr = curr.children.get(ch)
        if not curr:
            return 0
    return curr.count


class Node:
    def __init__(self):
        self.children = {}
        self.count = 0

    def __str__(self):
        return (f"{{count: {self.count}, children: {{" + ", ".join(
            [f"'{c}': {node}" for c, node in self.children.items()]) + "}}")

    @classmethod
    def from_string(cls, s):
        node = Node()
        ind = 0
        ind = s.index("count") + len("count: ")
        ind2 = s.index(",", ind)
        node.count = int(s[ind:ind2])
        ind = s.index("{", ind) + 1
        while ind != len(s) - 2:
            ind = s.index("'", ind) + 1
            c = s[ind]
            ind = s.index("{", ind)
            ind2 = ind + 1
            count = 1
            while count:
                if s[ind2] == "{":
                    count += 1
                if s[ind2] == "}":
                    count -= 1
                ind2 += 1
            node.children[c] = Node.from_string(s[ind:ind2])
            ind = ind2
        return node


tests = [
    (("{count: 1, children: {}}", ""), 1),
    (("{count: 0, children: {}}", ""), 0),
    (("{count: 1, children: {}}", "A"), 0),
    (("{count: 2000, children: {}}", ""), 2000),
    (("{count: 0, children: {'A': {count: 1, children: {}}}}", ""), 0),
    (("{count: 0, children: {'A': {count: 2, children: {}}}}", "A"), 2),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'A': {count: 2, children: {}}}}}}",
            "A",
        ),
        0,
    ),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'A': {count: 2, children: {}}}}}}",
            "B",
        ),
        0,
    ),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'A': {count: 2, children: {}}}}}}",
            "AA",
        ),
        2,
    ),
    (("{count: 0, children: {}}", ""), 0),
    (
        (
            "{count: 1, children: {'T': {count: 0, children: {'G': {count: 0, children: {'C': {count: 1, children: {}}}}}}, 'A': {count: 0, children: {'C': {count: 1, children: {}}}}}}",
            "AC",
        ),
        1,
    ),
    (
        (
            "{count: 1, children: {'G': {count: 0, children: {'A': {count: 0, children: {'A': {count: 0, children: {'G': {count: 1, children: {}}}}}}}}}}",
            "",
        ),
        1,
    ),
    (("{count: 0, children: {}}", "GCAAC"), 0),
    (("{count: 0, children: {}}", "TGC"), 0),
    (
        (
            "{count: 0, children: {'T': {count: 0, children: {'T': {count: 0, children: {'C': {count: 0, children: {'A': {count: 1, children: {}}}}}}, 'G': {count: 1, children: {}}}}}}",
            "TCTCT",
        ),
        0,
    ),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'C': {count: 0, children: {'C': {count: 0, children: {'T': {count: 0, children: {'A': {count: 1, children: {}}}}}}}}}}, 'T': {count: 0, children: {'C': {count: 2, children: {}}}}}}",
            "TGA",
        ),
        0,
    ),
    (("{count: 0, children: {}}", ""), 0),
    (
        (
            "{count: 0, children: {'T': {count: 0, children: {'C': {count: 0, children: {'T': {count: 0, children: {'C': {count: 1, children: {}}}}}}}}, 'G': {count: 1, children: {}}}}",
            "TCTC",
        ),
        1,
    ),
    (("{count: 0, children: {'C': {count: 1, children: {}}}}", "CAA"), 0),
]

for test_case, answer in tests:
    root, dna = test_case
    root = Node.from_string(root)
    student = search_tree(root, dna)
    if student != answer:
        print(
            "Koden feilet for følgende input: "
            + '(root={:}, dna="{:}"). '.format(root, dna)
            + "Din output: {:}. Riktig output: {:}".format(student, answer)
        )
        break
