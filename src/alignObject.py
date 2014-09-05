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
    
    gapOpenPenalty = -7
    gapAffinePenalty = -1
    
    rowGapCount = 0
    colGapCount = 0
    
    rowString = ""
    colString = ""
    
    def __init__(self, similarityMatrix, gapOpenPenalty=-10, gapAffinePenalty=-3):
        self.similarityMatrix = similarityMatrix
        self.gapOpenPenalty = gapOpenPenalty
        self.gapAffinePenalty = gapAffinePenalty
        
        
    @abc.abstractmethod
    def initScoreMarix(self, rowString, colString):
        '''
        
        '''
        
    @abc.abstractmethod    
    def initTracebackMatrix(self):
        '''
        
        '''
        
    def gapPenalty(self, count):
        
        if(count > 0):
            return self.gapAffinePenalty
        else:
            return self.gapOpenPenalty
        
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
        
        return max(options), options.index(max(options))
        maxValue = options[0]
        maxIndex = 0
        
        for i in range(1, len(options)):
            
            if(options[i] > maxValue):
                maxValue = options[i]
                maxIndex = i
            elif(options[i]==maxValue):
                pass
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
                assert "Invalid option"
            
            option = self.tracebackMatrix[row][col]
            
        return path    
                
    def printMatrix(self):
        print("\t\t\t", end="")
        for i in range(len(self.tracebackMatrix[0])-1):
            print("%8s"%self.colString[i], end="\t")
        print()
        for i in range(len(self.tracebackMatrix)):
            print()
            if(i==0):
                print("\t", end="")
            else:
                print(self.rowString[i-1], end="\t")
            for j in range(len(self.tracebackMatrix[0])):
                try:
                    print("[%4s, %4s]\t"%(self.scoreMatrix[i][j], self.tracebackMatrix[i][j]), end="")
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
        #iFirst-=1
        #iSecond-=1
        
        matchTypeReversed=[]
        
        score = 0 
        for option in tracebackPath:
            
            
            if(option == self.diag):
                
                if(self.rowString[iFirst-1]==self.colString[iSecond-1]):
                    matchTypeReversed.append("|")
                else:
                    matchTypeReversed.append(":")
                
                score +=self.scoreMatrix[iFirst][iSecond]
                firstAlignedReversed.append(self.rowString[iFirst-1])
                iFirst -= 1
                
                secondAlignedReversed.append(self.colString[iSecond-1])
                iSecond -= 1
                
                
            elif(option == self.left):
                
                matchTypeReversed.append(" ")
                
                score +=self.scoreMatrix[iFirst][iSecond]
                firstAlignedReversed.append(self.gapSymbol)
                
                secondAlignedReversed.append(self.colString[iSecond-1])
                iSecond -= 1
                
            elif(option == self.up):
                
                matchTypeReversed.append(" ")
                
                score +=self.scoreMatrix[iFirst][iSecond]
                firstAlignedReversed.append(self.rowString[iFirst-1])
                iFirst -= 1
                
                secondAlignedReversed.append(self.gapSymbol)
                
        seq1Aligned = "".join(reversed(firstAlignedReversed))
        seq2Aligned = "".join(reversed(secondAlignedReversed))
        matchTypeAligned = "".join(reversed(matchTypeReversed))
        
       
        return seq1Aligned,seq2Aligned,matchTypeAligned, score
        
