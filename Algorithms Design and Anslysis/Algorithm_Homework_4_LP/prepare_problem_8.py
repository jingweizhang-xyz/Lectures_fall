'''
Created on 2015-11-24

@author: wty
'''

import random
import string
from pprint import pprint

def writeToFile(path, content):
    with open(path, "w") as fw:
        fw.write(str(content))

dict = list(string.ascii_letters)
set = {}
def getRandomStr():
    while True:
        random.shuffle(dict)
        randStr = ''.join(dict[:10])
        if randStr not in set:
            set[randStr] = True
            break
    return randStr

if __name__ == '__main__':
    n = 100
    minValue = 1
    maxValue = 1000

    glpkInput = ""
    pythonInput = ""
    
    for i in range(1, n+1):
        glpkInput += "var x%d;\n" % i
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            dij = random.randint(minValue, maxValue)
            pythonInput += "%d\t%d\t%d\n" % (i, j, dij)
            glpkInput += "var d%d_%d = %d;\n" % (i, j, dij)
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            glpkInput += "var ve%d_%d >= 0;\n" % (i, j)
    glpkInput += "minimize answer: "
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            glpkInput += "ve%d_%d" % (i, j)
            glpkInput += " + " if i != n-1 or j != n else ""
    glpkInput += ";\n"
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            name = getRandomStr()
            glpkInput += "s.t. {2} : x{0} - x{1} - d{0}_{1} <= ve{0}_{1};\n".format(i, j, name)
            name = getRandomStr()
            glpkInput += "s.t. {2} : x{0} - x{1} - d{0}_{1} >= -ve{0}_{1};\n".format(i, j, name)
    
    writeToFile("8_CInput.in", pythonInput)
    writeToFile("8_glpkInput.mod", glpkInput)