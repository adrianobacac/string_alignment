'''
Created on Sep 15, 2014

@author: ppx10
'''


class SeqAndPercentageList(object):
    '''
    classdocs
    '''
    '''
    data = [[percentage1, seq1],[percentage2, seq2],...]
    '''
    data = []
    count = 10
    
    
    def __init__(self, count=10):
        self.count = count
        for i in range(0, self.count):  # @UnusedVariable
            self.data.append([-1, ""])
    
    def __str__(self):
        return str(self.getList())
    
    def getList(self):
        return sorted([pair for pair in self.data if pair[0]>=0], reverse=True)
        

    def add(self, percentage, seq):    
        percentages=[pair[0] for pair in self.data]
        
        if(percentage <= min(percentages)):
            return False
        else:
            newIndex=percentages.index(min(percentages))
            self.data[newIndex][0]=percentage
            self.data[newIndex][1]=seq
            
