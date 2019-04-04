import sys
import random


class Perceptron:
    RANDOM_FEATURES = 50
    NUM_FEATURES = 4
    MAX_EPOCHS = 2000
    LEARNING_RATE = 0.025

    def __init__(self, file):
        self.features = []
        self.images = []
        self.weights = []

        self.loadFeatures()
        self.loadImages(file)
        self.training()
        self.classifier()
        self.report()

    def loadFeatures(self):
        self.features = [0] * (self.RANDOM_FEATURES + 1)
        self.weights = [0] * len(self.features)

        self.features[0] = Feature()
        self.weights[0] = -1

        for i in range(len(self.features)):
            self.features[i] = Feature(self.NUM_FEATURES)
            self.weights[i] = -0.5 + random.uniform(0, 1)

    def loadImages(self, file):
        file = open(file, "r")
        # Cleans data into form [comment, dimensions, pixels]
        file = file.read().split("P1\n")
        for i in range(len(file)):
            file[i] = file[i].split("\n")
        file.remove([''])  # removes blank first item
        images = []
        for line in file:
            line[0] = line[0][1:]
            if '' in line:
                line.remove('')
            for i in range(3, len(line)):
                line[2] += line[i]
                line.remove(line[i])
            self.images.append(Image(line[0], line[1], line[2], self.features))

    def training(self):
        highestAccuracy = 0
        pocket = [0] * len(self.features)

        for epoch in range(self.MAX_EPOCHS):
            correct = 0
            for img in self.images:
                outcome = self.classify(img)
                desired = img.getDesiredClass()
                error = desired - outcome
                if error == 0:
                    correct += 1
                    continue
                for featureIndex in range(len(self.features)):
                    self.weights[featureIndex] += error * self.LEARNING_RATE * img.hasFeature(featureIndex)
            if correct > highestAccuracy:
                highestAccuracy = correct
                for i in range(len(self.features)):
                    pocket[i] = Feature(0, self.features[i])
            if correct == len(self.images):
                print("Converged: " + str(epoch) + " epochs")
                return
        self.features = pocket
        print("Did not converge.")

    def classifier(self):
        correct = 0
        for img in self.images:
            outcome = self.classify(img)
            desired = img.getDesiredClass()
            correct += 1 if desired == outcome else 0

        print("Correct: " + str(correct) + "/" + str(len(self.images)))

    def classify(self, img):
        sum = 0
        for featureIndex in range(len(self.features)):
            sum += self.weights[featureIndex] * img.hasFeature(featureIndex)

        return 1 if sum > 0 else 0

    def report(self):
        print("Features:")
        for i in range(len(self.features)):
            print("\tWeight:" + str(round(self.weights[i], 2)) + " Feature: " + self.features[i].toString())

class Feature:

    def __init__(self, numFeatures=0 , old=None):
        if numFeatures == 0 and old is None:
            self.row = None
            self.col = None
            self.sgn = None
        elif numFeatures != 0 and old is None:
            self.row = []
            self.col = []
            self.sgn = []

            for i in range(numFeatures):
                self.row.append(random.randint(0, 9))
                self.col.append(random.randint(0, 9))
                self.sgn.append(random.randint(0, 1) == 1)
        elif not old is None:
            self.row = old.row
            self.col = old.col
            self.sgn = old.sgn

    def evaluate(self, img):
        if self.row is None:
            return 1

        sum = 0
        for i in range(4):
            sum += 1 if img[self.row[i]][self.col[i]] == self.sgn[i] else 0
        return 1 if sum >= 3 else 0

    def toString(self):
        if self.row is None:
            return "Dummy feature"

        s = ""
        for i in range(len(self.sgn)):
            s += "(" + str(self.row[i]) + "," + str(self.col[i]) + "):" + str(self.sgn[i]) + " "
        return s


class Image:

    def __init__(self, type, dimensions, pixels, features):
        self.outcome = 1 if type == "Yes" else 0
        self.width = int(dimensions.split(" ")[0])
        self.height = int(dimensions.split(" ")[1])
        self.img = [[False for i in range(self.width)] for j in range(self.height)]
        c = 0
        for row in range(self.height):
            for col in range(self.width):
                self.img[row][col] = (pixels[c] == '1')
                c += 1

        self.features = [False] * len(features)
        for i in range(len(self.features)):
            self.features[i] = (features[i].evaluate(self.img) == 1)

    def hasFeature(self, index):
        return 1 if self.features[index] else 0

    def getPixel(self, row, col):
        return self.img[row][col]

    def getDesiredClass(self):
        return self.outcome

if(len(sys.argv) > 1):
    Perceptron(sys.argv[1])
else:
    Perceptron("part3/image.data")
