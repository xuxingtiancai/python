class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        return str(self.val)

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

class ListUtil:
    @classmethod
    def len(cls, head):
        return sum(1 for n in ListNodeIter(head))
    @classmethod
    def show(cls, head):
        for n in ListNodeIter(head):
            print n

def connectAll(nodes):
    if len(nodes) == 0:
        return None
    def connect(x, y):
        x.next = y
        return y
    reduce(connect, nodes).next = None
    return nodes[0]

if __name__ == '__main__':
    nodes = [ListNode(i) for i in range(5)]
    head = connectAll(nodes)
    print 'len', ListUtil.len(head)
    ListUtil.show(head)
