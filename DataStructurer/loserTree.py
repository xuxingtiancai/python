class LoserTree:
    class Node:
        def __init__(self, qid, v):
            self.qid = qid
            self.v = v

    def __init__(self, size):
        self.nodes = [None] * size
    
    def getWinner(self):
        return self.nodes[0]

    def insert(self, v):
        win_qid = self.nodes[0].qid
        player = Node(win_qid, v)
        cur = win_qid / 2

        while cur > 0:
            if self.nodes[cur].v < player.v:
                self.nodes[cur], player = player, self.nodes[cur]
            cur /= 2
        self.nodes[0] = player
        return player.qid

    def build(self, array):
        for i in range(self.size)[::-1]:
            left = self.nodes[2 * i]
            right = self.nodes[2 * i + 1]

#application
def find_k(array, k):
    tree = LoserTree()
    tree.build(array[:k])
    for i in array[k:]:
        tree.insert(i)

    print tree.winner().v


if __name__ == '__main__':
    find_k(range(100), 7)
