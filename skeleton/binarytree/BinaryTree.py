from collections import deque
import dill as pickle


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder(node: TreeNode | None, out: list):
    """Produces a list of the input binary tree in in-order form.

    Args:
        node (TreeNode | None): _description_

    Returns:
        list: _description_
    """
    # visit the left recursively, then current, then right recursively LNR
    if node:
        inorder(node.left, out)
        out.append(node.val)
        inorder(node.right, out)


def preorder(node: TreeNode | None, out: list):
    """Produces a list of the input binary tree in pre-order form.

    Args:
        node (TreeNode | None): _description_

    Returns:
        list: _description_
    """
    # visit the current, then left recursively, then right recursively NLR
    if node:
        out.append(node.val)
        preorder(node.left, out)
        preorder(node.right, out)


def postorder(node: TreeNode | None, out: list):
    """Produces a list of the input binary tree in post-order form.

    Args:
        node (TreeNode | None): _description_

    Returns:
        list: _description_
    """
    # visit the left recursively, then right recursively, then the current LRN
    if node:
        postorder(node.left, out)
        postorder(node.right, out)
        out.append(node.val)


def levelorder(node: TreeNode | None) -> list:
    """_summary_

    Args:
        node (TreeNode | None): _description_

    Returns:
        list: _description_
    """
    # visit each level from top to bottom, left to right
    q = deque()
    out = []
    if node:
        q.appendleft(node)
    while q:
        cus = q.pop()
        out.append(cus.val)
        if cus.left:
            q.appendleft(cus.left)
        if cus.right:
            q.appendleft(cus.right)
    return out


def has_value(root: TreeNode | None, value) -> bool:
    pass


def insert(root: TreeNode | None, value) -> TreeNode:
    pass


if __name__ == "__main__":
    root = TreeNode(100)
    root.left = TreeNode(20)
    root.right = TreeNode(200)
    root.left.left = TreeNode(10)
    root.left.right = TreeNode(30)
    root.right.left = TreeNode(150)
    root.right.right = TreeNode(300)

    # uncomment to test in order here
    output_list = []
    inorder(root, output_list)
    assert output_list == [
        10,
        20,
        30,
        100,
        150,
        200,
        300,
    ], f"Inorder Failed!, result: {output_list}"
    print(output_list)

    # uncomment to test preorder here
    output_list = []
    preorder(root, output_list)
    assert output_list == [
        100,
        20,
        10,
        30,
        200,
        150,
        300,
    ], f"Preorder Failed!, result: {output_list}"
    print(output_list)

    # uncomment to test postorder here
    output_list = []
    postorder(root, output_list)
    assert output_list == [
        10,
        30,
        20,
        150,
        300,
        200,
        100,
    ], f"Postorder Failed!, result: {output_list}"
    print(output_list)

    # uncomment to test levelorder here
    output_list = levelorder(root)
    assert output_list == [
        100,
        20,
        200,
        10,
        30,
        150,
        300,
    ], f"Levelorder Failed!, result: {output_list}"
    print(output_list)

    # # uncomment to test has_value
    # assert has_value(root, 300), 'has_value missed 300, check right traversal'
    # assert has_value(root, 10), 'has_value missed 10, check left traversal'
    # assert not has_value(None, 1), 'has value failed on empty node'
    # assert not has_value(root, 1), 'has value failed on missing value'

    # # uncomment to test insert
    # tt = TreeNode(100)
    # tt.left = TreeNode(20)
    # tt.left.left = TreeNode(10)
    # tt.left.right = TreeNode(30)
    # tt.right = TreeNode(500)

    # insert(tt, 21)
    # assert tt.left.right.left.val == 21, 'Insert placed 21 in the wrong spot'
    # out = []
    # inorder(tt, out)
    # assert out == sorted(out), 'Insert placed 21 in the wrong spot'
    # print(f"Your inorder BST:{out}")
