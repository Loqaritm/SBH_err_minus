import numpy as np
import random
from copy import deepcopy
from DNAparser import *

class Unit:
    sequence= [] #array of sequence numbers included in this unit
    name = '' #current unit string name eg. ACGAGT...[tbd]
    fitness = 0
    # def __init__(self, sequence, name):
    #     self.name=''

    def calculateFitness(self, spectrum, n): #this is spectrum created from chunks
        self.fitness = 0
        self.name = spectrum.strings[0]
        for i in range(1,len(self.sequence)):
            self.fitness+= self.addChunkToUnitNameByChunkID(spectrum, i) #dla wszystkich chunków oprócz pierwszego!
        print(self.name)
        difference = len(self.name)-spectrum.DesiredLength

        #return self.fitness

    def addChunkToUnitNameByChunkID(self, spectrum, id): #this function adds chunk eg. ATTAT to GCCATT name creating GCCATTAT name and returns number of fitted
        for i in reversed(range(1,len(spectrum.strings[id]))):   #reversed order                                   #nucleotyds - in this example ATT=3
            if self.name[-i:]==spectrum.strings[id][:i]:
                self.name = self.name + spectrum.strings[id][i:]
                return i
        self.name = self.name +spectrum.strings[id]
        return 0

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
    DesiredLength = 50
    def __init__(self, arr):
        # length = 6
        #firstOne
        # count =0
        # elemId =0
        # for i in range(1,len(arr)):
        #     if getCost(arr[0], arr[i]) == 1:
        #         elemId = i
        #         count+=1    #check for unique connections
        # if count==1:
        #     self.strings.append(arr[0] + arr[elemId][-1:])
        #     arr.remove(arr[elemId])
        #     arr.remove(arr[0])
        # else:
        #     self.strings.append(arr[0])
        #     arr.remove(arr[0])
        self.strings=self.getChunks(arr)
        for i in range(len(self.strings)):
            self.sequence.append(i)
            print(i, "    ")
            print(self.strings[i])

    def getChunks(self, array):
        localArray = deepcopy(array)
        costs = getMatrixOfCosts(localArray)

        for row in range(len(localArray)):
            numOfNexts = 0
            potentialNextPosition = 0
            for col in range(len(localArray)):
                if (costs[row, col] == 1):
                    numOfNexts = numOfNexts + 1
                    # save the last (and hopefuly only) next one
                    potentialNextPosition = col

            if (numOfNexts == 1):
                # update in both places
                newValue = localArray[row] + localArray[potentialNextPosition][-1:]
                localArray[:] = [
                    newValue if (x == localArray[row] or x == localArray[potentialNextPosition]) else x for x in
                    localArray]

        return list(dict.fromkeys(localArray))


class GeneticGeneration:
    generationSize = 10
    chainLength = 50
    def __init__(self, givenActualSpectr, length): #create initial sequences
        self.spectrum = SpectrumSEQ(givenActualSpectr, length) #name might be misleading, this "spectrum" is set of SEQUENCES created from actual spectrum
        self.generation = self.createGeneration(spectrum=self.spectrum)
        self.Actualspectrum = givenActualSpectr

    def createGeneration(self, spectrum): #FIRST PREDEFINED!!!!
        generation = []
        chunks = spectrum
        rand=0
        for i in range(self.generationSize):
            chunks=spectrum
            child=Unit()
            child.sequence.append(chunks.sequence[0]) ##first predefined #{
            #child.name += chunks.strings[0]
            del chunks.sequence[0]
            del chunks.strings[0]   #}
            while len(chunks.sequence) > 0:
                rand=random.randint(0,len(chunks.sequence))
                child.sequence.append(chunks.sequence[rand])
                #child.name += chunks.strings[rand]
                del chunks.sequence[rand]
                del chunks.strings[rand]
            generation.append(child)
            child.calculateFitness(spectrum, self.chainLength)
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
        bestmutant = mutants[0]
        for mutant in mutants:
            if mutant.fitness > bestmutant.fitness:
                bestmutant=mutant

        if bestmutant.fitness > ParentX.fitness:
            self.findAndReplaceWeakestMember(bestmutant)
            return True
        elif bestmutant.fitness > ParentY.fitness:
            self.findAndReplaceWeakestMember(bestmutant)
            return True
        return False

    def findAndReplaceWeakestMember(self, mutant):
        weakestMember = self.generation[0]
        for member in self.generation:
            if member.fitness<weakestMember.fitness:
                weakestMember = member
        self.generation.remove(weakestMember)
        self.generation.append(mutant)

    def selectBestCrossedOffspring(self, offspringTab): #selects best offspring based on fitness
        bestoffspring = offspringTab[0]
        bestoffspring.calculateFitness(spectrum=self.spectrum, n=self.chainLength)
        for i in range(len(offspringTab)):
            offspringTab[i].calculateFitness(spectrum=self.spectrum, n=self.chainLength)
            if offspringTab[i].fitness > bestoffspring.fitness:
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
                offspring.sequence.extend(parentX.sequence[-(len(parentX.sequence)-(partition-1*chunkX)):]) #add remaining part, wchich is lenght (eg 9) - partition-1 times chunk (eg. 2x3),
            else:
                offspring.sequence.extend(parentY.sequence[partition-1*chunkY:])
            offspring.fixoffspring(self.spectrum)
            crossoverOffspringList.append(offspring)
        offspring = self.selectBestCrossedOffspring(crossoverOffspringList)
        mutatedOffspring = self.mutateOffspring(offspring) #mutating only best fitting offspring
        mutatedOffspring.append(offspring)
        for mutant in mutatedOffspring:
            mutant.calculateFitness(spectrum=self.spectrum, n=self.chainLength)
        return self.offspringReplaceGenerationMember(mutatedOffspring, parentX, parentY) #return true if the generation changed


if __name__ == '__main__':
    testArray = ["CGAA", "GAAC", "AACT", "TTTA", "TTAC", "TTAG", "AAAA", "BCDE", "ABCD"]

    spec = SpectrumSEQ(arr=testArray)


    print("Na wejsciu:", testArray, "\nNa chunki:", result)