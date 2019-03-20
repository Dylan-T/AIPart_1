import numpy
from scipy.spatial import distance
import operator
import sys

"""Load the data"""
if len(sys.argv) > 1:
    trainingText = open(sys.argv[1], "r")
else:
    trainingText = open("part1/iris-training.txt")

trainingData = []
for line in trainingText:
    tokens = line.split()
    trainingData.append((numpy.array((float(tokens[0]), float(tokens[1]), float(tokens[2]), float(tokens[3]))), tokens[4])) #in format [((vector), class), ((vector), class)...((vector), class)]

if len(sys.argv) > 1:
    testingText = open(sys.argv[2], "r")
else:
    testingText = open("part1/iris-test.txt")

testingData = []
for line in testingText:
    tokens = line.split()
    testingData.append((numpy.array((float(tokens[0]), float(tokens[1]), float(tokens[2]), float(tokens[3]))), tokens[4])) #in format [((vector), class), ((vector), class)...((vector), class)]

"""Initialise the value of k"""
k = 5
predictions = []

"""Do this for each test point"""
for test in range(len(testingData)):

    """Calculate the distance between test data and each row of training data."""
    distances = []
    for train in range(len(trainingData)):
        dist = numpy.linalg.norm(testingData[test][0]-trainingData[train][0])
        distances.append([dist,trainingData[train][1]])


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
    predictions.append( max(classes, key=classes.get))

"""write predictions to a txt file"""
f=open("resultsK"+str(k)+".txt", "w+")
for i in predictions:
    f.write(i + "\n")
f.close()