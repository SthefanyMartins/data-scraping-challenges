
import unittest
from binary_tree import BinaryTree

class TestBinaryTree(unittest.TestCase):
    def setUp(self):
        self.tree = BinaryTree()
        self.tree.insert(10)
        self.tree.insert(5)
        self.tree.insert(15)
        self.tree.insert(2)
        self.tree.insert(7)

    def test_insert_and_search(self):
        self.assertTrue(self.tree.search(10))
        self.assertTrue(self.tree.search(5))
        self.assertFalse(self.tree.search(20))
        self.assertTrue(self.tree.search(7))
        self.assertFalse(self.tree.search(100))

    def test_inorder_traversal(self):
        self.assertEqual(self.tree.inorder_traversal(), [2, 5, 7, 10, 15])

if __name__ == '__main__':
    unittest.main()