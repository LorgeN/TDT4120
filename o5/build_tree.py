def build_tree(dna_sequences):
    root = Node()

    for dna_sequence in dna_sequences:
        curr = root
        for ch in dna_sequence:
            local = curr.children.get(ch)
            if not local:
                local = Node()
                curr.children[ch] = local
            curr = local
        curr.count += 1
    return root


class Node:
    def __init__(self):
        self.children = {}
        self.count = 0
        self.decendants = 0

    def __str__(self):
        return (
                f"{{count: {self.count}, children: {{"
                + ", ".join(
            [f"'{c}': {node}" for c, node in self.children.items()]
        )
                + "}}"
        )

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


def node_equals(node1, node2):
    stack = [(node1, node2)]
    while len(stack):
        if type(node1) != Node or type(node2) != Node:
            return False
        node1, node2 = stack.pop()
        if node1.count != node2.count:
            return False
        if len(node1.children) != len(node2.children):
            return False
        for key in node1.children:
            if key not in node2.children:
                return False
            stack.append((node1.children[key], node2.children[key]))
    return True


tests = [
    ([""], "{count: 1, children: {}}"),
    ([], "{count: 0, children: {}}"),
    (["A"], "{count: 0, children: {'A': {count: 1, children: {}}}}"),
    (["A", "A"], "{count: 0, children: {'A': {count: 2, children: {}}}}"),
    (
        ["AA", "AA"],
        "{count: 0, children: {'A': {count: 0, children: {'A': {count: 2, children: {}}}}}}",
    ),
    (
        ["AB", "AA"],
        "{count: 0, children: {'A': {count: 0, children: {'A': {count: 1, children: {}}, 'B': {count: 1, children: {}}}}}}",
    ),
    (
        ["BA", "AB"],
        "{count: 0, children: {'A': {count: 0, children: {'B': {count: 1, children: {}}}}, 'B': {count: 0, children: {'A': {count: 1, children: {}}}}}}",
    ),
    (
        ["AA", "AA", "A"],
        "{count: 0, children: {'A': {count: 1, children: {'A': {count: 2, children: {}}}}}}",
    ),
    ([], "{count: 0, children: {}}"),
    (
        ["", "GCC"],
        "{count: 1, children: {'G': {count: 0, children: {'C': {count: 0, children: {'C': {count: 1, children: {}}}}}}}}",
    ),
    (
        ["TGAA", "GAAG", ""],
        "{count: 1, children: {'G': {count: 0, children: {'A': {count: 0, children: {'A': {count: 0, children: {'G': {count: 1, children: {}}}}}}}}, 'T': {count: 0, children: {'G': {count: 0, children: {'A': {count: 0, children: {'A': {count: 1, children: {}}}}}}}}}}",
    ),
    (
        ["AGG", "", "", "ACACT"],
        "{count: 2, children: {'A': {count: 0, children: {'C': {count: 0, children: {'A': {count: 0, children: {'C': {count: 0, children: {'T': {count: 1, children: {}}}}}}}}, 'G': {count: 0, children: {'G': {count: 1, children: {}}}}}}}}",
    ),
    (
        ["CCG", "ATT"],
        "{count: 0, children: {'A': {count: 0, children: {'T': {count: 0, children: {'T': {count: 1, children: {}}}}}}, 'C': {count: 0, children: {'C': {count: 0, children: {'G': {count: 1, children: {}}}}}}}}",
    ),
    (
        ["", "CTG"],
        "{count: 1, children: {'C': {count: 0, children: {'T': {count: 0, children: {'G': {count: 1, children: {}}}}}}}}",
    ),
    (
        ["CTCTG", "ACAC", "TAG", "CTG"],
        "{count: 0, children: {'T': {count: 0, children: {'A': {count: 0, children: {'G': {count: 1, children: {}}}}}}, 'A': {count: 0, children: {'C': {count: 0, children: {'A': {count: 0, children: {'C': {count: 1, children: {}}}}}}}}, 'C': {count: 0, children: {'T': {count: 0, children: {'G': {count: 1, children: {}}, 'C': {count: 0, children: {'T': {count: 0, children: {'G': {count: 1, children: {}}}}}}}}}}}}",
    ),
    (["", "T"], "{count: 1, children: {'T': {count: 1, children: {}}}}"),
    (
        ["AG", "G", "TCTC", "TTCAT", "CAA"],
        "{count: 0, children: {'C': {count: 0, children: {'A': {count: 0, children: {'A': {count: 1, children: {}}}}}}, 'T': {count: 0, children: {'T': {count: 0, children: {'C': {count: 0, children: {'A': {count: 0, children: {'T': {count: 1, children: {}}}}}}}}, 'C': {count: 0, children: {'T': {count: 0, children: {'C': {count: 1, children: {}}}}}}}}, 'G': {count: 1, children: {}}, 'A': {count: 0, children: {'G': {count: 1, children: {}}}}}}",
    ),
    ([""], "{count: 1, children: {}}"),
]

for test_case, answer in tests:
    student = build_tree(test_case)
    if not node_equals(student, Node.from_string(answer)):
        print(
            "Koden feilet for følgende input: "
            + "(dna_sequences={:}). ".format(test_case)
            + "Din output: {:}. Riktig output: {:}".format(student, answer)
        )
        break
