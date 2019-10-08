from parser import *
from copy import deepcopy
import time
import matplotlib.pyplot as plt

# N = 30
# K = 5
# sqne = 5
# pose = 0



class ExactAlgorithm:
    MAXVAL = 10000

    def __init__(self, N, K, sqne, pose):
        self.values = getValuesFromUrl(N, K, sqne, pose)
        self.path = ""
        self.cost = 0
        self.minPath = ""
        self.N = N
        self.K = K
        self.bestPath = ""
        self.bestNumOfUsed = 0
        self.position = 0


    # gets cost matrix and visited matrix for specified position
    def setUpForPosition(self, position):
        self.costMatrix = getMatrixOfCosts(self.values[position])
        self.visited = np.zeros(self.costMatrix.shape[0])
        self.position = position
        # set this up for every position so that it gets reduced over time each time
        self.minCost = MAXVAL
        
        self.maxPathLen = 0
        if(self.position==0):
            self.maxPathLen = self.K - 1
        self.maxPathLen = self.maxPathLen + (position+1) * self.N // 5
        self.bestFitness = -MAXVAL
        # print("setUpForPosition", position, ": maxPathLen =", self.maxPathLen)

    def findBestRoute(self):
        nothing = 0
    
    def calculateFitness(self, cost, numOfUsedPoints):
        return numOfUsedPoints - cost

    def dfs(self, startPoint, visitedPoints, costNow, pathNow, numOfUsed):
        cost = deepcopy(costNow)
        path = deepcopy(pathNow)
        visited = deepcopy(visitedPoints)
        visited[startPoint] = 1
        allVisitedFlag = True
        if (len(path) > self.maxPathLen):
            # print("maxPathLen =", self.maxPathLen, "and localPathLen =", len(path))
            # print("too long path but i shouldn't be here i think")
            # no point in even trying to go deeper
            return

        for nextPoint, nextPointCost in enumerate(self.costMatrix[startPoint]):
            # print("my depth:", depth, "preparing to visit next with visited value of", visited[nextPoint])
            # print("my depth:", depth, "path right now", path)
            # we haven't visited it yet
            if(visited[nextPoint] == 0):
                # print("my depth:", depth, "preparing to visit next")
                allVisitedFlag = False
                localCost = cost + nextPointCost
                nextPointValue = self.values[self.position][nextPoint]
                localPath = path + nextPointValue[-nextPointCost:]
                
                if (len(localPath) > self.maxPathLen):
                    # print("maxPathLen =", self.maxPathLen, "and localPathLen =", len(localPath), "and pathLen =", len(path))
                    # too long path
                    # calculate based on previous path
                    calculatedFitness = self.calculateFitness(cost, numOfUsed)
                    if (calculatedFitness > self.bestFitness):
                        self.bestFitness = calculatedFitness
                        self.bestPath = deepcopy(path)
                        self.cost = deepcopy(cost)
                        self.bestNumOfUsed = deepcopy(numOfUsed)
                        # print("New best path found! fitness:", self.bestFitness, "and path:", self.bestPath)
                else:
                    self.dfs(nextPoint, visited, localCost, localPath, numOfUsed + 1)

        if (allVisitedFlag):
            calculatedFitness = self.calculateFitness(cost, numOfUsed)
            if (calculatedFitness > self.bestFitness):
                self.bestFitness = calculatedFitness
                self.bestPath = deepcopy(path)
                self.cost = deepcopy(cost)
                self.bestNumOfUsed = deepcopy(numOfUsed)
                # print("New best path found! fitness:", self.bestFitness, "and path:", self.bestPath)
            # self.minCost = deepcopy(cost)
            # needed as the minCost is just a check to see if things get better
            # self.cost = deepcopy(cost)
            # self.minPath = deepcopy(path)
            # print("New best path found! with cost:", self.minCost, "and path:", self.minPath)

    def removeAlreadyUsed(self, path):
        # print("---------\nstarting removeAlreadyUsed")
        alreadyUsed = []
        for i in range(len(path) - self.K + 1):
            alreadyUsed.append(path[i:i+self.K])

        # print("alreadyUsed values", alreadyUsed)
        # print("values before removal", self.values)
        self.values[:] = [x for x in self.values if x not in alreadyUsed]
        # print("values after removal", self.values)
        # print("---------\n")

    def addUnusedToNext(self, path):
        # print("---------\nstarting addUnusedToNext")
        alreadyUsed = []
        for i in range(len(path) - self.K + 1):
            alreadyUsed.append(path[i:i+self.K])

        # print("alreadyUsed values", alreadyUsed)
        # print("values before adding", self.values)
        unusedValues = [x for x in self.values[self.position] if x not in alreadyUsed]
        # print("unused values", unusedValues)
        self.values[self.position + 1] = self.values[self.position + 1] + unusedValues
        # print("values after adding", self.values)
        # print("---------\n")


