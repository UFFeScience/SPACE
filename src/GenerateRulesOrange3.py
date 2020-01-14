import Orange
import math
import re
import sys

def format_conf_rule(rule, id):
    # get relational operator
    operator = ""
    if (rule.__contains__(">")):
        operator = '>'
    elif (rule.__contains__("<")):
        operator = '<'
    elif (rule.__contains__("≤")):
        operator = '=<'
    elif (rule.__contains__("≥")):
        operator = '>='
    elif (rule.__contains__(":")):
        operator = '='

    # clean string
    filter = re.sub("[≥≤<>:'\[\]]", "", rule)
    filter = filter.replace(" ", "", 1)

    # format string
    j = filter.split(" ")
    if(j[0].__contains__(".000")):
        k=2
        while j[1] == '':
            j[1] = j[k]
            j[k] = ''
            k = k+1
        k = 3
        while j[2] == '':
            j[2] = j[k]
            k = k + 1
        conf = "conf(" + str(id) + "," + j[1] + ",Y):-" + j[1] + "(Y),Y>" + j[0].replace(".000", "") + ",Y=<" + j[2].replace(".000", "") + "."
    else:
        k = 2
        while j[1] == '':
            j[1] = j[k]
            k = k + 1
        # set string conf rule
        conf = "conf(" + str(id) + "," + j[0] + ",Y):-" + j[0] + "(Y),Y" + operator + j[1].replace(".000","") + "."

    return conf

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
        rules = s.split(",")
        for rule in rules:
            conf = format_conf_rule(rule, id)
            print ("%s" % conf)
            arq.write(conf + "\n")
    return id

def set_rules_situation(node, arq, id):
    if not node:
        return
    if node.children:
        for i in range(len(node.children)):
            id = set_rules_situation(node.children[i], arq, id)
            id = id + 1
    else:
        values = node.value
        values = re.sub("[\[\] ]", "", str(values)).split(".")
        max_value = node.value.max()
        if int(values[0]) == int(max_value):
            percent = (int(values[0]) / (int(values[0]) + int(values[1]) + int(values[2])))*100
            arq.write(":- discontiguous(confBaixo/" + str(id) + ").\n")
            arq.write("confBaixo(" + str(id) + "," + str(math.ceil(percent)) + ").\n")
        elif int(values[1]) == int(max_value):
            percent = (int(values[1]) / (int(values[0]) + int(values[1]) + int(values[2])))*100
            arq.write(":- discontiguous(confMedio/" + str(id) + ").\n")
            arq.write("confMedio(" + str(id) + "," + str(math.ceil(percent)) + ").\n")
        else:
            percent = (int(values[2]) / (int(values[0]) + int(values[1]) + int(values[2])))*100
            arq.write(":- discontiguous(confAlto/" + str(id) + ").\n")
            arq.write("confAlto(" + str(id) + "," + str(math.ceil(percent)) + ").\n")

    return id


def tree_rules(x):
    arq = open('teste.pl', 'w')
    id  = 0;
    if isinstance(x, Orange.tree.TreeModel):
        if(x.root.children):
            for i in range(len(x.root.children)):
                id = get_rules(x.root.children[i], arq, id)
            id = 0;
            for i in range(len(x.root.children)):
                id = set_rules_situation(x.root.children[i], arq, id)
    else:
        raise TypeError("invalid parameter")
    arq.write("confPMedio(I,X,Y):-conf(I,X,Y), confMedio(I,_).\n")
    arq.write("confPBaixo(I,X,Y):-conf(I,X,Y), confBaixo(I,_).\n")
    arq.write("confPAlto(I,X,Y):-conf(I,X,Y), confAlto(I,_).")
    arq.close()

# Execution params
if(len(sys.argv) == 1):
    path = "Teste5.csv"
    depth = 2
elif(len(sys.argv) == 3):
    path = sys.argv[1]
    depth = int(sys.argv[2])
else:
    raise ("ERROR: Execution: python <file.py> <path_of_csv> <tree_depth>")

data = Orange.data.Table(path)
learner = Orange.classification.TreeLearner(max_depth=depth)
classifier = learner(data)
tree_rules(classifier)

#print(dir(Orange.evaluation.scoring))
#l = [learner];
#teste = Orange.evaluation.testing.CrossValidation(data, l)
#print (Orange.evaluation.scoring.AUC(teste)[0])
#print (Orange.evaluation.scoring.CA(teste)[0])
