'''
Created on Jul 26, 2014

@author: ppx10
'''

class SimilarityMatrix(object):
    '''
    classdocs
    '''


    def __init__(self, path):
        '''
        Constructor
        '''
        self.table = {}
        self.parse(path)
        
    def parse(self, path):
        inputFile = open(path)
        
        data = inputFile.read().split("\n")
        
        columnInterpretation = data[0].split(" ")
        
        for index, row in enumerate(data[1:]):
            if(row == ""):
                continue
            rowData = row.split(" ")
            
            self.table[rowData[0]]={}
            
            for index, number in enumerate(rowData[1:]):
                
                self.table[rowData[0]].update({columnInterpretation[index]:int(number)})
        inputFile.close()
        
    def getTable(self):
        return self.table
