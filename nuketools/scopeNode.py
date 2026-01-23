import nuke

class scopeNode:
    """
    context manager (with statement) to temporarily switch 
    into the given node context and ensure that the original context is restored 
    when exiting the scope.

    Args:
        node (nuke.Group): A Nuke Group-type node to set as the current context.
    """
    def __init__(self, node):
        # validate that the node has a valid context
        self._validate_group(node)
        self.node = node
        self.context = None
        
    def __enter__(self):
        self.begin()
    
    def __exit__(self, exc_type, exc_value, traceback):
        # exc_type, exc_value, traceback: exception info from with block (None if no error)
        self.end()

    def begin(self):
        self.context = nuke.thisGroup()
        self.node.begin()

    def end(self):
        self.node.end()
        if self.context is not None:
            self.context.begin()

    def _validate_group(self, node):
        if not isinstance(node, nuke.Group):
            raise TypeError(f"Expected Group-type node, got {type(node).__name__}")
    
