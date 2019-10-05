from parser import *

class ExactAlgorithm:
    def __init__(self, N, K, sqne, pose):
        self.values = getValuesFromUrl(N, K, sqne, pose)


if __name__ == '__main__':
    algorithm = ExactAlgorithm(100, 10, 20, 20)
    print(algorithm.values[0])

