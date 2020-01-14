import Orange
import re

def get_rules(node, arq, id):
    if not node:
        return
    if node.children:
        for i in range(len(node.children)):
            id = get_rules(node.children[i], arq, id)
            id = id + 1
    else:
        s = classifier.rule(node)
        s = str(s)
        print(s)
        rules = s.split(",")
        for i in range(len(rules)):

            filter = re.sub("[≤<>:'\[\]]", "", rules[i])
            filter = filter.replace(" ", "", 1)
            j = filter.split(" ")
            k=2
            while j[1] == '':
                j[1] = j[k]
                k = k +1
            conf = "conf(" + str(id) + "," + j[0] + "," + j[1].replace(".000","") + ")."
            print ("%s" % conf)
            arq.write(conf + "\n")

        values = node.value
        values = re.sub("[\[\] ]", "", str(values)).split(".")
        max_value = node.value.max()
        if int(values[0]) == int(max_value):
            arq.write("confBaixo(" + str(id) + ").\n")
        elif int(values[1]) == int(max_value):
            arq.write("confMedio(" + str(id) + ").\n")
        else:
            arq.write("confAlto(" + str(id) + ").\n")

    return id


def tree_rules(x):
    arq = open('teste.pl', 'w')
    id  = 0;
    if isinstance(x, Orange.tree.TreeModel):
        if(x.root.children):
            for i in range(len(x.root.children)):
                id = get_rules(x.root.children[i], arq, id)
    else:
        raise TypeError("invalid parameter")
    arq.close()

data = Orange.data.Table("Teste5.csv")
learner = Orange.classification.TreeLearner(max_depth=2)
classifier = learner(data)
tree_rules(classifier)
