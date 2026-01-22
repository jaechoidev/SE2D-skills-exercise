"""

"""

from scopeNode import scopeNode

def findUpstream(node, filterFn=None)->list:
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
    visited = set()
    filtered = list()
    stack = [node]
    while stack:
        node = stack.pop()
        if node is None or node.fullName() in visited:
            continue
        visited.add(node.fullName())
        if filterFn is None or filterFn(node):
            filtered.append(node.fullName())
            node.setSelected(True)
        if isinstance(node, nuke.Group):
            with scopeNode(node):
                output = node.output() # get the actuall output node of the group
                # filtered |= findUpstream(output, filterFn)
                filtered += findUpstream(output, filterFn)
        stack += [node.input(i) for i in range(node.inputs())]
    print(len(visited))
    return filtered

