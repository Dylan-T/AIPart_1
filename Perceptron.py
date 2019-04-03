import sys
import random


class Feature:
    def __init__(self, row, col, values):
        self.row = row
        self.col = col
        self.values = values

        def calculate(image):
            sum = 0
            for i in range(4):
                if image[row[i]][col[i]]:
                    sum += 1
            if sum >= 3:
                return 1
            return 0


class Perceptron:
    def __init__(self):
        self.features = []


class Image:
    values = []
    def __init__(self, type, dimensions, pixels):
        self.type = type
        self.width = int(dimensions.split(" ")[0])
        self.height = int(dimensions.split(" ")[1])
        self.pixels = [[False for i in range(self.width)] for j in range(self.height)]
        c = 0
        for row in range(self.height):
            for col in range(self.width):
                if pixels[c] == '1':
                    self.pixels[row][col] = True
                else:
                    self.pixels[row][col] = False
                c += 1


"""Load images"""
if len(sys.argv) < 2:
    fname = "part3/image.data"
else:
    fname = sys.argv[1]
file = open(fname, "r")

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
    images.append(Image(line[0], line[1], line[2]))
print(str(len(images)) + " images loaded")


"""Construct a set(at least 50) of random features"""
features = []
for h in range(50):
    xcon = [random.randint(0, images[0].width) for i in range(4)]
    ycon = [random.randint(0, images[0].height) for j in range(4)]
    values = [random.randint(0, 1) == 1 for k in range(4)]
    features.append(Feature(xcon, ycon, values))

"""calculate feature values on each image"""


"""Construct a perceptron that uses the features as inputs"""


"""Train the perceptron on the images until either it has presented the whole set of images at least 100 times
or the perceptron weights have converged (ie, the perceptron is correct on all the images)"""
"""
Until the perceptron is always right (or some limit):
    Present an example (+ or -)
    If perceptron is correct:
        do nothing
    if - example wrong:
        subtract feature vector from weight vector
    if + example wrong:
        add feature vector to weight vector
"""

"""Report the number of training cycles to converge
or the number of images still classified incorrectly"""


"""Print out the features and final set of weights"""
