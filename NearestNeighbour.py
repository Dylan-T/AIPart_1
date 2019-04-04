import math
import sys

"""Load the training data"""
if len(sys.argv) > 1:
    trainingText = open(sys.argv[1], "r")
else:
    trainingText = open("part1/iris-training.txt")
trainingText = trainingText.read().splitlines()

trainingData = []  # in format [[[vector], class], ((vector), class)...((vector), class)]
for line in trainingText:
    tokens = line.split()
    if len(tokens) == 5:
        trainingData.append([[float(tokens[0]), float(tokens[1]), float(tokens[2]), float(tokens[3])], tokens[4]])

"""Find the dimension ranges"""
rMax = [trainingData[0][0][0], trainingData[0][0][1], trainingData[0][0][2], trainingData[0][0][3]]
rMin = [trainingData[0][0][0], trainingData[0][0][1], trainingData[0][0][2], trainingData[0][0][3]]
r = []
for f in trainingData:
    for i in range(4):
        if f[0][i] > rMax[i]:
            rMax[i] = f[0][i]
        if f[0][i] < rMin[i]:
            rMin[i] = f[0][i]
r = [rMax[0] - rMin[0], rMax[1] - rMin[1], rMax[2] - rMin[2], rMax[3] - rMin[3]]

"""Load the testing data"""
if len(sys.argv) > 1:
    testingText = open(sys.argv[2], "r")
else:
    testingText = open("part1/iris-test.txt")

testingData = []  # in format [((vector), class), ((vector), class)...((vector), class)]
actualClass = []
for line in testingText:
    tokens = line.split()
    testingData.append(((float(tokens[0]), float(tokens[1]), float(tokens[2]), float(tokens[3])), tokens[4]))
    actualClass.append(tokens[4])

"""Initialise the value of k"""
k = 1
predictions = []

"""Do this for each test point"""
for test in range(len(testingData)):

    """Calculate the distance between test data and each row of training data."""
    distances = []
    for train in range(len(trainingData)):
        dist = 0
        # Distance calculation
        for i in range(4):
            dist += (testingData[test][0][i] - trainingData[train][0][i])**2 / r[i]
        dist = math.sqrt(dist)
        distances.append([dist, trainingData[train][1]])

    """Sort the calculated distances in ascending order based on distance values"""
    distances.sort()

    """Get top k rows from the sorted array"""
    """Get the most frequent class of these rows"""
    classes = {}

    for x in range(k):
        if distances[x][1] in classes:
            classes[distances[x][1]] = classes[distances[x][1]]+1
        else:
            classes[distances[x][1]] = 1

    """Add predicted class to list"""
    predictions.append(max(classes, key=classes.get))

correct = 0
print("| Actual : Prediction |")
for i in range(len(predictions)):
    print("| " + actualClass[i] + " : " + predictions[i] + " |")
    if predictions[i] == actualClass[i]:
        correct += 1
print("Correct: " + str(correct) + "/" + str(len(predictions)))

"""write predictions to a txt file"""
# f = open("resultsK"+str(k)+".txt", "w+")
# for i in predictions:
#     f.write(i + "\n")
# f.write(str(correct) + "/" + str(len(predictions)))
# f.close()
#
