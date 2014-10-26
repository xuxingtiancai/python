#coding = utf-8
__author__ = 'xuxing'

import unittest
from linkedList import *

class LinkedListTest(unittest.TestCase):
    def setUp(self):
        self.empty = LinkedList()
        self.L = LinkedList(range(5))

    def tearDown(self):
        pass

    def testLen(self):
        self.assertEqual(0, len(self.empty))
        self.assertEqual(5, len(self.L))

    def testStr(self):
        self.assertEqual('0,1,2,3,4', str(self.L))

    def testAppend(self):
        self.L.append(ListNode(9))
        self.assertEqual(6, len(self.L))

if __name__ =='__main__':
    unittest.main()
