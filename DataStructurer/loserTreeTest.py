import random
import unittest
from loserTree import LoserTree


#application
def find_k(array, k, beat):
    tree = LoserTree(k+1, beat)
    tree.build(array[:k+1])
    for i in array[k+1:]:
        tree.insert(i)

    return reduce(lambda i, j: i if beat(i, j) else j, (n.v for n in tree.nodes[1: k+1]))

def multiple_merge(array_list, beat):
    Sentinel = object()
    def beat_Sentinel(i, j):
        if i == Sentinel:
            return False
        if j == Sentinel:
            return True
        return beat(i, j)
    tree = LoserTree(len(array_list), beat_Sentinel)

    array_iter_list = [iter(i) for i in array_list]
    initial = []
    for i in array_iter_list:
        try:
            initial.append(i.next())
        except:
            initial.append(Sentinel)
    tree.build(initial)
    
    result = []
    while True:
        winner = tree.getWinner()
        qid, v = winner.qid, winner.v
        if v == Sentinel:
            break
        
        result.append(v)

        try:
            tree.insert(array_iter_list[qid].next())
        except:
            tree.insert(Sentinel)

    return result

class LoserTreeTest(unittest.TestCase):
    def setUp(self):
        print 'setup-loserTree'

    def tearDown(self):
        print 'tearDown-loserTree'
    
    def testFindK(self):
        x = range(100)
        random.shuffle(x)
        #larger win = min_k
        self.assertEqual(6, find_k(x, 7, lambda i, j : i > j))
        #smaller win = max_k
        self.assertEqual(93, find_k(x, 7, lambda i, j : i < j))

    def testMultipleMerge(self):
        array_list = [[3 * i + mod for i in range(10)] for mod in range(3)]
        #smaller win = [min ~ max]
        self.assertEqual(range(30), multiple_merge(array_list, lambda i, j : i < j))


if __name__ == '__main__':
   unittest.main()
