# Бинарное дерево. Рекурсия

## Цель работы

Изучить принципы построения бинарных деревьев и рекурсивных алгоритмов на языке Python.

В рамках работы необходимо:

* реализовать рекурсивную функцию генерации бинарного дерева в четырёх вариантах хранения узлов;
* реализовать вспомогательные функции `tree_height` и `inorder`;
* разработать модульные тесты с использованием `unittest`.

---

## Постановка задачи

### Задание (Вариант №10)

Реализовать рекурсивную генерацию бинарного дерева:

* **Корень по умолчанию:** `10`
* **Высота по умолчанию:** `5`
* **Левый потомок:** `root × 3 + 1`
* **Правый потомок:** `3 × root − 1`

Реализовать **четыре варианта** хранения узлов:

| № | Тип | Описание |
|---|-----|----------|
| 1 | `dict` | Вложенные словари `{"value": ..., "left": ..., "right": ...}` |
| 2 | `collections.namedtuple` | Именованный кортеж `TreeNode(value, left, right)` |
| 3 | `collections.OrderedDict` | Упорядоченный словарь с гарантированным порядком ключей |
| 4 | `dataclass` | Класс с аннотациями `BinaryTreeNode` |

Дополнительно реализовать:
- `tree_height(tree)` — вычисление высоты дерева;
- `inorder(tree)` — обход дерева в порядке «левый → корень → правый».

### Пример дерева (высота = 2, корень = 10)

```
            10
           /   \
         31     29
```

* левый потомок: 10 × 3 + 1 = **31**
* правый потомок: 3 × 10 − 1 = **29**

---

## Теоретические сведения

### Рекурсия и бинарное дерево

Бинарное дерево — структура данных, в которой каждый узел имеет не более двух потомков. Рекурсивное построение:

```text
gen_bin_tree(height, root):
    если height == 0  → вернуть None
    иначе             → создать узел (root, левое поддерево, правое поддерево)
                        где левое  = gen_bin_tree(height-1, root*3+1)
                        и   правое = gen_bin_tree(height-1, 3*root-1)
```

### collections.namedtuple

`namedtuple` создаёт неизменяемый кортеж с именованными полями:

```python
from collections import namedtuple
TreeNode = namedtuple("TreeNode", ["value", "left", "right"])
node = TreeNode(value=10, left=None, right=None)
print(node.value)  # 10
# node.value = 99  # AttributeError: нельзя изменить
```

### collections.OrderedDict

`OrderedDict` гарантирует сохранение порядка добавления ключей (в Python 3.7+ обычный `dict` тоже сохраняет порядок, но `OrderedDict` явно выражает это намерение):

```python
from collections import OrderedDict
node = OrderedDict()
node["value"] = 10
node["left"]  = None
node["right"] = None
print(list(node.keys()))  # ['value', 'left', 'right']
```

### dataclass

`@dataclass` автоматически генерирует `__init__`, `__repr__`, `__eq__` и другие методы:

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BinaryTreeNode:
    value: int
    left:  Optional["BinaryTreeNode"] = field(default=None)
    right: Optional["BinaryTreeNode"] = field(default=None)
```

---

## Листинг программы

### Файл `binary_tree.py`

```python
"""
Построение бинарного дерева — вариант 10.

Параметры варианта по умолчанию:
    root   = 10
    height = 5
    left   = root * 3 + 1
    right  = 3 * root - 1

Реализованы четыре варианта хранения дерева:
    1. dict              — базовый вариант
    2. collections.namedtuple
    3. collections.OrderedDict
    4. dataclass
"""

from __future__ import annotations

from collections import namedtuple, OrderedDict
from dataclasses import dataclass, field
from typing import Optional, Union

# ---------------------------------------------------------------------------
# Константы варианта
# ---------------------------------------------------------------------------

START_ROOT: int = 10
START_HEIGHT: int = 5

# ---------------------------------------------------------------------------
# Формулы вычисления потомков (вариант 10)
# ---------------------------------------------------------------------------


def calc_left(val: int) -> int:
    """Возвращает значение левого потомка: val * 3 + 1."""
    return val * 3 + 1


def calc_right(val: int) -> int:
    """Возвращает значение правого потомка: 3 * val - 1."""
    return 3 * val - 1


# ---------------------------------------------------------------------------
# Вспомогательные типы
# ---------------------------------------------------------------------------

TreeNode = namedtuple("TreeNode", ["value", "left", "right"])
TreeNode.__new__.__defaults__ = (None, None)  # left и right по умолчанию None


@dataclass
class BinaryTreeNode:
    """Узел бинарного дерева на основе dataclass."""

    value: int
    left: Optional["BinaryTreeNode"] = field(default=None)
    right: Optional["BinaryTreeNode"] = field(default=None)


