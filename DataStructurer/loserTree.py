#

class LoserTree:
    class Node:
        def __init__(self, qid, v):
            self.qid = qid
            self.v = v

    def __init__(self, size):
        self.size = size
        self.nodes = [None] * size
    
    def getWinner(self):
        return self.nodes[0]

    def insert(self, v):
        win_qid = self.nodes[0].qid
        player = LoserTree.Node(win_qid, v)
        cur = win_qid / 2

        while cur > 0:
            if self.nodes[cur].v > player.v:
                self.nodes[cur], player = player, self.nodes[cur]
            cur /= 2
        self.nodes[0] = player
        print [n.v for n in self.nodes]
        return player.qid

    def build_pos(self, array, pos):
        if pos >= self.size:
            pos -= self.size
            return LoserTree.Node(pos, array[pos])

        left_winner = self.build_pos(array, 2 * pos)
        right_winner = self.build_pos(array, 2 * pos + 1)
        winner, loser = left_winner, right_winner
        if left_winner.v < right_winner.v:
            winner, loser = right_winner, left_winner

        self.nodes[pos] = loser
        return winner

    def build(self, array):
        self.nodes[0] = self.build_pos(array, 1)

#application
def find_k(array, k):
    tree = LoserTree(k)
    tree.build(array[:k])
    for i in array[k:]:
        tree.insert(i)

    print tree.getWinner().v


if __name__ == '__main__':
    find_k(range(100), 7)
