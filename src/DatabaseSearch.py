'''
Created on Sep 15, 2014

@author: ppx10
'''
from src.SeqAndPercentageList import SeqAndPercentageList
from src.AhoCorasick import ACAlgo
from src.SmithWaterman import SmithWaterman
from src.NeedlemanWunsch import NeedlemanWunsch
from src.test.SimilarityMatrix import SimilarityMatrix

class databaseSearch(object):
    '''
    classdocs
    '''
    databasePath=""
    dbSeqs=[]
    bestMatchingSeqs=None
    def __init__(self,databasePath):
        '''
        Constructor
        '''
        self.databasePath = databasePath
    
    def compare(self, query, compareSeq, shingleLength):
        ac = ACAlgo()
        total = 0
        for i in range(0, len(query) - shingleLength + 1):
            if(ac.add(query[i:i + shingleLength])):
                total+=1
        ac.join()
        
        results = ac.read(compareSeq)
        found = 0
        for result in results:
            
            if results[result] != []:
                found+=1

        return float(found)/total
            
    
    def searchAndCompare(self, queryProtein, bestDatabaseMatchCount = 10, shingleLength=5, local = True):
        
        dbTxt=open(self.databasePath)
        self.dbSeqs=dbTxt.read().split("\n")
        dbTxt.close()
        
        self.bestMatchingSeqs=SeqAndPercentageList(bestDatabaseMatchCount)
        
        for seq in self.dbSeqs:
            percentage=self.compare(queryProtein, seq, shingleLength)
            self.bestMatchingSeqs.add(percentage, seq)
        
        simMat=SimilarityMatrix("data/blosum62")
        
        if(local):
            aligner=SmithWaterman(simMat.getTable())
        else:
            aligner = NeedlemanWunsch(simMat.getTable())
            
        seqList=self.bestMatchingSeqs.getList()
        percentage=[element[0] for element in seqList]
        seqs=[element[1] for element in seqList]
        
        for i in range(0, bestDatabaseMatchCount):
            print("Match: %.2f" %(percentage[i]*100))    
            aligner.align(queryProtein, seqs[i], printing=True)
            print()