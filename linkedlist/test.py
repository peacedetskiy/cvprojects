import unittest
from LinkedList import *

class MyTestCase(unittest.TestCase):
    def test_node_init(self):
        a = Node(5)
        self.assertEqual(a.data, 5)
        self.assertEqual(a.next, None)


    def test_add_to_beginning(self):
        L = LinkedList()
        self.assertEqual(L.head, None)
        L.add_to_beginning(5)
        L.add_to_beginning(1)
        self.assertEqual(L.head.data, 1)


    def test_add_to_end(self):
        L = LinkedList()
        self.assertEqual(L.head, None)
        L.add_to_end(3)
        self.assertEqual(L.head.data, 3)
        L.add_to_end(2)
        last = L.head
        while last.next:
            last = last.next
        self.assertEqual(last.data, 2)


    def test_del_from_end(self):
        L = LinkedList()
        L.add_to_end(3)
        L.del_from_end()
        self.assertEqual(L.head, None)
        L.add_to_end(2)
        L.add_to_beginning(1)
        L.del_from_end()
        self.assertEqual(L.head.data, 1)
        self.assertEqual(L.head.next, None)


    def test_del_from_beginning(self):
        L = LinkedList()
        L.add_to_end(5)
        L.add_to_end(7)
        L.del_from_beginning()
        self.assertEqual(L.head.data, 7)


    def test_del_from_pos(self):
        L = LinkedList()
        L.add_to_end(7)
        L.add_to_end(8)
        L.add_to_end(9)
        L.del_from_pos(0)
        L.del_from_pos(1)
        self.assertEqual(L.head.data, 8)


    def test_del_every_second_even(self):
        L = LinkedList()
        for i in range(10):
            L.add_to_end(i)
        L.del_every_second()
        self.assertEqual(len(L), 5)


    def test_del_every_second_odd(self):
        L = LinkedList()
        for i in range(7):
            L.add_to_end(i)
        L.del_every_second()
        self.assertEqual(len(L), 4)


    def test_split_into_two(self):
        L = LinkedList()
        L.add_to_end(-1)
        L.add_to_end(1)
        li1 = LinkedList()
        li2 = LinkedList()
        L.split_into_two(li1, li2)
        self.assertEqual(li1.head.data, 1)
        self.assertEqual(li2.head.data, -1)


    def test_generator(self):
        L = LinkedList()
        L.generate(5)
        self.assertEqual(len(L), 5)


if __name__ == '__main__':
    unittest.main()
