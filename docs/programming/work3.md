# Бинарное дерево. Рекурсия

## Цель работы

Изучить принципы построения бинарных деревьев и рекурсивных алгоритмов на языке Python.

В рамках работы необходимо:

* реализовать рекурсивную функцию генерации бинарного дерева;
* реализовать вспомогательные функции `tree_height` и `inorder`;
* разработать модульные тесты с использованием `unittest`.

---

## Постановка задачи

### Задание (Вариант №10)

* **Корень по умолчанию:** `10`
* **Высота по умолчанию:** `5`
* **Левый потомок:** `root × 3 + 1`
* **Правый потомок:** `3 × root − 1`

### Пример дерева (высота = 2, корень = 10)

```
        10
       /  \
     31    29
```

* левый потомок: 10 × 3 + 1 = **31**
* правый потомок: 3 × 10 − 1 = **29**

---

## Листинг программы

### Файл `binary_tree.py`

```python
"""
Лабораторная работа №3. Построение бинарного дерева.
Вариант 10: root=10, height=5, left=root*3+1, right=3*root-1
"""


def gen_bin_tree(height=5, root=10):
    """Рекурсивно строит бинарное дерево в виде словаря.

    Args:
        height: высота дерева (по умолчанию 5).
        root: значение корневого узла (по умолчанию 10).

    Returns:
        Словарь {'root': ..., 'left': ..., 'right': ...}
        или None, если высота равна 0.
    """
    if height == 0:
        return None

    left_val = root * 3 + 1
    right_val = 3 * root - 1

    return {
        'root': root,
        'left': gen_bin_tree(height - 1, left_val),
        'right': gen_bin_tree(height - 1, right_val)
    }


def tree_height(tree):
    """Рекурсивно вычисляет высоту дерева.

    Args:
        tree: дерево в виде словаря или None.

    Returns:
        Высота дерева (целое число).
    """
    if tree is None:
        return 0
    return 1 + max(tree_height(tree['left']), tree_height(tree['right']))


def inorder(tree):
    """Обходит дерево в порядке: левый -> корень -> правый.

    Args:
        tree: дерево в виде словаря или None.

    Returns:
        Список значений узлов в порядке in-order.
    """
    if tree is None:
        return []
    return inorder(tree['left']) + [tree['root']] + inorder(tree['right'])


if __name__ == '__main__':
    tree = gen_bin_tree()
    print('Дерево:', tree)
    print('Высота:', tree_height(tree))
    print('Обход in-order:', inorder(tree))
```

---

### Файл `test_binary_tree.py`

```python
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
```

---

## Результаты тестирования

### TestGenBinTree (9 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_height_zero_returns_none` | height=0 → None | ✅ OK |
| 2 | `test_returns_dict` | возвращает dict | ✅ OK |
| 3 | `test_root_value` | `root == 10` | ✅ OK |
| 4 | `test_left_child` | левый потомок == 31 | ✅ OK |
| 5 | `test_right_child` | правый потомок == 29 | ✅ OK |
| 6 | `test_leaves_at_height_1` | left и right — None | ✅ OK |
| 7 | `test_default_root` | корень по умолчанию == 10 | ✅ OK |
| 8 | `test_default_height` | высота по умолчанию == 5 | ✅ OK |
| 9 | `test_keys_in_node` | ключи: root, left, right | ✅ OK |

### TestTreeHeight (3 теста)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_none_returns_zero` | None → 0 | ✅ OK |
| 2 | `test_single_node` | height=1 → 1 | ✅ OK |
| 3 | `test_height_3` | height=3 → 3 | ✅ OK |

### TestInorder (3 теста)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_none_returns_empty` | None → [] | ✅ OK |
| 2 | `test_single_node` | height=1 → [10] | ✅ OK |
| 3 | `test_height_2` | height=2 → [31, 10, 29] | ✅ OK |

```
Ran 15 tests in 0.XXXs

OK
```

---

## Вывод

Реализована рекурсивная генерация бинарного дерева по **Варианту №10** (корень=10, высота=5, левый=`root×3+1`, правый=`3×root−1`) в виде вложенных словарей. Дополнительно реализованы функции `tree_height()` для вычисления высоты и `inorder()` для обхода дерева. Разработаны **15 модульных тестов** в 3 классах, все тесты пройдены успешно.

---

## 📁 Файлы проекта

| Файл | Описание |
|---|---|
| [binary_tree.py](lab3/binary_tree.py) | Рекурсивное построение дерева + вспомогательные функции |
| [test_binary_tree.py](lab3/test_binary_tree.py) | 15 модульных тестов (3 класса) |
