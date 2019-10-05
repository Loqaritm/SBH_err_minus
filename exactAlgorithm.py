from parser import *

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

    def findBestRoute(self):
        nothing = 0
        print(self.visited)
        
    def dfs(self, startPoint, visitedPoints, costNow, pathNow, depth):
        cost = costNow
        path = pathNow
        visitedPoints[startPoint] = 1
        allVisitedFlag = True
        print(self.costMatrix[startPoint])
        for nextPoint, nextPointCost in enumerate(self.costMatrix[startPoint]):
            print("dupa", nextPoint, nextPointCost)
            print("my depth:", depth)


            # we haven't visited it yet
            if(visitedPoints[nextPoint] == 0):
                allVisitedFlag = False
                cost = cost + nextPointCost
                path = path + self.values[self.position][nextPoint]
                self.dfs(nextPoint, visitedPoints, cost, path, depth + 1)

            # # ignore as there is no point in checking more if its worse than minimum we already got
            # if (cost > self.minCost):
            #     continue
        
        if (allVisitedFlag and cost < self.minCost):
            self.minCost = cost
            self.minPath = path
            print(self.minCost)

        return

if __name__ == '__main__':
    algorithm = ExactAlgorithm(100, 10, 20, 20)
    print(algorithm.values[0])

    #get cost matrix
    algorithm.setUpForPosition(0)
    print(algorithm.costMatrix)

    algorithm.findBestRoute()

    algorithm.dfs(0, algorithm.visited, 0, "", 0)
    print(algorithm.minCost, algorithm.minPath)

