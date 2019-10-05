from parser import *
from copy import deepcopy

class ExactAlgorithm:
    MAXVAL = 10000

    def __init__(self, N, K, sqne, pose):
        self.values = getValuesFromUrl(N, K, sqne, pose)
        self.path = ""

    # gets cost matrix and visited matrix for specified position
    def setUpForPosition(self, position):
        self.costMatrix = getMatrixOfCosts(self.values[position])
        self.visited = np.zeros(self.costMatrix.shape[0])
        self.minCost = MAXVAL
        self.minPath = ""
        self.position = position
        
        self.listOfPoints = []

    def findBestRoute(self):
        nothing = 0
        
    def dfs(self, startPoint, visitedPoints, costNow, pathNow, depth):
        cost = deepcopy(costNow)
        path = deepcopy(pathNow)
        visited = deepcopy(visitedPoints)
        visited[startPoint] = 1
        allVisitedFlag = True
        if (cost > self.minCost):
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
                self.dfs(nextPoint, visited, localCost, localPath, depth + 1)

        if (allVisitedFlag and cost < self.minCost):
            self.minCost = deepcopy(cost)
            self.minPath = deepcopy(path)
            print("New best path found! with cost:", self.minCost, "and path:", self.minPath)

if __name__ == '__main__':
    algorithm = ExactAlgorithm(100, 10, 20, 20)
    # algorithm = ExactAlgorithm(50, 5, 5, 0)
    print("values in first position:", algorithm.values[0], "len:", len(algorithm.values[0]))

    #get cost matrix
    algorithm.setUpForPosition(0)

    startPoint = 0
    # algorithm.values[algorithm.position][startPoint]
    algorithm.dfs(startPoint, algorithm.visited, 0, algorithm.values[algorithm.position][startPoint], 0)
    print("=========\nBest path returned\n", algorithm.minCost, algorithm.minPath, len(algorithm.minPath))

