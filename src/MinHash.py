'''
Created on Jul 20, 2014

@author: ppx10
'''
from random import randint
from _operator import xor
from operator import mod
import sys


class MinHash(object):
    '''
    classdocs
    '''


    def __init__(self, hashCnt=200):
        '''
        Constructor
        '''
        self.randomNums = [randint(-sys.maxsize+1, sys.maxsize) for i in range(0, hashCnt)]  # @UnusedVariable
    
    def simpleHash(self, source, seed):
        return xor((source >> mod(seed, 64)), seed)
    
    def minHashValues(self, seq, shingleLength):
        '''
        
        '''
        hashedShingles = []
        for i in range(0, len(seq) - shingleLength + 1):
            hashedShingles.append(hash(seq[i:i + shingleLength]))
        minValues = []
        
        for randNum in self.randomNums:
            minValues.append(min([self.simpleHash(hashedShingle, randNum) for hashedShingle in hashedShingles]))
        
        return set(minValues)
        
        
    def compareSets(self, set1, set2):
        '''
        
        '''
        return len((set1 & set2))/len((set1 | set2))
    
    def similarity(self, seq1, seq2, shingleLength=7):
        '''
        
        '''
        
        if(len(seq1)>=shingleLength and len(seq2) >=shingleLength):
        
            set1 = self.minHashValues(seq1, shingleLength)
            set2 = self.minHashValues(seq2, shingleLength)
            
            return self.compareSets(set1, set2)
            
        
        elif(len(seq1)<shingleLength):
            raise Exception("The first sequence is too short for a shingle length of",shingleLength)
        else:
            raise Exception("The second sequence is too short for a shingle length of",shingleLength)

