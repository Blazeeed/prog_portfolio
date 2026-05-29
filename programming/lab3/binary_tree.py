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
