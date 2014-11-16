__author__ = 'xuxing'

class TreeNode:
    def __init__(self):
        self.val = 'x'
        self.children = [None] * 2

    def __str__(self):
        stack = [root]
        result = ''
        while stack:
            node = stack.pop(0)
            result += str(node.val) if node else '#'
            if node:
                stack.extend(node.children)
        return result

def insert_str(root, s):
    def insert_bit(node, bit):
        if node.children[bit] is None:
            node.children[bit] = TreeNode()
        return node.children[bit]
    reduce(insert_bit, map(int, s), root)

def insert_array(array):
    root = TreeNode()
    for s in array:
        insert_str(root, s)
    return root

def contain(root, s):
    def sift(node, bit):
        return None if node is None else node.children[bit]
    result = reduce(sift, map(int, s), root)
    return result is not None

if __name__ == '__main__':
    root = insert_array(['11', '00'])
    print contain(root, '1')
    print contain(root, '11')
    print contain(root, '111')
    print contain(root, '10')