def runOnce(N, K, sqne, pose):
    algorithm = ExactAlgorithm(N, K, sqne, pose)
    # get cost matrix
    # algorithm.setUpForPosition(0)
    # algorithm.dfs(0, algorithm.visited, 0, algorithm.values[0][0])

    # first start point is the first in values
    startPoint = 0
    startPath = algorithm.values[0][startPoint]
    for i in range(5):
        if(i==0):
            algorithm.bestPath = startPath
        
        if (i!=0):
            # remove already mers we've used in previous positions
            algorithm.removeAlreadyUsed(algorithm.bestPath)
            # insert the last from previous iteration as the first of this one
            algorithm.values[i].insert(0, algorithm.bestPath[-algorithm.K:])
        

        # print("values in position",i,":", algorithm.values[i], "len:", len(algorithm.values[i]))

        algorithm.setUpForPosition(i)
        algorithm.dfs(startPoint, algorithm.visited, algorithm.cost, algorithm.bestPath, algorithm.bestNumOfUsed)
        # print("=========\nBest path returned for position", algorithm.position,"\n", algorithm.bestFitness, algorithm.bestPath, len(algorithm.bestPath), "\n")

        if (i!=4):
            algorithm.addUnusedToNext(algorithm.bestPath)

    return algorithm.bestPath, algorithm.bestFitness

def plotTime():
    N = 40
    K = 8
    sqne = 0
    pose = 5
    numOfRepeats = 10

    x = []
    y = []

    for N in range(20, 71, 5):
        x.append(N)
        timeBefore = time.time()
        for i in range(numOfRepeats):
            runOnce(N, 8, N//8, N//8)
            print("for N =", N, "run", i, "path:", bestPath, len(bestPath))
        timeAfter = time.time()
        y.append((timeAfter - timeBefore)/numOfRepeats)

    # plt.tight_layout()
    plt.plot(x, y, 'ro-')
    plt.xlabel('Długość ciągu N')
    plt.ylabel('Średnia czasu dla ' + str(numOfRepeats) + ' powtórzeń [s]')
    # plt.yscale('log')

    plt.savefig('pics/czas_20-70_5.png', bbox_inches='tight')
    # plt.show()
    plt.close()


def plotSqneTimeAndFitness():
    N = 50
    K = 8
    pose = 0
    numOfRepeats = 10

    x = []
    y = []
    fitnessY = []

    for sqne in range(0, 10, 1):
        x.append(sqne)
        localFitness = 0
        timeBefore = time.time()
        for i in range(numOfRepeats):
            bestPath, bestFitness = runOnce(N, 8, sqne, pose)
            localFitness = localFitness + bestFitness
            print("for sqne =", sqne, "run", i, "path:", bestPath, len(bestPath), "best fitness", bestFitness)
        timeAfter = time.time()
        y.append((timeAfter - timeBefore)/numOfRepeats)
        fitnessY.append(localFitness/numOfRepeats)

    # plt.tight_layout()
    plt.plot(x, y, 'ro-')
    plt.xlabel('Ilość błędów negatywnych')
    plt.ylabel('Średnia czasu dla ' + str(numOfRepeats) + ' powtórzeń [s]')
    # plt.yscale('log')

    plt.savefig('pics/sqne_time2.png', bbox_inches='tight')
    # plt.show()
    plt.close()

    plt.plot(x,fitnessY, 'bo-')
    plt.xlabel('Ilość błędów negatywnych')
    plt.ylabel('Średnia wartość funkcji celu dla ' + str(numOfRepeats) + ' powtórzeń')
    plt.savefig('pics/sqne_fitness2.png', bbox_inches='tight')


def plotPoseTimeAndFitness(sqne):
    N = 50
    K = 8
    pose = 0
    numOfRepeats = 10

    x = []
    y = []
    fitnessY = []

    for pose in range(0, 10, 2):
        x.append(pose)
        localFitness = 0
        timeBefore = time.time()
        for i in range(numOfRepeats):
            bestPath, bestFitness = runOnce(N, 8, sqne, pose)
            localFitness = localFitness + bestFitness
            print("for pose =", pose, "run", i, "path:", bestPath, len(bestPath), "best fitness", bestFitness)
        timeAfter = time.time()
        y.append((timeAfter - timeBefore)/numOfRepeats)
        fitnessY.append(localFitness/numOfRepeats)

    # plt.tight_layout()
    plt.plot(x, y, 'ro-')
    plt.xlabel('Ilość błędów pozycji')
    plt.ylabel('Średnia czasu dla ' + str(numOfRepeats) + ' powtórzeń [s]')
    # plt.yscale('log')

    plt.savefig('pics/pose_time_sqne'+str(sqne)+'.png', bbox_inches='tight')
    # plt.show()
    plt.close()

    plt.plot(x,fitnessY, 'bo-')
    plt.xlabel('Ilość błędów pozycji')
    plt.ylabel('Średnia wartość funkcji celu dla ' + str(numOfRepeats) + ' powtórzeń')
    plt.savefig('pics/pose_fitness_sqne'+str(sqne)+'.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    # plotSqneTimeAndFitness()
    plotPoseTimeAndFitness(0)
    plotPoseTimeAndFitness(7)


    

# TODO:
# stop if over the len of position
# push everything not chosen to next position
# add value better if more used

# fix numOfUsed