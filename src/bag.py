
"""
Execution:    python -m algs4.bag ../dataset/tobe.txt

% more ../dataset/tobe.txt
to be or not to - be - - that - - - is

% python -m algs4.bag ../dataset/tobe.txt
to be or not to - be - - that - - - is
"""
class Node:

    def __init__(self, item, next_node):
        self.item = item
        self.next = next_node


class LinkIterator:

    def __init__(self, current):
        self.current = current

    def __next__(self):
        if self.current is None:
            raise StopIteration()
        else:
            item = self.current.item
            self.current = self.current.next
            return item


class Bag:

    def __init__(self):
        self.first = None
        self.n = 0

    def __str__(self):
        return " ".join(str(i) for i in self)

    def __iter__(self):
        return LinkIterator(self.first)

    def size(self):
        return self.n

    def is_empty(self):
        return self.first is None

    def add(self, item):
        oldfirst = self.first
        self.first = Node(item, oldfirst)
        self.n += 1


if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        bag = Bag()
        for item in line.split():
            bag.add(item)
        print("size of bag = ", bag.size())
        for i in bag:
            print(i)
