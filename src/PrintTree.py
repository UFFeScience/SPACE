import Orange

def tree_size(node):
    if not node:
        return 0
    size = 1
    if node.branch_selector:
        for branch in node.branches:
            size += tree_size(branch)
    return size


def print_tree1(node, level):
    if not node:
        print (" " * level + "<null node>")
        return
    if node.branch_selector:
        node_desc = node.branch_selector.class_var.name
        node_cont = node.distribution
        print ("\\n" + "   " * level + "%s (%s)" % (node_desc, node_cont))
        for i in range(len(node.branches)):
            print ("\\n" + "   " * level + ": %s" % node.branch_descriptions[i])
            print_tree0(node.branches[i], level + 1)
    else:
        node_cont = node.distribution
        major_class = node.node_classifier.default_value
        print ("--> %s (%s) " % (major_class, node_cont))

def print_tree0(node, level, s):
    if not node:
        print (" " * level + "<null node>")
        return
    if node.branch_selector:
        node_desc = node.branch_selector.class_var.name
        for i in range(len(node.branches)):
            m = s + "(" + str(node_desc) + " " + str(node.branch_descriptions[i])+ ")"
            print_tree0(node.branches[i], level + 1, m)
    else:
        s = s + " THEN " + str(node.node_classifier.default_value) + "(" + str(node.distribution) + ")\n"
        print ("%s" % s)

def print_tree(x):
    s = "IF "
    if isinstance(x, Orange.classification.tree.TreeLearner):
        print_tree0(x, 0, s)
    elif isinstance(x, Orange.classification.tree.Node):
        print_tree0(x, 0, s)
    else:
        raise TypeError("invalid parameter")

data = Orange.data.Table("Teste5.csv")
learner = Orange.classification.TreeLearner(max_depth=2)
classifier = learner(data)
print (classifier.print_tree())
print (classifier.leaf_count())
print (dir (Orange.tree.TreeModel))
print (dir (classifier))

classifier.rule(classifier.root.children[0].children[0])

#print (classifier)
#print (classifier.get_values())
#print (classifier.print_tree)
#


#print_tree(tree_classifier.tree)
#print tree_size(tree_classifier.tree)
