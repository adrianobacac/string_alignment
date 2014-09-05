'''
Created on Jul 15, 2014

@author: ppx10
'''
from src.alignObject import alignObject

class NeedlemanWunsch(alignObject):
    
    def initScoreMarix(self):
        self.scoreMatrix = [[0]]
        
        
        rowLen = len(self.rowString)
        rowPenalty = self.gapPenalty(0)
        
        currentRow = 0
        while(currentRow <rowLen):
            self.scoreMatrix .append([rowPenalty])   
            
            currentRow+=1
            rowPenalty += self.gapPenalty(1)
            
            
        
        colLen = len(self.colString)
        colPenalty = self.gapPenalty(0)
        
        currentCol = 0
        while(currentCol<colLen):
            self.scoreMatrix [0].append(colPenalty)
            
            currentCol+=1
            colPenalty += self.gapPenalty(1)
            
        
    
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
        
        options = [leftScore, upScore , diagScore]
        
        (value, choice) = self.maxChoice(options)
        
        if(choice == 0):
            option = self.left
        elif(choice == 1):
            option = self.up
        elif(choice == 2):
            option = self.diag
        else:
            assert "Invalid option"
        return (value, option)
        
        
    def startPosition(self):
        '''
        get starting position for traceback
        '''
        return len(self.rowString), len(self.colString)
   
                

