"""Тесты для модуля binary_tree (вариант 10)."""

import unittest
from binary_tree import gen_bin_tree, tree_height, inorder


class TestGenBinTree(unittest.TestCase):

    def test_height_zero_returns_none(self):
        """При height=0 должен вернуться None."""
        self.assertIsNone(gen_bin_tree(height=0))

    def test_returns_dict(self):
        """Функция должна возвращать словарь."""
        result = gen_bin_tree(height=1, root=10)
        self.assertIsInstance(result, dict)

    def test_root_value(self):
        """Значение корня должно совпадать с переданным."""
        result = gen_bin_tree(height=1, root=10)
        self.assertEqual(result['root'], 10)

    def test_left_child(self):
        """Левый потомок: root*3+1."""
        result = gen_bin_tree(height=2, root=10)
        self.assertEqual(result['left']['root'], 31)

    def test_right_child(self):
        """Правый потомок: 3*root-1."""
        result = gen_bin_tree(height=2, root=10)
        self.assertEqual(result['right']['root'], 29)

    def test_leaves_at_height_1(self):
        """При height=1 потомки должны быть None."""
        result = gen_bin_tree(height=1, root=10)
        self.assertIsNone(result['left'])
        self.assertIsNone(result['right'])

    def test_default_root(self):
        """Корень по умолчанию равен 10."""
        result = gen_bin_tree()
        self.assertEqual(result['root'], 10)

    def test_default_height(self):
        """Высота по умолчанию равна 5."""
        result = gen_bin_tree()
        self.assertEqual(tree_height(result), 5)

    def test_keys_in_node(self):
        """Словарь должен содержать ключи root, left, right."""
        result = gen_bin_tree(height=1, root=10)
        self.assertIn('root', result)
        self.assertIn('left', result)
        self.assertIn('right', result)


class TestTreeHeight(unittest.TestCase):

    def test_none_returns_zero(self):
        self.assertEqual(tree_height(None), 0)

    def test_single_node(self):
        self.assertEqual(tree_height(gen_bin_tree(height=1)), 1)

    def test_height_3(self):
        self.assertEqual(tree_height(gen_bin_tree(height=3)), 3)


class TestInorder(unittest.TestCase):

    def test_none_returns_empty(self):
        self.assertEqual(inorder(None), [])

    def test_single_node(self):
        self.assertEqual(inorder(gen_bin_tree(height=1, root=10)), [10])

    def test_height_2(self):
        # левый(31) -> корень(10) -> правый(29)
        self.assertEqual(inorder(gen_bin_tree(height=2, root=10)), [31, 10, 29])


if __name__ == '__main__':
    unittest.main(verbosity=2)