DTree      = Optional[dict]
NTupleTree = Optional[TreeNode]
OdTree     = Optional[OrderedDict]
DcTree     = Optional[BinaryTreeNode]
TreeType   = Union[DTree, NTupleTree, OdTree, DcTree]


# ---------------------------------------------------------------------------
# 1. dict
# ---------------------------------------------------------------------------


def gen_bin_tree(
    height: int = START_HEIGHT,
    root: int = START_ROOT,
) -> DTree:
    """Рекурсивно строит дерево в виде вложенных словарей.

    Args:
        height: Высота дерева. При 0 возвращает None.
        root:   Значение корневого узла.

    Returns:
        Словарь вида {"value": ..., "left": ..., "right": ...}
        или None, если высота равна 0.
    """
    if height == 0:
        return None
    return {
        "value": root,
        "left":  gen_bin_tree(height - 1, calc_left(root)),
        "right": gen_bin_tree(height - 1, calc_right(root)),
    }


# ---------------------------------------------------------------------------
# 2. namedtuple
# ---------------------------------------------------------------------------


def gen_bin_tree_namedtuple(
    height: int = START_HEIGHT,
    root: int = START_ROOT,
) -> NTupleTree:
    """Рекурсивно строит дерево, используя collections.namedtuple.

    Args:
        height: Высота дерева.
        root:   Значение корневого узла.

    Returns:
        Именованный кортеж TreeNode(value, left, right)
        или None, если высота равна 0.
    """
    if height == 0:
        return None
    return TreeNode(
        value=root,
        left=gen_bin_tree_namedtuple(height - 1, calc_left(root)),
        right=gen_bin_tree_namedtuple(height - 1, calc_right(root)),
    )


# ---------------------------------------------------------------------------
# 3. OrderedDict
# ---------------------------------------------------------------------------


def gen_bin_tree_ordered_dict(
    height: int = START_HEIGHT,
    root: int = START_ROOT,
) -> OdTree:
    """Рекурсивно строит дерево, используя collections.OrderedDict.

    Args:
        height: Высота дерева.
        root:   Значение корневого узла.

    Returns:
        OrderedDict с ключами value, left, right
        или None, если высота равна 0.
    """
    if height == 0:
        return None
    od_node: OrderedDict = OrderedDict()
    od_node["value"] = root
    od_node["left"]  = gen_bin_tree_ordered_dict(height - 1, calc_left(root))
    od_node["right"] = gen_bin_tree_ordered_dict(height - 1, calc_right(root))
    return od_node


# ---------------------------------------------------------------------------
# 4. dataclass
# ---------------------------------------------------------------------------


def gen_bin_tree_dataclass(
    height: int = START_HEIGHT,
    root: int = START_ROOT,
) -> DcTree:
    """Рекурсивно строит дерево, используя узлы-dataclass.

    Args:
        height: Высота дерева.
        root:   Значение корневого узла.

    Returns:
        Экземпляр BinaryTreeNode или None, если высота равна 0.
    """
    if height == 0:
        return None
    return BinaryTreeNode(
        value=root,
        left=gen_bin_tree_dataclass(height - 1, calc_left(root)),
        right=gen_bin_tree_dataclass(height - 1, calc_right(root)),
    )


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def tree_height(tree: TreeType) -> int:
    """Вычисляет фактическую высоту дерева рекурсивно.

    Args:
        tree: Дерево в любом из четырёх форматов или None.

    Returns:
        Целое число — высота дерева (0 для пустого дерева).

    Raises:
        TypeError: Если передан неподдерживаемый тип.
    """
    if tree is None:
        return 0
    if isinstance(tree, dict):
        return 1 + max(tree_height(tree["left"]), tree_height(tree["right"]))
    if isinstance(tree, BinaryTreeNode):
        return 1 + max(tree_height(tree.left), tree_height(tree.right))
    if isinstance(tree, tuple):  # namedtuple
        return 1 + max(tree_height(tree.left), tree_height(tree.right))
    raise TypeError(f"Неподдерживаемый тип дерева: {type(tree)}")


def inorder(tree: TreeType) -> list[int]:
    """Обходит дерево в порядке in-order (левый → корень → правый).

    Args:
        tree: Дерево в любом из четырёх форматов или None.

    Returns:
        Список значений узлов в порядке in-order.

    Raises:
        TypeError: Если передан неподдерживаемый тип.
    """
    if tree is None:
        return []
    if isinstance(tree, dict):
        return inorder(tree["left"]) + [tree["value"]] + inorder(tree["right"])
    if isinstance(tree, (BinaryTreeNode, tuple)):
        return inorder(tree.left) + [tree.value] + inorder(tree.right)
    raise TypeError(f"Неподдерживаемый тип дерева: {type(tree)}")


