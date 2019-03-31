import sys

"""Global fields"""
categories = []
allAttributes = []
attributes = []
allInstances = []


class Instance:
    def __init__(self, category, values):
        self.category = category
        self.values = values


class Node:
    def __init__(self, a, left, right):
        self.a = a
        self.left = left
        self.right = right


class LeafNode:
    def __init__(self, c, probability):
        self.c = c
        self.probability = probability


def readDataFile(fname):

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
            values.append(tokens[i] == 'true')
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
        global allInstances
        catCount = [0] * len(categories)
        for i in allInstances:
            catCount[i.category] += 1

        cat = catCount.index(max(catCount))

        return LeafNode(cat, max(catCount)/len(allInstances))

    elif getImpurity(instances) == 0:  # if instances are pure (all same class)
        return LeafNode(instances[0].category, 1)
    elif len(attributes) == 0:
        # count instance classes
        # get most common class
        # return LeafNode(categories[i], count/len(instances))
        return 0
    else:
        minImpurity = 2
        bestInstsTrue = []
        bestInstsFalse = []
        for a in attributes:
            """separate instances into two sets depending on their value of the attribute"""
            tInsts = []
            fInsts = []
            for i in instances:
                if i.values[getAttributeIndex(a)]:
                    tInsts.append(i)
                else:
                    fInsts.append(i)

            """Compute purity of each set"""
            tImpurity = getImpurity(tInsts)
            fImpurity = getImpurity(fInsts)

            """if weighted average purity of these sets is best so far"""
            """WAP = P(nodei)*impurity(nodei)"""
            waImp = (len(tInsts)/(len(tInsts) + len(fInsts)))*tImpurity + (len(fInsts)/(len(tInsts) + len(fInsts)))*fImpurity
            if waImp < minImpurity:
                minImpurity = waImp
                bestAtt = a
                bestInstsTrue = tInsts
                bestInstsFalse = fInsts
        """Build subtrees using the remaining attributes"""
        attributes.remove(bestAtt)
        left = buildTree(bestInstsTrue, attributes)
        right = buildTree(bestInstsFalse, attributes)
    return Node(bestAtt, left, right)


def getImpurity(instances):
    """Count classes"""
    m = 0
    n = 0
    for i in instances:
        if i.category == 0:
            m += 1
        if i.category == 1:
            n += 1
    if m == 0 or n == 0:
        return 0
    return (m*n)/(m+n)**2


def evaluateInstance(inst, root):
    if isinstance(root, LeafNode):
        return root.c
    else:
        i = getAttributeIndex(root.a)
        if inst.values[i]:
            return evaluateInstance(inst, root.left)
        else:
            return evaluateInstance(inst, root.right)


def getAttributeIndex(attribute):
    global allAttributes
    for i in range(len(allAttributes)):
        if allAttributes[i] == attribute:
            return i


def treeToText(root, indent):
    result = ""
    for i in range(indent):
        result += "\t"

    if isinstance(root, LeafNode):
        result += "Class " + categories[root.c] + ", prob = " + str(root.probability) + "\n"
    else:
        result += root.a + " = " + " True:\n"
        result += treeToText(root.left, indent+1)

        for i in range(indent):
            result += "\t"
        result += root.a + " = " + " False:\n"
        result += treeToText(root.left, indent + 1)

    return result


"""Take args"""
if len(sys.argv) > 2:
    trainFile = sys.argv[1]
    testFile = sys.argv[2]
else:
    trainFile = "part2/golf-test.dat"
    testFile = "part2/golf-training.dat"

"""Read training data"""
trainInstances = readDataFile(trainFile)
allInstances = trainInstances.copy()
allAttributes = attributes.copy()

"""Build the tree"""
dTree = buildTree(trainInstances, attributes)
print(treeToText(dTree, 0))

"""Read testing data"""
tempf = open(testFile, "r")
file = tempf.read().splitlines()
tempf.close()
testInstances = readInstances(file)

"""evaluate test data using decision tree"""
predictions = []
correct = 0
for instance in testInstances:
    p = evaluateInstance(instance, dTree)
    if p == instance.category:
        correct += 1
    predictions.append(p)

print(correct)
print(predictions)
"""Output the results"""
# file = open("result.txt", "w")
# for pred in predictions:
#     file.write(categories[pred] + "\n")
# file.write(str(correct/len(testInstances)) + "\n")
# file.close()


sys.exit(0)
