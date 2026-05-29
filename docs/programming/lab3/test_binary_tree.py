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
    calc_left,
    calc_right,
    gen_bin_tree,
    gen_bin_tree_dataclass,
    gen_bin_tree_namedtuple,
    gen_bin_tree_ordered_dict,
    inorder,
    tree_height,
)


class TestChildFormulas(unittest.TestCase):
    """Тесты формул вычисления потомков варианта 10."""

    def test_left_from_root_10(self):
        self.assertEqual(calc_left(10), 31)   # 10*3+1

    def test_right_from_root_10(self):
        self.assertEqual(calc_right(10), 29)  # 3*10-1

    def test_left_from_root_1(self):
        self.assertEqual(calc_left(1), 4)     # 1*3+1

    def test_right_from_root_1(self):
        self.assertEqual(calc_right(1), 2)    # 3*1-1

    def test_left_from_root_0(self):
        self.assertEqual(calc_left(0), 1)     # 0*3+1

    def test_right_from_root_0(self):
        self.assertEqual(calc_right(0), -1)   # 3*0-1


# ---------------------------------------------------------------------------
# dict
# ---------------------------------------------------------------------------

class TestDictImpl(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree(height=0, root=10))

    def test_returns_dict(self):
        self.assertIsInstance(gen_bin_tree(height=1, root=10), dict)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree(height=1, root=10)["value"], 10)

    def test_leaves_none_at_height_1(self):
        tr = gen_bin_tree(height=1, root=10)
        self.assertIsNone(tr["left"])
        self.assertIsNone(tr["right"])

    def test_left_child_value(self):
        self.assertEqual(gen_bin_tree(height=2, root=10)["left"]["value"], 31)

    def test_right_child_value(self):
        self.assertEqual(gen_bin_tree(height=2, root=10)["right"]["value"], 29)

    def test_keys_present(self):
        tr = gen_bin_tree(height=1, root=10)
        self.assertIn("value", tr)
        self.assertIn("left", tr)
        self.assertIn("right", tr)

    def test_default_params_root(self):
        self.assertEqual(gen_bin_tree()["value"], 10)

    def test_default_params_height(self):
        self.assertEqual(tree_height(gen_bin_tree()), 5)

    def test_custom_root(self):
        tr = gen_bin_tree(height=2, root=5)
        self.assertEqual(tr["value"], 5)
        self.assertEqual(tr["left"]["value"],  16)  # 5*3+1
        self.assertEqual(tr["right"]["value"], 14)  # 3*5-1

    def test_height_matches_actual(self):
        for ht in range(1, 6):
            with self.subTest(height=ht):
                self.assertEqual(tree_height(gen_bin_tree(height=ht, root=10)), ht)


# ---------------------------------------------------------------------------
# namedtuple
# ---------------------------------------------------------------------------

class TestNamedTupleImpl(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree_namedtuple(height=0, root=10))

    def test_returns_treenode(self):
        self.assertIsInstance(gen_bin_tree_namedtuple(height=1, root=10), TreeNode)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree_namedtuple(height=1, root=10).value, 10)

    def test_leaves_none_at_height_1(self):
        nd = gen_bin_tree_namedtuple(height=1, root=10)
        self.assertIsNone(nd.left)
        self.assertIsNone(nd.right)

    def test_left_child_value(self):
        self.assertEqual(gen_bin_tree_namedtuple(height=2, root=10).left.value, 31)

    def test_right_child_value(self):
        self.assertEqual(gen_bin_tree_namedtuple(height=2, root=10).right.value, 29)

    def test_immutability(self):
        nd = gen_bin_tree_namedtuple(height=1, root=10)
        with self.assertRaises(AttributeError):
            nd.value = 99

    def test_height_matches_actual(self):
        self.assertEqual(tree_height(gen_bin_tree_namedtuple(height=4, root=10)), 4)

    def test_default_params_root(self):
        self.assertEqual(gen_bin_tree_namedtuple().value, 10)


# ---------------------------------------------------------------------------
# OrderedDict
# ---------------------------------------------------------------------------

class TestOrderedDictImpl(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree_ordered_dict(height=0, root=10))

    def test_returns_ordered_dict(self):
        self.assertIsInstance(gen_bin_tree_ordered_dict(height=1, root=10), OrderedDict)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree_ordered_dict(height=1, root=10)["value"], 10)

    def test_key_order(self):
        nd = gen_bin_tree_ordered_dict(height=1, root=10)
        self.assertEqual(list(nd.keys()), ["value", "left", "right"])

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

class TestDataclassImpl(unittest.TestCase):

    def test_height_zero_returns_none(self):
        self.assertIsNone(gen_bin_tree_dataclass(height=0, root=10))

    def test_returns_binary_tree_node(self):
        self.assertIsInstance(gen_bin_tree_dataclass(height=1, root=10), BinaryTreeNode)

    def test_root_value(self):
        self.assertEqual(gen_bin_tree_dataclass(height=1, root=10).value, 10)

    def test_leaves_none_at_height_1(self):
        nd = gen_bin_tree_dataclass(height=1, root=10)
        self.assertIsNone(nd.left)
        self.assertIsNone(nd.right)

    def test_left_child_value(self):
        self.assertEqual(gen_bin_tree_dataclass(height=2, root=10).left.value, 31)

    def test_right_child_value(self):
        self.assertEqual(gen_bin_tree_dataclass(height=2, root=10).right.value, 29)

    def test_equality(self):
        nd1 = gen_bin_tree_dataclass(height=2, root=10)
        nd2 = gen_bin_tree_dataclass(height=2, root=10)
        self.assertEqual(nd1, nd2)

    def test_height_matches_actual(self):
        self.assertEqual(tree_height(gen_bin_tree_dataclass(height=5, root=10)), 5)

    def test_default_params(self):
        nd = gen_bin_tree_dataclass()
        self.assertEqual(nd.value, 10)
        self.assertEqual(tree_height(nd), 5)


# ---------------------------------------------------------------------------
# tree_height
# ---------------------------------------------------------------------------

class TestHeightCalc(unittest.TestCase):

    def test_none_returns_0(self):
        self.assertEqual(tree_height(None), 0)

    def test_single_node_dict(self):
        self.assertEqual(tree_height(gen_bin_tree(height=1, root=10)), 1)

    def test_single_node_namedtuple(self):
        self.assertEqual(tree_height(gen_bin_tree_namedtuple(height=1, root=10)), 1)

    def test_single_node_dataclass(self):
        self.assertEqual(tree_height(gen_bin_tree_dataclass(height=1, root=10)), 1)

    def test_all_implementations_same_height(self):
        ht = 4
        self.assertEqual(tree_height(gen_bin_tree(height=ht)), ht)
        self.assertEqual(tree_height(gen_bin_tree_namedtuple(height=ht)), ht)
        self.assertEqual(tree_height(gen_bin_tree_ordered_dict(height=ht)), ht)
        self.assertEqual(tree_height(gen_bin_tree_dataclass(height=ht)), ht)

    def test_unsupported_type_raises(self):
        with self.assertRaises(TypeError):
            tree_height("not a tree")


# ---------------------------------------------------------------------------
# inorder
# ---------------------------------------------------------------------------

class TestInorderTraversal(unittest.TestCase):

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
