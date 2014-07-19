'''
Created on Jul 15, 2014

@author: ppx10
'''
from src.alignObject import alignObject

class NeedlemanWunsch(alignObject):
    
    def initScoreMarix(self):
        self.scoreMatrix = [[self.gapOpenPenalty]]
        
        rowGapCnt=0
        rowLen = len(self.rowString)
        rowPenalty = self.gapPenalty(0)
        
        while(rowLen > 0):
            self.scoreMatrix .append([rowPenalty])   
            rowGapCnt+=1
            rowPenalty += self.gapPenalty(0)
            rowLen -= 1
            
        colGapCnt = 0
        colLen = len(self.colString)
        colPenalty = self.gapPenalty(0)
        
        while(colLen > 0):
            self.scoreMatrix [0].append(colPenalty)
            colGapCnt+=1
            colPenalty += self.gapPenalty(0)
            colLen -= 1    
        
    
    def initTracebackMatrix(self):
        self.tracebackMatrix = [[self.done]]
        rowLen = len(self.rowString)
        while(rowLen > 0):
            self.tracebackMatrix.append([self.up])
            rowLen -= 1
            
            colLen = len(self.colString)
        while(colLen > 0):
            self.tracebackMatrix[0].append(self.left)
            colLen -= 1    
    
               
    def score(self, row, col):
        diagScore = self.diagScore(
                              row,
                              col,
                              self.rowString[row - 1],
                              self.colString[col - 1]
                              )
        upScore = self.upScore(row, col)
        leftScore = self.leftScore(row, col)
        
        options = [leftScore,upScore , diagScore]
        self.printMatrix(self.scoreMatrix)
        print()
        (value, choice) = self.maxChoice(options)
        
        if(choice == 2):
            option = self.diag
        elif(choice ==1):
            option = self.up
        elif(choice==0):
            option = self.left
        else:
            assert "Invalid option"
        return (value, option)
        
        
    def startPosition(self):
        '''
        get starting position for traceback
        '''
        return len(self.rowString), len(self.colString)
   
                

    
 
similarityMatrix = {
                  "a":{"a":10, "c":0, "g":0, "t":0},
                  "c":{"a":0, "c":10, "g":0, "t":0},
                  "g":{"a":0, "c":0, "g":10, "t":0},
                  "t":{"a":0, "c":0, "g":0, "t":10}
                  }
                   
test = NeedlemanWunsch(similarityMatrix,-10, -1)
    

test.align("gaaaagagaaagaaa", "gagaaa")
