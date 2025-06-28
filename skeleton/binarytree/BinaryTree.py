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
    pass


def postorder(node: TreeNode | None, out: list):
    """Produces a list of the input binary tree in post-order form.

    Args:
        node (TreeNode | None): _description_

    Returns:
        list: _description_
    """
    # visit the left recursively, then right recursively, then the current LRN
    pass


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
    pass 


with open("./utils/binarytree.pkl", "rb") as f:
    make_tree = pickle.load(f)

if __name__ == "__main__":
    root = TreeNode(100)
    root.left = TreeNode(20)
    root.right = TreeNode(200)
    root.left.left = TreeNode(10)
    root.left.right = TreeNode(30)
    root.right.left = TreeNode(150)
    root.right.right = TreeNode(300)
    
    root2 = make_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])

    # # uncomment to test in order here
    # output_list = []
    # inorder(root, output_list)
    # assert output_list == [
    #     10,
    #     20,
    #     30,
    #     100,
    #     150,
    #     200,
    #     300,
    # ], f"Inorder Failed!, result: {output_list}"
    # print(output_list)

    # # uncomment to test preorder here
    # output_list = []
    # preorder(root, output_list)
    # assert output_list == [
    #     100,
    #     20,
    #     10,
    #     30,
    #     200,
    #     150,
    #     300,
    # ], f"Preorder Failed!, result: {output_list}"
    # print(output_list)

    # # uncomment to test postorder here
    # output_list = []
    # postorder(root, output_list)
    # assert output_list == [
    #     10,
    #     30,
    #     20,
    #     150,
    #     300,
    #     200,
    #     100,
    # ], f"Postorder Failed!, result: {output_list}"
    # print(output_list)

    # # uncomment to test levelorder here
    # output_list = levelorder(root)
    # assert output_list == [
    #     100,
    #     20,
    #     200,
    #     10,
    #     30,
    #     150,
    #     300,
    # ], f"Postorder Failed!, result: {output_list}"
    # print(output_list)
