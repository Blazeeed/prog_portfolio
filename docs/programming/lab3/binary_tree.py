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

_DEFAULT_ROOT: int = 10
_DEFAULT_HEIGHT: int = 5

# ---------------------------------------------------------------------------
# Формулы вычисления потомков (вариант 10)
# ---------------------------------------------------------------------------


def _left(root: int) -> int:
    """Возвращает значение левого потомка: root * 3 + 1."""
    return root * 3 + 1


def _right(root: int) -> int:
    """Возвращает значение правого потомка: 3 * root - 1."""
    return 3 * root - 1


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


DictTree = Optional[dict]
NTTree   = Optional[TreeNode]
ODTree   = Optional[OrderedDict]
DCTree   = Optional[BinaryTreeNode]
AnyTree  = Union[DictTree, NTTree, ODTree, DCTree]


# ---------------------------------------------------------------------------
# 1. dict
# ---------------------------------------------------------------------------


def gen_bin_tree(
    height: int = _DEFAULT_HEIGHT,
    root: int = _DEFAULT_ROOT,
) -> DictTree:
    """Рекурсивно строит дерево в виде вложенных словарей."""
    if height == 0:
        return None
    return {
        "value": root,
        "left":  gen_bin_tree(height - 1, _left(root)),
        "right": gen_bin_tree(height - 1, _right(root)),
    }


# ---------------------------------------------------------------------------
# 2. namedtuple
# ---------------------------------------------------------------------------


def gen_bin_tree_namedtuple(
    height: int = _DEFAULT_HEIGHT,
    root: int = _DEFAULT_ROOT,
) -> NTTree:
    """Рекурсивно строит дерево, используя collections.namedtuple."""
    if height == 0:
        return None
    return TreeNode(
        value=root,
        left=gen_bin_tree_namedtuple(height - 1, _left(root)),
        right=gen_bin_tree_namedtuple(height - 1, _right(root)),
    )


# ---------------------------------------------------------------------------
# 3. OrderedDict
# ---------------------------------------------------------------------------


def gen_bin_tree_ordered_dict(
    height: int = _DEFAULT_HEIGHT,
    root: int = _DEFAULT_ROOT,
) -> ODTree:
    """Рекурсивно строит дерево, используя collections.OrderedDict."""
    if height == 0:
        return None
    node: OrderedDict = OrderedDict()
    node["value"] = root
    node["left"]  = gen_bin_tree_ordered_dict(height - 1, _left(root))
    node["right"] = gen_bin_tree_ordered_dict(height - 1, _right(root))
    return node


# ---------------------------------------------------------------------------
# 4. dataclass
# ---------------------------------------------------------------------------


def gen_bin_tree_dataclass(
    height: int = _DEFAULT_HEIGHT,
    root: int = _DEFAULT_ROOT,
) -> DCTree:
    """Рекурсивно строит дерево, используя узлы-dataclass."""
    if height == 0:
        return None
    return BinaryTreeNode(
        value=root,
        left=gen_bin_tree_dataclass(height - 1, _left(root)),
        right=gen_bin_tree_dataclass(height - 1, _right(root)),
    )


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def tree_height(tree: AnyTree) -> int:
    """Вычисляет фактическую высоту дерева рекурсивно."""
    if tree is None:
        return 0
    if isinstance(tree, dict):
        return 1 + max(tree_height(tree["left"]), tree_height(tree["right"]))
    if isinstance(tree, BinaryTreeNode):
        return 1 + max(tree_height(tree.left), tree_height(tree.right))
    if isinstance(tree, tuple):  # namedtuple
        return 1 + max(tree_height(tree.left), tree_height(tree.right))
    raise TypeError(f"Неподдерживаемый тип дерева: {type(tree)}")


def inorder(tree: AnyTree) -> list[int]:
    """Обходит дерево в порядке in-order (левый → корень → правый)."""
    if tree is None:
        return []
    if isinstance(tree, dict):
        return inorder(tree["left"]) + [tree["value"]] + inorder(tree["right"])
    if isinstance(tree, (BinaryTreeNode, tuple)):
        return inorder(tree.left) + [tree.value] + inorder(tree.right)
    raise TypeError(f"Неподдерживаемый тип дерева: {type(tree)}")


def _pretty_print(tree: AnyTree, prefix: str = "", is_left: bool = True) -> None:
    """Выводит дерево в консоль в виде ASCII-графики."""
    if tree is None:
        return
    if isinstance(tree, dict):
        val, left, right = tree["value"], tree["left"], tree["right"]
    else:
        val, left, right = tree.value, tree.left, tree.right
    connector = "|-- " if is_left else "\\-- "
    print(prefix + connector + str(val))
    extension = "|   " if is_left else "    "
    _pretty_print(left,  prefix + extension, is_left=True)
    _pretty_print(right, prefix + extension, is_left=False)


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Binary tree — variant 10")
    print("root=10, height=5, left=root*3+1, right=3*root-1")
    print("=" * 60)

    print("\n[1] dict (height=3):")
    tree_dict = gen_bin_tree(height=3, root=10)
    _pretty_print(tree_dict)
    print(f"    height  : {tree_height(tree_dict)}")
    print(f"    in-order: {inorder(tree_dict)}")

    print("\n[2] namedtuple (height=2):")
    print(f"    {gen_bin_tree_namedtuple(height=2, root=10)}")

    print("\n[3] OrderedDict (height=2):")
    tree_od = gen_bin_tree_ordered_dict(height=2, root=10)
    print(f"    keys: {list(tree_od.keys())}")

    print("\n[4] dataclass (height=2):")
    print(f"    {gen_bin_tree_dataclass(height=2, root=10)}")

    print("\n[5] Full tree (height=5):")
    full = gen_bin_tree()
    print(f"    height  : {tree_height(full)}")
    print(f"    in-order (first 7): {inorder(full)[:7]} ...")
