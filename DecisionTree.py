import sys

"""Global fields"""
categories = []
attributes = []


class Instance:

    def __init__(self, category, values):
        self.category = category
        self.values = values


class Node:

    def __init__(self, left, right):
        self.left = left
        self.right = right


class LeafNode:
    def __init__(self, c, probability):
        self.c = c
        self.probability = probability


def readDataFile (fname):

    print("Reading data from file " + fname)
    tempf = open(fname, "r")
    file = tempf.read().splitlines()
    tempf.close()

    global categories
    for token in file[0].split("\t"):
        categories.append(token)
    numCategories = len(categories)
    print(str(numCategories) + " categories")

    global attributes
    for token in file[1].split("\t"):
        attributes.append(token)
    numAttributes = len(attributes)
    print(str(numAttributes) + " attributes")

    return readInstances(file)


def readInstances(file):
    """in format: class att1 att2 att3 ..."""
    instances = []
    for line in range(2, len(file)):
        tokens = file[line].split("\t")
        values = []
        for i in range(1, len(tokens)):
            values.append(tokens[i]=='true')
        global categories
        for x in range(len(categories)):
            if categories[x] == tokens[0]:
                category = x
        instances.append(Instance(category, values))

    print("Read " + str(len(instances)) + " instances")
    return instances


def buildTree(instances, attributes):
    if len(instances) == 0:
        # find overall most likely class
        # return LeafNode(class, prob)
        return 0
    elif instances:  # if instances are pure (all same class)
        # return LeafNode(instances[0].category, 1)
        return 0
    elif len(attributes) == 0:
        # count instance classes
        # get most common class
        # return LeafNode(categories[i], count/len(instances))
        return 0
    else:
        for a in attributes:
            """separate instances into two sets depending on their value of the attribute"""

            """Compute purity of each set"""

            """if weighted average purity of these sets is best so far"""
            if True:
                bestAtt = a
                bestInstsTrue = 0  # subset that is true
                bestInstsFalse = 0  # subset that is false
        """Build subtrees using the remaining attributes"""
        attributes.remove(bestAtt)
        left = buildTree(bestInstsTrue, attributes)
        right = buildTree(bestInstsFalse, attributes)
    return Node(bestAtt, left, right)


def evaluateInstance(inst, root):
    if isinstance(root, LeafNode):
        return root.c
    else:
        global attributes
        for i in range(len(attributes)):
            if attributes[i] == root.attribute:
                break
        if inst.values[i]:
            evaluateInstance(inst, root.left)
        else:
            evaluateInstance(inst, root.right)


trainInstances = readDataFile("part2/golf-training.dat")
dTree = buildTree(trainInstances, attributes)

testInstances = readDataFile("part2/golf-test.dat")

predictions = []
correct = 0
# apply tests to tree
for instance in testInstances:
    p = evaluateInstance(instance, dTree)
    if p == instance.category:
        correct += 1
    predictions.append(p)

file = open("result.txt", "w")
for pred in predictions:
    file.write(categories[pred] + "\n")
file.write(str(correct/len(testInstances)) + "\n")
file.close()
sys.exit(0)
