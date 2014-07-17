'''
Created on Jul 17, 2014

@author: ppx10
'''

class matrixValue(object):
    value=None
    row=0
    col=0

    def isGreater(self, num):
        if(num>self.value):
            return True
        else:
            return False

    def setValue(self, value, row, col):
        self.value=value
        self.row=row
        self.col=col

class SmithWaterman(object):
    
    done = "done"
    up = "up"
    left = "left"
    diag = "diag"
    
    maxValue=matrixValue()
    
    similarityMatrix = [[]]
    scoreMatrix = [[0]]
    tracebackMatrix = [[done]]
    
    gapSymbol = "-"
    gapPenalty = 10
    
    
    def __init__(self, similarityMatrix, gapPenalty=10, gapSymbol="-"):
        self.similarityMatrix = similarityMatrix
        self.gapPenalty = gapPenalty
        self.gapSymbol = gapSymbol
        self.maxValue.setValue(0, 0, 0)
    
    def initScoreMarix(self, rowLen, colLen):
        
        while(rowLen > 0):
            self.scoreMatrix .append([0])
            rowLen -= 1
            
        while(colLen > 0):
            self.scoreMatrix [0].append(0)
            colLen -= 1    
            
            
    def initTracebackMatrix(self, rowLen, colLen):
        
        while(rowLen > 0):
            self.tracebackMatrix.append([self.done])
            rowLen -= 1
            
        while(colLen > 0):
            self.tracebackMatrix[0].append(self.done)
            colLen -= 1    
            
            
            
            
    def maxChoice(self, diag, up, left):  
        
            maxValue = max([diag, up, left,0])
            
            maxPos = self.diag
            if(maxValue == up):
                maxPos = self.up
            elif (maxValue == left):
                maxPos = self.left
            elif(maxValue==0):
                maxPos=self.done
                
            return [maxValue, maxPos]
            
            
    def score(self, row, col, rowString, colString):
     
        diag = self.scoreMatrix[row - 1][col - 1] + self.similarityMatrix[rowString[row-1]][colString[col-1]]
        up = self.scoreMatrix[row - 1][col] - self.gapPenalty
        left = self.scoreMatrix[row][col - 1] - self.gapPenalty
        
        choice=self.maxChoice(diag, up, left)
        
        if(self.maxValue.isGreater(choice[0])):
            self.maxValue.setValue(choice[0], row, col)
            
        return choice 
            
    def printMatrix(self, matrix):
        for i in range(0,len(matrix)):
            print(matrix[i])
    
    
    def fillScoreAndTracebackMatrix(self, rowString, colString):
        
        for row in range(1, len(self.scoreMatrix)):
            for col in range(1, len(self.scoreMatrix[0])):
                score = self.score(row, col, rowString, colString)
                maxValue = score[0]
                maxPos = score[1]
                self.scoreMatrix[row].append( maxValue)
                self.tracebackMatrix[row].append(maxPos)
                
        self.printMatrix(self.tracebackMatrix)
                
                
    
    
    def traceback(self, firstString, secondString):
        rowNum = self.maxValue.row
        colNum = self.maxValue.col
        
        path = []
        position = self.tracebackMatrix[rowNum][colNum]
        while(position != self.done):
        
            
            path.append(position)
            if(position == self.diag):
                rowNum -= 1
                colNum -= 1
            elif position == self.left:
                colNum -= 1
            elif position == self.up:
                rowNum -= 1
            else:
                raise Exception("WTF")
            
            position = self.tracebackMatrix[rowNum][colNum]
            
        firstAligned = []
        secondAligned = []
        
        iFirst = self.maxValue.row-1
        iSecond = self.maxValue.col-1
        print("ALIGNMENT", path)
        print(firstAligned, secondAligned)
        for option in path:
            print(option)
            
            if(option == self.diag):
                firstAligned.append(firstString[iFirst])
                iFirst -= 1
                
                secondAligned.append(secondString[iSecond])
                iSecond -= 1
                
            elif(option == self.left):
                firstAligned.append(self.gapSymbol)
                
                secondAligned.append(secondString[iSecond])
                iSecond -= 1
                
            elif(option == self.up):
                firstAligned.append(firstString[iFirst])
                iFirst -= 1
                
                secondAligned.append(self.gapSymbol)
        
            print(firstAligned, secondAligned)
        print("\nRESULT:\n","".join(reversed(firstAligned)),"\n", "".join(reversed(secondAligned)))
        
        return ["".join(reversed(firstAligned)), "".join(reversed(secondAligned))]
                
                
    def align(self, firstString, secondString):
        
        self.initScoreMarix(len(firstString), len(secondString))
        self.initTracebackMatrix(len(firstString), len(secondString))
        
        self.fillScoreAndTracebackMatrix(firstString, secondString)
        
        return self.traceback(firstString, secondString)
    
    
 
similarityMatrix = {
                  "a":{"a":5, "c":-2, "g":-2, "t":-2},
                  "c":{"a":-2, "c":1, "g":-2, "t":-2},
                  "g":{"a":-2, "c":-2, "g":5, "t":-2},
                  "t":{"a":-2, "c":-2, "g":-2, "t":5}
                  }

test = SmithWaterman(similarityMatrix, 6)

test.align("aaagctcgtcgtaaaaaaacgtcgctgcaaaaaa", "gtcgtcggtcgcta")
