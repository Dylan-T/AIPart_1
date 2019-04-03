import sys
import random


class Image:

    def __init__(self, type, dimensions, pixels, features):
        if type == "Yes":
            self.type = 1
        else:
            self.type = 0

        self.width = int(dimensions.split(" ")[0])
        self.height = int(dimensions.split(" ")[1])
        self.pixels = [[False for i in range(self.width)] for j in range(self.height)]
        c = 0
        for row in range(self.height):
            for col in range(self.width):
                self.pixels[row][col] = (pixels[c] == '1')
                c += 1

        self.features = features

    def hasFeature(self, index):
        if self.features[index]:
            return 1
        else:
            return 0


class Feature:
    def __init__(self, feature, isDummy):
        if isinstance(feature, Feature):
            self.row = feature.row
            self.col = feature.col
            self.values = feature.values
        elif isDummy:
            self.isDummy = True
            self.row = None
            self.col = None
            self.values = None
        else:
            self.col = [random.randint(0, 10) for i in range(4)]  # needs image dimensions (hard coded for now)
            self.row = [random.randint(0, 10) for j in range(4)]
            self.values = [random.randint(0, 1) == 1 for k in range(4)]


    def evaluate(self, image):
        sum = 0
        for i in range(4):
            if image[self.row[i]][self.col[i]]:
                sum += 1
        if sum >= 3:
            return 1
        return 0


class Perceptron:
    images = []
    features = []
    weights = []

    MAX_EPOCH = 2000
    LEARNING_RATE = 0.025

    def __init__(self, filename):
        self.loadFeatures()
        print("Features loaded")
        self.loadImages(filename)
        print("Images loaded")
        self.train()
        print("Perceptron trained")

    def loadImages(self, filename):
        file = open(filename, "r")

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


    def loadFeatures(self):
        self.features.append(Feature(0, True))  # Dummy feature
        self.weights.append(0)
        for h in range(49):
            self.features.append(Feature(0, False))
            self.weights.append(0)  # -.5 + randomDouble

    def train(self):
        maxAcc = 0
        pocket = [0] * len(self.features)

        for epoch in range(self.MAX_EPOCH):
            correct = 0

            for image in self.images:
                outcome = self.classify(image)
                expected = image.type

                if(outcome == expected):
                    correct += 1
                else:
                    error = expected - outcome
                    for featureI in range(len(self.features)):
                        self.weights[featureI] += error * self.LEARNING_RATE * image.hasFeature(featureI)

            if correct > maxAcc:
                maxAcc = correct
                for i in range(len(self.features)):
                    pocket[i] = Feature(self.features[i], False)

            if correct == len(self.images):
                return  # HAS CONVERGEDs

        self.features = pocket  # DID NOT CONVERGE

    def classify(self, image):
        sum = 0
        for featureI in range(len(self.features)):
            sum += self.weights[featureI] * image.hasFeature(featureI)
        if sum > 0:
            return 1
        return 0



"""Get args if possible"""
if len(sys.argv) < 2:
    fname = "part3/image.data"
else:
    fname = sys.argv[1]

"""Create and train perceptron"""
perceptron = Perceptron(fname)
print("Perceptron created")

for i in perceptron.images:
    correct = 0
    prediction = perceptron.classify(i)
    actual = i.type
    if prediction == actual:
        correct += 1
print("Correct: " + str(correct) + "/" + str(len(perceptron.images)))
