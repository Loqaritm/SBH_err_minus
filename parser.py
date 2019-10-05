import urllib.request
import xml.etree.ElementTree as ET
import numpy as np

N = 100
K = 10
sqne = 20
pose = 20

url = "http://www.piotr.e.wawrzyniak.doctorate.put.poznan.pl/bio.php?n=" + str(N) +"&k="+ str(K) +"&mode=basic&intensity=0&position=1&sqpe=0&sqne=" + str(sqne) + "&pose=" + str(pose)

def getValuesFromUrl():
    contents = urllib.request.urlopen(url)

    root = ET.parse(contents).getroot()
    
    # just a check if works 
    print(root.tag, root.attrib)

    probe = root.find('probe')

    valuesAndPosition = [[],[],[],[],[]]

    for cell in probe:
        print(cell.tag, cell.attrib['position'], cell.text)
        position = int(cell.attrib['position'])
        valuesAndPosition[position].append(cell.text) 
    
    print(valuesAndPosition)

    return valuesAndPosition

def getCost(first, second):
    # they need to be the same len
    if (len(first) != len(second)):
        print("WRONG LEN - RETURNING LEN OF FIRST")

    # iterate from 0 to K, -1 because the first string is checked from 1 to K so we will be adding +1
    # this is the starting point of check
    for i in range(len(first) - 1):
        firstSubstring = first[i:]
        secondSubstring = second[:len(second)-i]
        # check if substrings are the same 
        if (firstSubstring == secondSubstring):
            # ok this means we can return the number of different letters at the end which is = i
            return i
    
    return len(first)

def createMatrixOfCosts(valuesAndPosition):
    nothing = 1

if __name__ == '__main__':
    # valuesAndPosition = getValuesFromUrl()
    print(getCost("ACGTA", "CATAT"))