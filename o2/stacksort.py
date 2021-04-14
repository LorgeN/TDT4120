def sort(stack1, stack2, stack3):
    if stack1.empty():
        return

    i = 0
    hi = 0
    lo = 0
    while not stack1.empty():
        x = stack1.pop()
        if i % 2 == 0:
            stack3.push(x)
            hi += 1
        else:
            stack2.push(x)
            lo += 1
        i += 1

    sort_amount(stack2, stack1, stack3, lo, True)
    sort_amount(stack3, stack1, stack2, hi, True)
    merge_into(stack2, stack3, stack1, lo, hi, desc)


def sort_amount(sin, tmp1, tmp2, amount, asc_ord):
    if amount <= 1:
        return

    n1 = amount // 2
    n2 = amount - n1

    # Push first n1 elements in sin to tmp1
    for i in range(n1):
        tmp1.push(sin.pop())

    # Push first n2 elements in sin to tmp2
    for i in range(n2):
        tmp2.push(sin.pop())

    sort_amount(tmp1, sin, tmp2, n1, not asc_ord)
    sort_amount(tmp2, sin, tmp1, n2, not asc_ord)

    merge_into(tmp1, tmp2, sin, n1, n2, asc if asc_ord else desc)


def desc(x, y):
    return x >= y


def asc(x, y):
    return y >= x


def merge_into(in1, in2, out, n1, n2, cmp):
    in1_head = None if n1 == 0 else in1.pop()
    in2_head = None if n2 == 0 else in2.pop()
    i1 = 0 if n1 is None else 1  # Items removed from each stack
    i2 = 0 if n2 is None else 1
    for i in range(n1 + n2):
        if in1_head is None:
            out.push(in2_head)

            if n2 == i2:
                in2_head = None
            else:
                in2_head = in2.pop()
                i2 += 1
        elif in2_head is None or cmp(in1_head, in2_head):
            out.push(in1_head)

            if n1 == i1:
                in1_head = None
            else:
                in1_head = in1.pop()
                i1 += 1
        else:
            out.push(in2_head)

            if n2 == i2:
                in2_head = None
            else:
                in2_head = in2.pop()
                i2 += 1


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def get_value(self):
        return self.value


class Stack:
    def __init__(self, operation_counter, element_counter, initial=None):
        self.stack = []
        if initial is not None:
            self.stack = initial

        self.element_counter = element_counter
        self.operation_counter = operation_counter

    def push(self, value):
        if self.element_counter.get_value() <= 0:
            raise RuntimeError(
                "Du kan ikke ta vare på flere elementer på "
                "stakkene enn det fantes originalt."
            )
        self.stack.append(value)
        self.element_counter.decrement()
        self.operation_counter.increment()

    def pop(self):
        if self.element_counter.get_value() >= 2:
            raise RuntimeError(
                "Du kan ikke ha mer enn 2 elementer i minnet " "av gangen."
            )
        self.element_counter.increment()
        self.operation_counter.increment()
        return self.stack.pop()

    def peek(self):
        self.operation_counter.increment()
        return self.stack[-1]

    def empty(self):
        return len(self.stack) == 0


# Tester, høyre side blir toppen av stakken
tests = (
    [4, 3, 2, 1],
    [1, 2, 3, 4],
    [4, 2, 1, 7],
    [1, 1, 1, 1],
    [7, 3, 9, 2, 0, 1, 3, 4],
    [7, 3, 0, 13, 48, 49, 233, 9, 2, 0, 1, 3, 4],
    [7, 97, 38, 21, 39, 12, 33, 12, 88, 46, 63, 82, 32, 37, 3, 0, 12, 13, 48]
    + [49, 233, 9, 2, 0, 1, 3, 4],
)

failed = False

for test in tests:
    counter1 = Counter()
    counter2 = Counter()
    stack1 = Stack(counter1, counter2, initial=test[:])
    stack2, stack3 = Stack(counter1, counter2), Stack(counter1, counter2)

    sort(stack1, stack2, stack3)

    result = []
    counter2.value = float("-inf")
    while not stack1.empty():
        result.append(stack1.pop())

    if result != sorted(test):
        print(
            "Feilet for testen {:}, resulterte i listen".format(test)
            + "{:} i stedet for {:}.".format(result, sorted(test))
        )
        failed = True
    else:
        print(
            "Koden brukte {:}".format(counter1.get_value() - len(result))
            + " operasjoner på sortering av {:}".format(test)
        )

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")
