'''
Created on Jul 17, 2014

@author: ppx10
'''
from src.alignObject import alignObject


class SmithWaterman(alignObject):
    
    done = "done"
    up = "up"
    left = "left"
    diag = "diag"
    
    maxValue = 0
    maxValueRow = 0
    maxValueCol = 0
   
    
    def initScoreMarix(self):
        self.scoreMatrix = [[0]]
        
        rowLen = len(self.rowString)
        while(rowLen > 0):
            self.scoreMatrix .append([0])
            rowLen -= 1
        
        colLen = len(self.colString)
        while(colLen > 0):
            self.scoreMatrix [0].append(0)
            colLen -= 1    
            
            
    def initTracebackMatrix(self):
        self.tracebackMatrix = [[self.done]]
        
        rowLen = len(self.rowString)
        while(rowLen > 0):
            self.tracebackMatrix.append([self.done])
            rowLen -= 1
            
        colLen = len(self.colString)
        while(colLen > 0):
            self.tracebackMatrix[0].append(self.done)
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
        
        options = [leftScore, upScore , diagScore, 0]
        
        (value, choice) = self.maxChoice(options)
        
        if(value>self.maxValue):
            self.maxValue=value
            self.maxValueRow=row
            self.maxValueCol=col
            
        if(choice == 0):
            option = self.left
        elif(choice == 1):
            option = self.up
        elif(choice == 2):
            option = self.diag
        elif(choice == 3):
            option = self.done
        else:
            assert "Invalid option"
        return (value, option)
    
    def startPosition(self):
        '''
         get starting position for traceback
        '''
        return self.maxValueRow, self.maxValueCol
    
    
 
similarityMatrix = {
                  "a":{"a":10, "c":0, "g":0, "t":0},
                  "c":{"a":0, "c":10, "g":0, "t":0},
                  "g":{"a":0, "c":0, "g":10, "t":0},
                  "t":{"a":0, "c":0, "g":0, "t":10}
                  }

test = SmithWaterman(similarityMatrix, -10, -1)

test.align("aaagtgtgtcaac", "aac")
