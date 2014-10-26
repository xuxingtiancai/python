from List import *

class Intersect(Exception):
    def __init__(self):  
        Exception.__init__(self)

class CommonIter:
    def __init__(self, node):
        self.sp = node
        self.fp = node

    def __iter__(self):
        return self

    def next(self):
        try:
            self.sp = self.sp.next
            self.fp = self.fp.next.next
        except:
            raise StopIteration
        if self.sp == self.fp:
            raise Intersect

def getLoop(head):
    iter = CommonIter(head)
    try:
        while True:
            iter.next()
    except StopIteration:
        return None
    except Intersect:
        return iter.sp
    

if __name__ == '__main__':
    nodes = [ListNode(i) for i in range(5)]
    head = connectAll(nodes)
    nodes[-1].next = nodes[2]

    print getLoop(head)
