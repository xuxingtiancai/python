#coding=gbk

import sys
sys.path.append(r'D:\workspace\resources\lib')
import util
from functools import wraps

c_Exists = 0

class SimpleTrieTree(object):
    def __init__(self):
        self.tree = {}

    def add(self, word):
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                tree[char] = dict()
                tree = tree[char]
        tree[c_Exists] = True
    
    def match(self, word, start=0, root=None):
        if root == None:
            root = self.tree

        if c_Exists in root:
            yield []
        if start >= len(word):
            return
        if word[start] in root:
            for res in self.match(word, start+1, root[word[start]]):
                yield [word[start]] + res

    def match(self, word, start=0, root=None):
        if root == None:
            root = self.tree

        if c_Exists in root:
            yield []
        if start >= len(word):
            return
        if word[start] in root:
            for res in self.match(word, start+1, root[word[start]]):
                yield [word[start]] + res

    def search(self, word):
        for i in range(len(word)):
            sub = word[i:]
            for res in self.match(sub):
                yield res

    def is_match(self, word, start=0, root=None):
        if root == None:
            root = self.tree

        if c_Exists in root:
            return True
        if start >= len(word):
            return False
        if word[start] in root:
            return self.is_match(word, start+1, root[word[start]])
        return False

    def is_search(self, word):
        return any(self.is_match(word[i:]) for i in range(len(word)))

#对抽出的pattern进行汇总 ent取最长的
def aggregation(fn):
    @wraps(fn)
    def wrapper(*args):
        pat_dic = dict()
        for pat_chars, es, ews in fn(*args):
            pat = ''.join(pat_chars)
            if pat not in pat_dic:
                pat_dic[pat] = (pat_chars, es, ews)
            else:
                if len(''.join(ews)) > len(''.join(pat_dic[pat][2])):
                    pat_dic[pat] = (pat_chars, es, ews)

        for pat_chars, es, ews in pat_dic.itervalues():
            yield pat_chars, es, ews
    return wrapper


class ComplexTrieTree(SimpleTrieTree): 
    def __init__(self, ent_tree_dic):
        self.tree = dict()
        self.ent_tree_dic = ent_tree_dic
    
    @aggregation
    def match(self, word, start=0, root=None): 
        if root == None:
            root = self.tree
        if c_Exists in root:
            yield [], [], []
        if start >= len(word):
            return

        if word[start] in root:
            for pat_chars, es, ews in self.match(word, start+1, root[word[start]]):
                yield [word[start]] + pat_chars, es, ews
        for e, tree in self.ent_tree_dic.iteritems():
            if e in root:
                for ent_chars in tree.match(word, start):
                    ew = ''.join(ent_chars)
                    for pat_chars, es, ews in self.match(word, start+len(ew), root[e]):
                        yield [e] + pat_chars, [e] + es, [ew] + ews

    @aggregation
    def search(self, word):
        for i in range(len(word)):
            sub = word[i:]
            for res in self.match(sub):
                yield res

    def is_match(self, word, start=0, root=None): 
        if root == None:
            root = self.tree
        if c_Exists in root:
            return True
        if start >= len(word):
            return False

        def selections():
            if word[start] in root:
                yield self.is_match(word, start+1, root[word[start]])
            for k, v in self.ent_tree_dic.iteritems():
                if k in root:
                    for res in v.match(word, start):
                        yield self.is_match(word, start+len(res), root[k])
        return any(selections())

if __name__ == '__main__':
    print u'测试simple'
    tree = SimpleTrieTree()
    tree.add('ab')
    tree.add('cd')
    for res in tree.match('cde'):
        print res

    print u'测试complex'
    ent_tree = SimpleTrieTree()
    ent_tree.add(u'告白')
    ent_tree.add(u'告白气球')

    pattern_tree = ComplexTrieTree({u'$song':ent_tree})
    pattern_tree.add(list(u'我想听') + ['$song'] + list(u'操蛋'))
    pattern_tree.add(list(u'我想听') + ['$song'])

    for pat_chars, es, ews in pattern_tree.match(u'我想听告白气球操蛋'):
        print ''.join(pat_chars), ''.join(es), ''.join(ews)

    print pattern_tree.is_match(u'我想听告白气球操蛋')
