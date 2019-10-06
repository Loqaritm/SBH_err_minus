import numpy as np
import random
from copy import deepcopy
from parser import *

class Unit:
    sequence= [] #array of sequence numbers included in this unit
    name = '' #current unit string name eg. ACGAGT...[tbd]
    fitness = 0
    # def __init__(self, sequence, name):
    #     self.name=''

    def calculateFitness(self, spectrum):
        self.fitness = 0
        #return self.fitness


    def fixoffspring(self, spectrum):#offspring sequence fixing
        for i in range(len(self.sequence)):
            for j in range(i+1, len(self.sequence)): #only following
                if self.sequence[i] == self.sequence[j]:
                    self.sequence[j]= self.findBestSub(i, spectrum)


    def findBestSub(self, pos, spectrum): #problematic position =pos
        second = set(self.sequence)
        possibleSubs = [item for item in spectrum.sequence not in second]
        for sub in possibleSubs:
            pass #calculate adjecent


class SpectrumSEQ: #TODO
    sequence = [] #just 12345678
    strings = [] #according to sequence AGTA GTAC etc

    # def __init__(self, arr):
    #     self.sequence.append(0) #firstOne
    #     for i in range(1,len(arr)):
    #         if getCost()



    def getChunks(self, array):
        localArray = deepcopy(array)
        costs = getMatrixOfCosts(localArray)

        for row in range(len(localArray)):
            numOfNexts = 0
            potentialNextPosition = 0
            for col in range(len(localArray)):
                if (costs[row,col] == 1):
                    numOfNexts = numOfNexts + 1
                    # save the last (and hopefuly only) next one
                    potentialNextPosition = col
            
            if (numOfNexts == 1):
                # update in both places
                newValue = localArray[row] + localArray[potentialNextPosition][-1:]
                localArray[:] = [newValue if (x == localArray[row] or x == localArray[potentialNextPosition]) else x for x in localArray]
            
        return list(dict.fromkeys(localArray))

                




class GeneticGeneration:
    def __init__(self, givenActualSpectr): #create initial sequences
        self.spectrum = SpectrumSEQ(givenActualSpectr) #name might be misleading, this "spectrum" is set of SEQUENCES created from actual spectrum
        self.generation = self.createGeneration(spectrum=self.spectrum)
        self.Actualspectrum = givenActualSpectr

    def createGeneration(self, spectrum): #FIRST PREDEFINED!!!!
        generation = []
        return generation

    def chooseParents(self):
        parentXn = random.randint(0, len(self.generation))
        parentYn = random.randint(0, len(self.generation))
        while parentXn == parentYn:  # differentParents
            parentYn = random.randint(0, len(self.generation))  # parents as numbers
        parentX = self.generation[parentXn]
        parentY = self.generation[parentYn]  # objects
        return parentX, parentY

    def mutateOffspring(self, offspring):
        mutants = []
        seq = self.randomMutationSequence(offspring)
        for i in range(1, offspring.sequence):
            mutant = offspring
            mutant.sequence[i] = seq
            mutants.append(mutant)
        return mutants

    def randomMutationSequence(self, unit): #find random sequence to replace others
        while True:
            seq = random.randint(0, len(self.spectrum.sequence))
            if seq not in unit.sequence:
                return seq

    def offspringReplaceGenerationMember(self, mutants, ParentX, ParentY):
        for mutant in mutants:
            if mutant.fitness > ParentX.fitness:
                self.findAndReplaceWeakestMember(mutant)
                return True
            elif mutant.fitness > ParentY.fitness:
                self.findAndReplaceWeakestMember(mutant)
                return True
        return False

    def findAndReplaceWeakestMember(self, mutant):
        weakestMember = self.generation[0]
        for member in self.generation:
            if member.fitness<weakestMember.fitness:
                weakestMember=member
        self.generation.remove(weakestMember)
        self.generation.append(mutant)

    def selectBestCrossedOffspring(self, offspringTab):
        bestoffspring = offspringTab[0]
        bestoffspring.calculateFitness()
        for i in range(len(offspringTab)):
            if offspringTab[i].calculateFitness() > bestoffspring.fitness:
                bestoffspring = offspringTab[i]
        return bestoffspring

    def crossover(self):
        parentX, parentY = self.chooseParents()
        partition = random.randint(3, 5) #na ile będzie sie dzielic
        chunkX = len(parentX.sequence)/partition
        chunkY = len(parentY.sequence)/partition
        crossoverOffspringList = []
        offspring = Unit()
        for i in range(5):
            for j in range(0, partition-1):
                if random.randint(0, 1) < 1:
                    offspring.sequence.extend(parentX.sequence[j*chunkX:(j+1)*chunkX])
                else:
                    offspring.sequence.extend(parentY.sequence[j * chunkY:(j + 1) * chunkY])
            if random.randint(0, 1) < 1:
                offspring.sequence.extend(parentX.sequence[len(parentX.sequence)-(partition-1*chunkX)])
            else:
                offspring.sequence.extend(parentY.sequence[len(parentY.sequence)-(partition-1*chunkY)])
            offspring.fixoffspring(self.spectrum)
            crossoverOffspringList.append(offspring)
        offspring = self.selectBestCrossedOffspring(crossoverOffspringList)
        mutatedOffspring = self.mutateOffspring(offspring)
        mutatedOffspring.append(offspring)
        for mutant in mutatedOffspring:
            mutant.calculateFitness(self.spectrum)
        return self.offspringReplaceGenerationMember(mutatedOffspring, parentX, parentY) #return true if the generation changed


if __name__ == '__main__':
    testArray = ["EEEE","CGAA", "GAAC", "AACT", "TTTA", "TTAC", "TTAG", "AAAA", "BCDE", "ABCD"]
    
    spec = SpectrumSEQ()
    result = spec.getChunks(testArray)

    print("Na wejsciu:", testArray, "\nNa chunki:", result)