"""
Author: Tarun Ambati
Last updated: July 26, 2026
Description: Defines the TreeNode class used to build and search the
Engineering faculty roster tree. Each node stores a name, node type,
optional data, parent reference, and list of child nodes.
"""

"""
We really only use 2 out of 6 methods, add_child() & find(). The rest are not used in the program, but they are useful for different use cases.
"""
from enum import Enum


class TreeNode:
    def __init__(self, name, node_type, data=None):
        self.name = name
        self.node_type = node_type
        self.data = data
        self.parent = None  
        self.children = []


    def add_child(self, child) -> None:
        """Add the given TreeNode as a child of the current node.

        The child is appended to this node's children list, and the
        child's parent reference is updated so it points back to this
        current node.
        """
        self.children.append(child)
        child.parent = self


    def remove_child(self, child) -> None:
        """Remove the given TreeNode from this node's children.

        If the child exists in the children list, it is removed and its
        parent reference is cleared. If the child is not present, the
        method leaves the tree unchanged.
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None


    def is_leaf(self) -> bool:
        """Return True if this node has no children.

        A leaf node is a node at the end of a branch, meaning it does not
        have any child nodes below it.
        """
        return len(self.children) == 0


    def depth(self) -> int:
        """Return this node's depth in the tree.

        Depth is the number of edges from the root node to the current
        node. The root has depth 0, its children have depth 1, and so on.
        """
        depth = 0
        current = self

        while current.parent is not None:
            depth += 1
            current = current.parent

        return depth


    def height(self) -> int:
        """Return this node's height in the tree.

        Height is the number of edges on the longest path from this node
        down to one of its leaf nodes. A leaf node has height 0.
        """
        if self.is_leaf():
            return 0

        child_heights = []
        for child in self.children:
            child_heights.append(child.height())

        return 1 + max(child_heights)


    def find(self, name):
        """Search this node and its descendants for the given name.

        The method performs a recursive depth-first traversal. It checks
        the current node first, then searches each child subtree. It
        returns the matching TreeNode if one is found, or None if the name
        does not appear in this part of the tree.
        """
        if self.name == name:
            return self

        for child in self.children:
            result = child.find(name)
            if result is not None:
                return result

        return None


    def print_tree(self, indent=0):
        """ Prints the tree with indentation. """
        print("    " * indent + str(self))

        for child in self.children:
            child.print_tree(indent + 1)


    def __str__(self):
        return self.name
    

    class NodeType(Enum):
        SCHOOL = "School"
        PROGAM = "Program"
        FACULTY = "Faculty"

        @classmethod
        def init_from_str(cls, node_type):
            return cls[node_type.strip().upper()]

if __name__ == "__main__":
    root = TreeNode("Engineering", TreeNode.NodeType.SCHOOL)

    comp_e = TreeNode("CompE", TreeNode.NodeType.PROGAM)
    root.add_child(comp_e)

    ee = TreeNode("EE", TreeNode.NodeType.PROGAM)
    root.add_child(ee)

    kubota = TreeNode("Kubota", TreeNode.NodeType.FACULTY)
    comp_e.add_child(kubota)

    qin = TreeNode("Qin", TreeNode.NodeType.FACULTY)
    comp_e.add_child(qin)

    root.print_tree()