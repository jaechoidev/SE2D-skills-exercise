# Software Engineer - 2D Skills Exercise

## Step 1 - Context Management in Groups

### Background
In the Nuke Python API, using the with keyword for Group nodes does not restore the
original parent node context when exiting the scope. Instead, it sets it to the parent of the
node used in the scope, which can lead to nodes being created in the wrong context.

### Task
Implement a Python class scopeNode(node) that can be used as a context manager
(with statement) to temporarily switch into the given node context and ensure that the
original context is restored when exiting the scope.
Make sure to demonstrate that your work is behaving correctly

### Example Usage
```Python
with scopeNode(node):
    nuke.createNode("Blur") # This node should be created inside `node`
# Outside the with block, the original context should be restored.
nuke.createNode("Grade")
```

### Approach
- check existing discussion on the behavior as it does not look like ideal behavior
    - post 1[^1]
    - post 2[^2]
- learn more about with, PEP343 - The `with` statement[^3]
- check which nodes have `begin`,`end`,`__enter__` or `__exit__`, which can be assumed having context.
```Python
ctx_nodes = []
for name in dir(nuke):
    obj = getattr(nuke, name)
    if isinstance(obj, type) and issubclass(obj, nuke.Node):
        if hasattr(obj, 'begin'):
            ctx_nodes.append(name)
print(ctx_nodes)
# Result: ['Gizmo', 'Group', 'LiveGroup', 'Precomp', 'Root']
# all of these are subclasses of Group
```


## Step 2 - Upstream Node Search with Filtering

### Background
Given that nodes can be nested into groups, you often need to traverse the graph to find
specific nodes upstream of a given node.

### Task
Using the context manager implemented in ## Step 1, implement a Python function:

```Python
def findUpstream(node, filterFn=None):
"""
Find all upstream nodes for a given node using traversal algorithm.
Args:
node (nuke.Node): The node to start from.
filterFn (callable, optional): Optional function to filter nodes.
Should return True for nodes to keep.
Returns:
list of nuke.Node: List of nodes upstream of the given node that
satisfy the filter.
"""
```
Requirements
1. Use a graph algorithm to traverse upstream nodes.
2. Respect the filterFn to only return nodes that match a condition (e.g., lambda n: n.Class() == "Blur").

### Example Usage
```Python
blur_nodes = findUpstream(write_node, filterFn=lambda n: n.Class() == "Blur")
```

### Approach
- Implement DFS type of algorithm (BFS would be fine) to traverse upstream nodes.
- We need to traverse inside if the node has context, so use the result of step1.


## Step 3 - Node Replacement

### Background
It is often necessary to swap one tool for another—such as replacing a standard node with a
custom Gizmo or upgrading an outdated plugin. Doing this manually in a large script is
time-consuming and risks breaking complex connections and expressions.

### Task
Implement a Python function replaceNode(sourceClass, targetClass,
node=None) that:
1. Filters by Scope: Finds all nodes of sourceClass that exist upstream of the
specified node. If no node is provided, it should target all nodes of that class in the
script.
2. Executes Seamless Replacement: Creates a node of targetClass for every
instance found, ensuring it inherits the X/Y position of the original.
3. Restores Graph Topology: Automatically reconnects all input pipes and reroutes all
downstream nodes (outputs) so the new node sits exactly where the old one was.
4. Synchronizes Knob Data: Iterates through all knobs; if a knob name exists in both the
source and target nodes, copy the value or the animation/expression across.
5. Script Expressions: Searches the entire Nuke script for any TCL expressions that
reference the old node's name and updates them to reference the new node's name.

### Example Usage
```Python
# Replaces all "Blur" nodes upstream of "Write1" with "Defocus" nodes
replaceNode("Blur", "Defocus", "Write1")
```

### Approach
- task1 uses step2 and `nuke.allNodes(sourceClass)`
- search for a way to copy knobs[^4], but it seems better to check each knobs
- reconnects means, disconnect and reconnect, inputs and outputs
- find expressions that reference ethe old node and replace them
- what if the expression is not valid? remove it or not?

## Step 4 - Node Replacement

### Background
You will be provided a Nuke script (replace_node_test.nk) to demonstrate the results of
your work so far.

### Task
Use the node replacement tool to find all Blur nodes upstream of "Write1" and replace
them for Defocus nodes.
Save the modified Nuke script with a new name for us to review.



## Results
### Limitations

### Potential improvements
- currently it's not checking if the expression is valid after replacing nodes. For example, `parent.Blur2.size*2` changed into `parent.Defocus1.size*2`, but Defocus does not have size knob. Maybe good to validate and delete it or,
- it would be good to have custom mapping while replacing nodes. For example, blur['size'] could be interpreted Defocus['defocus']. 
- scopeNode assumes that it expects Group-type (Group node or subclasses of Group node). It is not necessary to generalize more now, but might be better.

### Modified nuke script 


### References
[^1]: https://community.foundry.com/discuss/topic/156600/nuke-root-begin-breaks-code
[^2]: https://community.foundry.com/discuss/topic/158875/issues-with-context-when-creating-nodes
[^3]: https://peps.python.org/pep-0343/
[^4]: https://learn.foundry.com/nuke/developers/16.0/pythondevguide/_autosummary/nuke.Node.html?highlight=nuke%20node#nuke.Node.writeKnobs
