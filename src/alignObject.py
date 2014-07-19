'''
Created on Jul 18, 2014

@author: ppx10
'''
import abc
class alignObject(object):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta
    
    
    done = "done"
    up = "up"
    left = "left"
    diag = "diag"
    
    
    similarityMatrix = [[]]
    scoreMatrix = [[0]]
    tracebackMatrix = [[done]]
    
    gapSymbol = "-"
    
    gapOpenPenalty = -10
    gapAffinePenalty = -3
    
    rowGapCount = 0
    colGapCount = 0
    
    rowString = ""
    colString = ""
    
    def __init__(self, similarityMatrix, gapOpenPenalty=-10, gapAffinePenalty=-3):
        self.similarityMatrix = similarityMatrix
        self.gapOpenPenalty = gapOpenPenalty
        self.gapAffinePenalty = gapAffinePenalty
        
        
    @abc.abstractmethod
    def initScoreMarix(self):
        '''
        
        '''
        
    @abc.abstractmethod    
    def initTracebackMatrix(self):
        '''
        
        '''
        
    def gapPenalty(self, count):
        return self.gapOpenPenalty - self.gapAffinePenalty * count
    
    
    def diagScore(self, row, col, rowChar, colChar):
        self.colGapCount = 0
        self.rowGapCount = 0
        return self.scoreMatrix[row - 1][col - 1] + self.similarityMatrix[rowChar][colChar]
    
    def upScore(self, row, col):
        self.colGapCount += 1
        self.rowGapCount = 0
        return self.scoreMatrix[row - 1][col] + self.gapPenalty(self.colGapCount)
    
    def leftScore(self, row, col):
        self.colGapCount = 0
        self.rowGapCount += 1
        return self.scoreMatrix[row][col - 1] + self.gapPenalty(self.rowGapCount)
    
    
    def maxChoice(self, options):  
        maxValue = options[0]
        maxIndex = 0
        
        for i in range(1, len(options)):
            if(options[i] > maxValue):
                maxValue = options[i]
                maxIndex = i
            
        return (maxValue, maxIndex)
                
    @abc.abstractmethod               
    def score(self, row, col):
        '''
        
        '''
        
    def createScoreAndTracebackMatrix(self):
        
        self.initScoreMarix()
        self.initTracebackMatrix()
        
        for row in range(1, len(self.scoreMatrix)):
            for col in range(1, len(self.scoreMatrix[0])):
                (value, option) = self.score(row, col)
                
                self.scoreMatrix[row].append(value)
                self.tracebackMatrix[row].append(option)
                
        
    @abc.abstractmethod 
    def startPosition(self):
        '''
        get starting position for traceback
        '''
        
    def tracebackPath(self):
        
        path = []
        
        (row, col) = self.startPosition()
        
        option = self.tracebackMatrix[row][col]
        
        while(option != self.done):
            path.append(option)
            if(option == self.diag):
                row -= 1
                col -= 1
            elif option == self.left:
                col -= 1
            elif option == self.up:
                row -= 1
            else:
                raise Exception("WTF")
            
            option = self.tracebackMatrix[row][col]
            
        return path    
                
    def printMatrix(self, matrix):
        for i in range(len(matrix)):
            print("")
            for j in range(len(matrix[0])):
                try:
                    print("%7s"%(matrix[i][j]), end="")
                except:
                    pass
                pass
            
            

    def align(self, seq1, seq2):
        
        (self.rowString, self.colString) = (seq1, seq2) if len(seq1) < len(seq2) else (seq2, seq1)
        
        self.createScoreAndTracebackMatrix()
        
       
       
        tracebackPath = self.tracebackPath()
        
        firstAlignedReversed = []
        secondAlignedReversed = []
        
        (iFirst, iSecond) = self.startPosition()
        iFirst-=1
        iSecond-=1
        
        for option in tracebackPath:
            
            
            if(option == self.diag):
                firstAlignedReversed.append(self.rowString[iFirst])
                iFirst -= 1
                
                secondAlignedReversed.append(self.colString[iSecond])
                iSecond -= 1
                
            elif(option == self.left):
                firstAlignedReversed.append(self.gapSymbol)
                
                secondAlignedReversed.append(self.colString[iSecond])
                iSecond -= 1
                
            elif(option == self.up):
                firstAlignedReversed.append(self.rowString[iFirst])
                iFirst -= 1
                
                secondAlignedReversed.append(self.gapSymbol)
                
        seq1Aligned = "".join(reversed(firstAlignedReversed))
        seq2Aligned = "".join(reversed(secondAlignedReversed))
        
        print(seq1Aligned)
        print(seq2Aligned)
        return seq1Aligned, seq2Aligned
        
