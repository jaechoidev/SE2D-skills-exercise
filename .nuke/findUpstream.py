"""

"""

from scopeNode import scopeNode

def findUpstream(node, filterFn=None):
    """
    Find all upstream nodes for a given node using traversal algorithm (DFS).
    Args:
        node (nuke.Node): The node to start from.
        filterFn (callable, optional): Optional function to filter nodes.
        Should return True for nodes to keep.
    Returns:
        list of nuke.Node: List of nodes upstream of the given node that
        satisfy the filter.
    """    
    def _traverse(node):
        stack = [node]
        while stack:
            node = stack.pop()
            if node is None or node.fullName() in visited:
                continue
            visited.add(node.fullName())
            if filterFn is None or filterFn(node):
                filtered.add(node.fullName())
                node.setSelected(True)
            if isinstance(node, nuke.Group):
                with scopeNode(node):
                    output = node.output()
                    _traverse(output)
            stack += [node.input(i) for i in range(node.inputs())]
    visited = set()
    filtered = set()
    _traverse(node)
    return list(filtered)
