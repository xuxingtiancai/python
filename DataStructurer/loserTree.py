#
class LoserTree:
    class Node:
        def __init__(self, qid, v):
            self.qid = qid
            self.v = v

    def __init__(self, size, beat_value):
        if size <= 0:
            raise Exception('invalid para, size')
        self.size = size
        self.nodes = [None] * size
        self.beat_value = beat_value
    
    def getWinner(self):
        return self.nodes[0]
    
    #n1 beat n2   
    def beat_node(self, n1, n2):
        return self.beat_value(n1.v, n2.v)

    def insert(self, v):
        win_qid = self.nodes[0].qid
        player = LoserTree.Node(win_qid, v)
        cur = (win_qid + self.size) / 2

        while cur > 0:
            if self.beat_node(self.nodes[cur], player):
                self.nodes[cur], player = player, self.nodes[cur]
            cur /= 2
        self.nodes[0] = player
        return player.qid

    def build_pos(self, array, pos):
        if pos >= self.size:
            pos -= self.size
            return LoserTree.Node(pos, array[pos])

        left_winner = self.build_pos(array, 2 * pos)
        right_winner = self.build_pos(array, 2 * pos + 1)
        if self.beat_node(right_winner, left_winner):
            winner, loser = right_winner, left_winner
        else:
            winner, loser = left_winner, right_winner

        self.nodes[pos] = loser
        return winner

    def build(self, array):
        self.nodes[0] = self.build_pos(array, 1)
