"""

"""
import re

def replaceNode(sourceClass, targetClass, node=None):
    # 1. Filters by Scope
    if node is None:
        nodes = nuke.allNodes(sourceClass)
    else:
        node_names = findUpstream(nuke.toNode(node), filterFn=lambda n: n.Class() == sourceClass)
        nodes = [nuke.toNode(n) for n in node_names]
    # deselect all NOT to mess up while creating new nodes
    [n.setSelected(False) for n in nuke.allNodes(recurseGroups=True)]

    # 2. Executes Seamless Replacement
    replacements = []  # List[tuple] : [(old_node, new_node, inputs, deps_info)]
    old_to_new = {}    # mapping old_node : new_node

    for old_node in nodes:
        with scopeNode(old_node.parent()):
            new_node = nuke.createNode(targetClass, inpanel=False)
            new_node.setXpos(old_node.xpos())
            new_node.setYpos(old_node.ypos())
        
        # input connections
        inputs = [old_node.input(i) for i in range(old_node.inputs())]
        
        # dependent connections
        deps_info = []
        for dep in old_node.dependent(nuke.INPUTS):
            for i in range(dep.inputs()):
                if dep.input(i) == old_node:
                    deps_info.append((dep, i))    
        replacements.append((old_node, new_node, inputs, deps_info))
        old_to_new[old_node] = new_node

    # 3. Restores Graph Topology
    for old_node, new_node, inputs, deps_info in reversed(replacements):
        for i, inp in enumerate(inputs):
            # connect to new node when input is old node
            if inp in old_to_new:
                new_node.setInput(i, old_to_new[inp])
            else:
                new_node.setInput(i, inp)
        for dep, i in deps_info:
            # only when dep requires replacement
            if dep not in old_to_new:
                dep.setInput(i, new_node)
                
    # 4. Synchronizes Knob Data
    # There might be cleaner way
        skip_knobs = {'name', 'xpos', 'ypos', 'selected'}
        for key in old_node.knobs():
            if key in skip_knobs or key not in new_node.knobs():
                continue
            try:
                new_node[key].fromScript(old_node[key].toScript())
            except:
                pass

    # 5. Script Expressions
    for old_node, new_node, _, _ in reversed(replacements):
        for dep in old_node.dependent(nuke.EXPRESSIONS): # only check expression refered nodes
            for knob in dep.knobs().values():
                if knob.hasExpression():
                    script = knob.toScript()
                    new_script = re.sub(rf'\b{old_node.name()}\b', new_node.name(), script)
                    if script != new_script:
                        knob.fromScript(new_script)
    
    # 6. Remove old nodes
    for old_node, _, _, _ in replacements:
        nuke.delete(old_node)
