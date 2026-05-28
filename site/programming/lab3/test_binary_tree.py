"""Тесты для модуля binary_tree (вариант 10).

Покрывают:
    - формулы вычисления потомков
    - все четыре реализации (dict, namedtuple, OrderedDict, dataclass)
    - вспомогательные функции tree_height и inorder
"""

import unittest
from collections import OrderedDict

from binary_tree import (
    BinaryTreeNode,
    TreeNode,
    _left,
    _right,
    gen_bin_tree,
    gen_bin_tree_dataclass,
    gen_bin_tree_namedtuple,
    gen_bin_tree_ordered_dict,
    inorder,
    tree_height,
)


class TestFormulas(unittest.TestCase):
    """Тесты формул вычисления потомков варианта 10."""

    def test_left_from_root_10(self):
        self.assertEqual(_left(10), 31)   # 10*3+1

    def test_right_from_root_10(self):
        self.assertEqual(_right(10), 29)  # 3*10-1

    def test_left_from_root_1(self):
        self.assertEqual(_left(1), 4)     # 1*3+1

    def test_right_from_root_1(self):
        self.assertEqual(_right(1), 2)    # 3*1-1

    def test_left_from_root_0(self):
        self.assertEqual(_left(0), 1)     # 0*3+1

    def test_right_from_root_0(self):
        self.assertEqual(_right(0), -1)   # 3*0-1


# ---------------------------------------------------------------------------
# dict
# ---------------------------------------------------------------------------

class TestGenBinTreeDict(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree(height=0, root=10))

    def test_returns_dict(self):
        self.assertIsInstance(gen_bin_tree(height=1, root=10), dict)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree(height=1, root=10)["value"], 10)

    def test_leaves_none_at_height_1(self):
        tree = gen_bin_tree(height=1, root=10)
        self.assertIsNone(tree["left"])
        self.assertIsNone(tree["right"])

    def test_left_child_value(self):
        self.assertEqual(gen_bin_tree(height=2, root=10)["left"]["value"], 31)

    def test_right_child_value(self):
        self.assertEqual(gen_bin_tree(height=2, root=10)["right"]["value"], 29)

    def test_keys_present(self):
        tree = gen_bin_tree(height=1, root=10)
        self.assertIn("value", tree)
        self.assertIn("left", tree)
        self.assertIn("right", tree)

    def test_default_params_root(self):
        self.assertEqual(gen_bin_tree()["value"], 10)

    def test_default_params_height(self):
        self.assertEqual(tree_height(gen_bin_tree()), 5)

    def test_custom_root(self):
        tree = gen_bin_tree(height=2, root=5)
        self.assertEqual(tree["value"], 5)
        self.assertEqual(tree["left"]["value"],  16)  # 5*3+1
        self.assertEqual(tree["right"]["value"], 14)  # 3*5-1

    def test_height_matches_actual(self):
        for h in range(1, 6):
            with self.subTest(height=h):
                self.assertEqual(tree_height(gen_bin_tree(height=h, root=10)), h)


# ---------------------------------------------------------------------------
# namedtuple
# ---------------------------------------------------------------------------

class TestGenBinTreeNamedTuple(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree_namedtuple(height=0, root=10))

    def test_returns_treenode(self):
        self.assertIsInstance(gen_bin_tree_namedtuple(height=1, root=10), TreeNode)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree_namedtuple(height=1, root=10).value, 10)

    def test_leaves_none_at_height_1(self):
        t = gen_bin_tree_namedtuple(height=1, root=10)
        self.assertIsNone(t.left)
        self.assertIsNone(t.right)

    def test_left_child_value(self):
        self.assertEqual(gen_bin_tree_namedtuple(height=2, root=10).left.value, 31)

    def test_right_child_value(self):
        self.assertEqual(gen_bin_tree_namedtuple(height=2, root=10).right.value, 29)

    def test_immutability(self):
        t = gen_bin_tree_namedtuple(height=1, root=10)
        with self.assertRaises(AttributeError):
            t.value = 99

    def test_height_matches_actual(self):
        self.assertEqual(tree_height(gen_bin_tree_namedtuple(height=4, root=10)), 4)

    def test_default_params_root(self):
        self.assertEqual(gen_bin_tree_namedtuple().value, 10)


# ---------------------------------------------------------------------------
# OrderedDict
# ---------------------------------------------------------------------------