def show_tree(tree: TreeType, prefix: str = "", is_left: bool = True) -> None:
    """Выводит дерево в консоль в виде ASCII-графики.

    Args:
        tree:    Дерево для отображения.
        prefix:  Строка-отступ для текущего уровня.
        is_left: Признак того, является ли узел левым потомком.
    """
    if tree is None:
        return
    if isinstance(tree, dict):
        node_val, l_child, r_child = tree["value"], tree["left"], tree["right"]
    else:
        node_val, l_child, r_child = tree.value, tree.left, tree.right
    branch = "|-- " if is_left else "\\-- "
    print(prefix + branch + str(node_val))
    pad = "|   " if is_left else "    "
    show_tree(l_child, prefix + pad, is_left=True)
    show_tree(r_child, prefix + pad, is_left=False)


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Binary tree — variant 10")
    print("root=10, height=5, left=root*3+1, right=3*root-1")
    print("=" * 60)

    print("\n[1] dict (height=3):")
    tree_d = gen_bin_tree(height=3, root=10)
    show_tree(tree_d)
    print(f"    height  : {tree_height(tree_d)}")
    print(f"    in-order: {inorder(tree_d)}")

    print("\n[2] namedtuple (height=2):")
    print(f"    {gen_bin_tree_namedtuple(height=2, root=10)}")

    print("\n[3] OrderedDict (height=2):")
    tree_od = gen_bin_tree_ordered_dict(height=2, root=10)
    print(f"    keys: {list(tree_od.keys())}")

    print("\n[4] dataclass (height=2):")
    print(f"    {gen_bin_tree_dataclass(height=2, root=10)}")

    print("\n[5] Full tree (height=5):")
    full_tree = gen_bin_tree()
    print(f"    height  : {tree_height(full_tree)}")
    print(f"    in-order (first 7): {inorder(full_tree)[:7]} ...")
```

---

### Файл `test_binary_tree.py`

```python
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
```

---

## Результаты тестирования

### TestChildFormulas — формулы потомков (6 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_left_from_root_10` | `calc_left(10) == 31` | ✅ OK |
| 2 | `test_right_from_root_10` | `calc_right(10) == 29` | ✅ OK |
| 3 | `test_left_from_root_1` | `calc_left(1) == 4` | ✅ OK |
| 4 | `test_right_from_root_1` | `calc_right(1) == 2` | ✅ OK |
| 5 | `test_left_from_root_0` | `calc_left(0) == 1` | ✅ OK |
| 6 | `test_right_from_root_0` | `calc_right(0) == -1` | ✅ OK |

### TestDictImpl — dict (11 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_height_zero_returns_none` | height=0 → None | ✅ OK |
| 2 | `test_returns_dict` | height=1 → dict | ✅ OK |
| 3 | `test_root_value` | `tr["value"] == 10` | ✅ OK |
| 4 | `test_leaves_none_at_height_1` | left и right — None | ✅ OK |
| 5 | `test_left_child_value` | левый потомок == 31 | ✅ OK |
| 6 | `test_right_child_value` | правый потомок == 29 | ✅ OK |
| 7 | `test_keys_present` | ключи: value, left, right | ✅ OK |
| 8 | `test_default_params_root` | корень по умолчанию == 10 | ✅ OK |
| 9 | `test_default_params_height` | высота по умолчанию == 5 | ✅ OK |
| 10 | `test_custom_root` | root=5: left=16, right=14 | ✅ OK |
| 11 | `test_height_matches_actual` | высота 1..5 соответствует | ✅ OK |

### TestNamedTupleImpl — namedtuple (9 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_height_zero_returns_none` | height=0 → None | ✅ OK |
| 2 | `test_returns_treenode` | возвращает TreeNode | ✅ OK |
| 3 | `test_root_value` | `.value == 10` | ✅ OK |
| 4 | `test_leaves_none_at_height_1` | left, right — None | ✅ OK |
| 5 | `test_left_child_value` | `.left.value == 31` | ✅ OK |
| 6 | `test_right_child_value` | `.right.value == 29` | ✅ OK |
| 7 | `test_immutability` | присвоение → AttributeError | ✅ OK |
| 8 | `test_height_matches_actual` | высота == 4 | ✅ OK |
| 9 | `test_default_params_root` | корень по умолчанию == 10 | ✅ OK |

