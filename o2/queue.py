class Queue:
    def __init__(self, max_size):
        self.head = self.tail = 0
        self.val = [None] * max_size

    def enqueue(self, value):
        try:
            self.val[self.tail] = value
            self.tail += 1
            return
        except:
            self.val[0] = value
            self.tail = 1

    def dequeue(self):
        try:
            value = self.val[self.head]
            self.head += 1
            return value
        except:
            value = self.val[0]
            self.head = 1
            return value


def tester(values, sequence, max_size):
    """
    Tester en oppgitt sekvens av operasjoner og sjekker at verdiene
    (values) kommer ut i riktig rekkefølge.
    """
    index = 0
    queue = Queue(max_size)
    output = []
    for action in sequence:
        if action == "enqueue":
            queue.enqueue(values[index])
            index += 1
        elif action == "dequeue":
            output.append(queue.dequeue())

    if output != values:
        print(
            "Feilet for følgende sekvens av operasjoner "
            + "'{:}' med verdiene ".format(", ".join(sequence))
            + "'{:}' og maksimal størrelse".format(", ".join(map(str, values)))
            + "'{:}'".format(max_size)
        )
        return True
    return False


tests = (
    (
        [1, 7, 3],
        ("enqueue", "dequeue", "enqueue", "dequeue", "enqueue", "dequeue"),
        3,
    ),
    (
        [1, 7, 3],
        ("enqueue", "dequeue", "enqueue", "dequeue", "enqueue", "dequeue"),
        1,
    ),
    (
        [-1, 12, 0, 99],
        (
            "enqueue",
            "enqueue",
            "dequeue",
            "dequeue",
            "enqueue",
            "enqueue",
            "dequeue",
            "dequeue",
        ),
        2,
    ),
    (
        [-1, 12, 0, 99],
        (
            "enqueue",
            "enqueue",
            "dequeue",
            "enqueue",
            "dequeue",
            "enqueue",
            "dequeue",
            "dequeue",
        ),
        2,
    ),
    (
        [-1, 12, 0, 99],
        (
            "enqueue",
            "enqueue",
            "enqueue",
            "enqueue",
            "dequeue",
            "dequeue",
            "dequeue",
            "dequeue",
        ),
        4,
    ),
)

failed = False

for values, sequence, max_size in tests:
    failed |= tester(values, sequence, max_size)

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")
