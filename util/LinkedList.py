__author__ = 'xuxing'
import unittest

#node
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        return str(self.val)

#iter
class ListNodeIter():
    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return self

    def next(self):
        current = self.node
        try:
            self.node = self.node.next
        except:
            raise StopIteration
        return current

class LinkedList:
    def __init__(self, values = []):
        nodes = [ListNode(val) for val in values]
        if len(nodes) == 0:
            self.head = None
            self.tail = None
            self.len = 0
            return

        def connect(x, y):
            x.next = y
            return y
        reduce(connect, nodes).next = None
        self.head = nodes[0]
        self.tail = nodes[-1]
        self.len = len(nodes)

    def __str__(self):
        return ','.join(str(node) for node in iter(self))

    def __len__(self):
        return self.len

    def __iter__(self):
        return ListNodeIter(self.head)

    def append(self, node):
        if not node:
            return
        node.next = None
        if not self.head:
            self.head = node
            self.tail = node
            self.len = 1
        else:
            self.tail.next = node
            self.len += 1

    def remove(self, node):
        pass