### TestOrderedDictImpl — OrderedDict (8 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_height_zero_returns_none` | height=0 → None | ✅ OK |
| 2 | `test_returns_ordered_dict` | возвращает OrderedDict | ✅ OK |
| 3 | `test_root_value` | `["value"] == 10` | ✅ OK |
| 4 | `test_key_order` | порядок ключей: value, left, right | ✅ OK |
| 5 | `test_left_child_value` | левый потомок == 31 | ✅ OK |
| 6 | `test_right_child_value` | правый потомок == 29 | ✅ OK |
| 7 | `test_height_matches_actual` | высота == 3 | ✅ OK |
| 8 | `test_default_params_root` | корень по умолчанию == 10 | ✅ OK |

### TestDataclassImpl — dataclass (9 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_height_zero_returns_none` | height=0 → None | ✅ OK |
| 2 | `test_returns_binary_tree_node` | возвращает BinaryTreeNode | ✅ OK |
| 3 | `test_root_value` | `.value == 10` | ✅ OK |
| 4 | `test_leaves_none_at_height_1` | left, right — None | ✅ OK |
| 5 | `test_left_child_value` | `.left.value == 31` | ✅ OK |
| 6 | `test_right_child_value` | `.right.value == 29` | ✅ OK |
| 7 | `test_equality` | два одинаковых дерева равны | ✅ OK |
| 8 | `test_height_matches_actual` | высота == 5 | ✅ OK |
| 9 | `test_default_params` | root=10, height=5 | ✅ OK |

### TestHeightCalc — tree_height (6 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_none_returns_0` | None → 0 | ✅ OK |
| 2 | `test_single_node_dict` | dict h=1 → 1 | ✅ OK |
| 3 | `test_single_node_namedtuple` | namedtuple h=1 → 1 | ✅ OK |
| 4 | `test_single_node_dataclass` | dataclass h=1 → 1 | ✅ OK |
| 5 | `test_all_implementations_same_height` | все 4 типа: h=4 | ✅ OK |
| 6 | `test_unsupported_type_raises` | строка → TypeError | ✅ OK |

### TestInorderTraversal — inorder (8 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_none_returns_empty` | None → [] | ✅ OK |
| 2 | `test_single_node` | h=1 → [10] | ✅ OK |
| 3 | `test_height_2_dict` | h=2 dict → [31, 10, 29] | ✅ OK |
| 4 | `test_height_2_namedtuple` | h=2 namedtuple → [31, 10, 29] | ✅ OK |
| 5 | `test_height_2_ordered_dict` | h=2 OrderedDict → [31, 10, 29] | ✅ OK |
| 6 | `test_height_2_dataclass` | h=2 dataclass → [31, 10, 29] | ✅ OK |
| 7 | `test_all_implementations_same_inorder` | все 4 типа: h=3 одинаковы | ✅ OK |
| 8 | `test_unsupported_type_raises` | int → TypeError | ✅ OK |

```
Ran 57 tests in 0.XXXs

OK
```

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `collections.namedtuple` | Неизменяемый именованный кортеж `TreeNode` |
| `collections.OrderedDict` | Словарь с гарантированным порядком ключей |
| `dataclasses` | Автогенерация `__init__`, `__eq__`, `__repr__` для `BinaryTreeNode` |
| `typing` | Аннотации типов (`Optional`, `Union`) |
| `unittest` | Модульное тестирование |

---

## Структура файлов

```
lab3/
├── binary_tree.py       # Четыре реализации + tree_height + inorder + show_tree
└── test_binary_tree.py  # 57 тестов (7 классов)
```

---

## Вывод

В ходе работы реализована рекурсивная генерация бинарного дерева по **Варианту №10** (корень=10, высота=5, левый=`root×3+1`, правый=`3×root−1`) в четырёх вариантах хранения:

* `gen_bin_tree()` — вложенные словари `dict`;
* `gen_bin_tree_namedtuple()` — неизменяемый `TreeNode` через `namedtuple`;
* `gen_bin_tree_ordered_dict()` — `OrderedDict` с фиксированным порядком ключей;
* `gen_bin_tree_dataclass()` — класс `BinaryTreeNode` с `@dataclass`.

Реализованы вспомогательные функции `tree_height()`, `inorder()` и `show_tree()`, поддерживающие все четыре типа. Разработаны **57 модульных тестов** в 7 классах, покрывающих формулы потомков, все реализации, граничные случаи и обработку ошибок.

---

## 📁 Файлы проекта

| Файл | Описание |
|---|---|
| [binary_tree.py](lab3/binary_tree.py) | Четыре реализации дерева + вспомогательные функции |
| [test_binary_tree.py](lab3/test_binary_tree.py) | 57 модульных тестов (7 классов) |
