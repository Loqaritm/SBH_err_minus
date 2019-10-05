import urllib.request
import xml.etree.ElementTree as ET
import numpy as np

defN = 100
defK = 10
defsqne = 20
defpose = 20
MAXVAL = 100000
positions = 5

# url = "http://www.piotr.e.wawrzyniak.doctorate.put.poznan.pl/bio.php?n=" + str(N) +"&k="+ str(K) +"&mode=basic&intensity=0&position=1&sqpe=0&sqne=" + str(sqne) + "&pose=" + str(pose)

def getValuesFromUrl(N, K, sqne, pose, shouldPrint = False):
    url = "http://www.piotr.e.wawrzyniak.doctorate.put.poznan.pl/bio.php?n=" + str(N) +"&k="+ str(K) +"&mode=basic&intensity=0&position=1&sqpe=0&sqne=" + str(sqne) + "&pose=" + str(pose)

    contents = urllib.request.urlopen(url)

    root = ET.parse(contents).getroot()
    
    if (shouldPrint):
        # just a check if works 
        print(root.tag, root.attrib)

    probe = root.find('probe')

    valuesAndPosition = [[],[],[],[],[]]

    for cell in probe:
        if (shouldPrint):
            print(cell.tag, cell.attrib['position'], cell.text)
        position = int(cell.attrib['position'])
        valuesAndPosition[position].append(cell.text) 
    
    return valuesAndPosition

def getCost(first, second):
    # they need to be the same len
    if (len(first) != len(second)):
        print("WRONG LEN - RETURNING LEN OF FIRST")

    # iterate from 0 to K, -1 because the first string is checked from 1 to K so we will be adding +1
    # this is the starting point of check
    for i in range(1, len(first)):
        firstSubstring = first[i:]
        secondSubstring = second[:len(second)-i]
        # check if substrings are the same 
        if (firstSubstring == secondSubstring):
            # ok this means we can return the number of different letters at the end which is = i
            return i
    
    return len(first)

def getMatrixOfCosts(valuesForOnePosition):
    matrix = np.full((len(valuesForOnePosition), len(valuesForOnePosition)), MAXVAL)
    rows, cols = matrix.shape

    for x in range(0, rows):
        for y in range(0, cols):
            if (x!=y):
                matrix[x,y] = getCost(valuesForOnePosition[x], valuesForOnePosition[y])
            else:
                matrix[x,y] = MAXVAL
    
    return matrix

# dont use this - this will get new data each time
def getMatrices(N = defN, K = defK, sqne = defsqne, pose = defpose):
    valuesAndPosition = getValuesFromUrl(N, K, sqne, pose)
    matrices = np.asarray(valuesAndPosition).reshape(positions)

    for i, matrix in enumerate(matrices):
        matrices[i] = createMatrixOfCosts(matrix)

    # return all matrices of costs
    return matrices
        

if __name__ == '__main__':
    # valuesAndPosition = getValuesFromUrl()
    print(getCost("ACGTA", "ACGTA"))
    # print(getCost("ACGTA", "CGTAA"))
    # print(getCost("CGTAA", "ACGTA"))
    createMatrixOfCosts(["ACGTA","CGTAA","GTACC", "TACCC", "ATCGT", "CCCCC"])
    getMatrices()