class TestGenBinTreeOrderedDict(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree_ordered_dict(height=0, root=10))

    def test_returns_ordered_dict(self):
        self.assertIsInstance(gen_bin_tree_ordered_dict(height=1, root=10), OrderedDict)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree_ordered_dict(height=1, root=10)["value"], 10)

    def test_key_order(self):
        t = gen_bin_tree_ordered_dict(height=1, root=10)
        self.assertEqual(list(t.keys()), ["value", "left", "right"])

    def test_left_child_value(self):
        self.assertEqual(gen_bin_tree_ordered_dict(height=2, root=10)["left"]["value"], 31)

    def test_right_child_value(self):
        self.assertEqual(gen_bin_tree_ordered_dict(height=2, root=10)["right"]["value"], 29)

    def test_height_matches_actual(self):
        self.assertEqual(tree_height(gen_bin_tree_ordered_dict(height=3, root=10)), 3)

    def test_default_params_root(self):
        self.assertEqual(gen_bin_tree_ordered_dict()["value"], 10)


# ---------------------------------------------------------------------------
# dataclass
# ---------------------------------------------------------------------------

class TestGenBinTreeDataclass(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree_dataclass(height=0, root=10))

    def test_returns_binary_tree_node(self):
        self.assertIsInstance(gen_bin_tree_dataclass(height=1, root=10), BinaryTreeNode)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree_dataclass(height=1, root=10).value, 10)

    def test_leaves_none_at_height_1(self):
        t = gen_bin_tree_dataclass(height=1, root=10)
        self.assertIsNone(t.left)
        self.assertIsNone(t.right)

    def test_left_child_value(self):
        self.assertEqual(gen_bin_tree_dataclass(height=2, root=10).left.value, 31)

    def test_right_child_value(self):
        self.assertEqual(gen_bin_tree_dataclass(height=2, root=10).right.value, 29)

    def test_equality(self):
        t1 = gen_bin_tree_dataclass(height=2, root=10)
        t2 = gen_bin_tree_dataclass(height=2, root=10)
        self.assertEqual(t1, t2)

    def test_height_matches_actual(self):
        self.assertEqual(tree_height(gen_bin_tree_dataclass(height=5, root=10)), 5)

    def test_default_params(self):
        t = gen_bin_tree_dataclass()
        self.assertEqual(t.value, 10)
        self.assertEqual(tree_height(t), 5)


# ---------------------------------------------------------------------------
# tree_height
# ---------------------------------------------------------------------------

class TestTreeHeight(unittest.TestCase):

    def test_none_returns_0(self):
        self.assertEqual(tree_height(None), 0)

    def test_single_node_dict(self):
        self.assertEqual(tree_height(gen_bin_tree(height=1, root=10)), 1)

    def test_single_node_namedtuple(self):
        self.assertEqual(tree_height(gen_bin_tree_namedtuple(height=1, root=10)), 1)

    def test_single_node_dataclass(self):
        self.assertEqual(tree_height(gen_bin_tree_dataclass(height=1, root=10)), 1)

    def test_all_implementations_same_height(self):
        h = 4
        self.assertEqual(tree_height(gen_bin_tree(height=h)), h)
        self.assertEqual(tree_height(gen_bin_tree_namedtuple(height=h)), h)
        self.assertEqual(tree_height(gen_bin_tree_ordered_dict(height=h)), h)
        self.assertEqual(tree_height(gen_bin_tree_dataclass(height=h)), h)

    def test_unsupported_type_raises(self):
        with self.assertRaises(TypeError):
            tree_height("not a tree")


# ---------------------------------------------------------------------------
# inorder
# ---------------------------------------------------------------------------

class TestInorder(unittest.TestCase):

    def test_none_returns_empty(self):
        self.assertEqual(inorder(None), [])

    def test_single_node(self):
        self.assertEqual(inorder(gen_bin_tree(height=1, root=10)), [10])

    def test_height_2_dict(self):
        self.assertEqual(inorder(gen_bin_tree(height=2, root=10)), [31, 10, 29])

    def test_height_2_namedtuple(self):
        self.assertEqual(inorder(gen_bin_tree_namedtuple(height=2, root=10)), [31, 10, 29])

    def test_height_2_ordered_dict(self):
        self.assertEqual(inorder(gen_bin_tree_ordered_dict(height=2, root=10)), [31, 10, 29])

    def test_height_2_dataclass(self):
        self.assertEqual(inorder(gen_bin_tree_dataclass(height=2, root=10)), [31, 10, 29])

    def test_all_implementations_same_inorder(self):
        expected = inorder(gen_bin_tree(height=3, root=10))
        self.assertEqual(inorder(gen_bin_tree_namedtuple(height=3, root=10)), expected)
        self.assertEqual(inorder(gen_bin_tree_ordered_dict(height=3, root=10)), expected)
        self.assertEqual(inorder(gen_bin_tree_dataclass(height=3, root=10)), expected)

    def test_unsupported_type_raises(self):
        with self.assertRaises(TypeError):
            inorder(42)


if __name__ == "__main__":
    unittest.main(verbosity=2)
