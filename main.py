import csv
import random
import math
import operator 
import sys
import time
 
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        maxTrainData = int(split * len(dataset))
        for x in range(0, len(dataset)):
            for y in range(14):
                dataset[x][y] = float(dataset[x][y])
            if x < maxTrainData:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])
 
 
def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)
 
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors
 
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]
 
def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0
    
def main():
    startTime = time.time()
    # prepare data
    trainingSet=[]
    testSet=[]
    split = 0.75
    if (len(sys.argv) > 1):
        if sys.argv[1] == "0.75" or sys.argv[1] == "0.8" or sys.argv[1] == "0.9":
            split = float(sys.argv[1])
        else:
            print 'WARNING:\nRatio\'s accepted value is 0.75, 0.8, or 0.9\nUsing default instead'
    loadDataset('datasets/adult_5k.data', split, trainingSet, testSet)
    print '\n'
    print 'Train ratio: ' + repr(split)
    print 'Train set: ' + repr(len(trainingSet))
    print 'Test set: ' + repr(len(testSet))
    print 'Calculating ...'
    # generate predictions
    predictions=[]
    k = 3
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        # print('> ' + str(x) + ' predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(round(accuracy,2)) + '%')
    print('Program runs for ' + str(round(time.time() - startTime, 2)) + ' seconds')
    
main()