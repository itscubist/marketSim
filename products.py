# This file handles the product properties and functions
import numpy as np
import matplotlib.pyplot as plt

prodSeed = 122807528840384100672342237672332433418
prodRng = np.random.default_rng(prodSeed)

# Product class
class Product:
    
    # Initialize
    def __init__(self, name, materialNamesIn):
        self.name = name
        self.materialKeys(materialNamesIn)
        self.produced = 0
    
    # Prepare dictionary keys based on available raw materials
    def materialKeys(self, materialNames):
        self.materialDict = dict.fromkeys(materialNames,[])
        
    # Prepare dictionary values based on required materials
    def setMaterialReqs(self, materialReqs):
        self.materialDict = {k:v for (k,v) in zip(self.materialDict.keys(),materialReqs)}
        
    # Set required materials randomly
    def setRandomMaterialReqs(self):
        # Determine the number of required material types: either 1 or 2 (only if there are 2 or more material types available)
        self.materialTypeCtr = prodRng.integers(1,max(3,len(self.materialDict)+1))
        # Determine which raw materials by shuffling and taking first elements:
        materialListTemp = [k for k in self.materialDict]
        prodRng.shuffle(materialListTemp)
        # Update first element (and second element if there are two required material types) by a random integer between 1 to 3 inclusive
        self.materialDict.update(materialListTemp[0], prodRng.integers(1,4))
        if self.materialTypeCtr>1:
            self.materialDict.update(materialListTemp[1], prodRng.integers(1,4))

    def increaseProduced(self, produceInc):
        self.produced = self.produced + produceInc
        
    def setTotalMaterialCost(self, matCost):
        self.totalMaterialCost = matCost
        
    def printInfo(self):
        print("Product name is:[0]".format(self.name))
        print("Raw material requirements are:")
        for k in self.materialDict:
            print("Material: [0], Requirement: [1]".format(k,self.MaterialDict[k]))