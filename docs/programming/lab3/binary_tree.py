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
        Словарь вида ``{"value": ..., "left": ..., "right": ...}``
        или ``None``, если высота равна 0.
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
        Именованный кортеж ``TreeNode(value, left, right)``
        или ``None``, если высота равна 0.
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
        ``OrderedDict`` с ключами ``value``, ``left``, ``right``
        или ``None``, если высота равна 0.
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
        Экземпляр ``BinaryTreeNode`` или ``None``, если высота равна 0.
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
        tree: Дерево в любом из четырёх форматов или ``None``.

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
        tree: Дерево в любом из четырёх форматов или ``None``.

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
