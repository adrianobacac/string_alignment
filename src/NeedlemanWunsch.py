'''
Created on Jul 15, 2014

@author: ppx10
'''
class NeedlemanWunsch(object):
    '''
    classdocs
    '''
    
    done = "done"
    up = "up"
    left = "left"
    diag = "diag"
    
    similarityMatrix = [[]]
    scoreMatrix = [[0]]
    tracebackMatrix = [[done]]
    
    gapSymbol = "-"
    gapPenalty = 10
    charPenalty = 10
    
    
    def __init__(self, similarityMatrix, gapPenalty=10, charPenalty=10, gapSymbol="-"):
        self.similarityMatrix = similarityMatrix
        self.gapPenalty = gapPenalty
        self.gapSymbol = gapSymbol
        self.charPenalty = charPenalty
        
    
    def initScoreMarix(self, rowLen, colLen):
        
        rowPenalty = -self.charPenalty
        while(rowLen > 0):
            self.scoreMatrix .append([rowPenalty])
            rowPenalty -= self.charPenalty
            rowLen -= 1
            
        colPenalty = -self.charPenalty
        while(colLen > 0):
            self.scoreMatrix [0].append(colPenalty)
            colPenalty -= self.charPenalty
            colLen -= 1    
            
            
    def initTracebackMatrix(self, rowLen, colLen):
        
        while(rowLen > 0):
            self.tracebackMatrix.append([self.up])
            rowLen -= 1
            
        while(colLen > 0):
            self.tracebackMatrix[0].append(self.left)
            colLen -= 1    
            
            
            
            
    def maxChoice(self, diag, up, left):  
        
            maxValue = max([diag, up, left])
            
            maxPos = self.diag
            if(maxValue == up):
                maxPos = self.up
            elif (maxValue == left):
                maxPos = self.left
                 
            return [maxValue, maxPos]
            
            
    def score(self, row, col, rowString, colString):
     
        diag = self.scoreMatrix[row - 1][col - 1] + self.similarityMatrix[rowString[row-1]][colString[col-1]]
        up = self.scoreMatrix[row - 1][col] - self.gapPenalty
        left = self.scoreMatrix[row][col - 1] - self.gapPenalty
        
        return self.maxChoice(diag, up, left)
            
            
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
        rowNum = len(self.tracebackMatrix)-1
        colNum = len(self.tracebackMatrix[0])-1
        
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
        
        iFirst = len(firstString)-1
        iSecond = len(secondString)-1
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
                   
test = NeedlemanWunsch(similarityMatrix,6,6)
    

test.align("ttcata", "tgctcgta")
