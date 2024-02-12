# This file handles the product properties and functions
import numpy as np
import matplotlib.pyplot as plt
import supplySide as sup

prodSeed = 122807528840384100672342237672332433418
prodRng = np.random.default_rng(prodSeed)

# Product class
class Product:
    # Number of products
    nProducts = 0
    # Initialize
    def __init__(self, name, materialNamesIn):
        self.name = name
        self.materialKeys(materialNamesIn)
        self.produced = 0
        self.materialCostPerItem = 0
        self.totalMaterialCost = 0
        Product.nProducts += 1
    
    # Prepare dictionary keys based on available raw materials
    def materialKeys(self, materialNames):
        self.materialDict = dict.fromkeys(materialNames,0)
        self.matObjectDict = dict.fromkeys(materialNames,[])
        
    # Prepare dictionary values based on required materials
    def setMaterialReqs(self, materialReqs):
        self.materialDict = {k:v for (k,v) in zip(self.materialDict.keys(),materialReqs)}
    
    # Set raw material objects (which should be created earlier)
    def setMaterialObjects(self, matObjects):
        self.matObjectDict = {k:v for (k,v) in zip(self.matObjectDict.keys(),matObjects)}
        
    # Set required materials randomly
    def setRandomMaterialReqs(self):
        # Determine the number of required material types: either 1 or 2 (only if there are 2 or more material types available)
        self.materialTypeCtr = prodRng.integers(1,max(3,len(self.materialDict)+1))
        # Determine which raw materials by shuffling and taking first elements:
        materialListTemp = [k for k in self.materialDict]
        prodRng.shuffle(materialListTemp)
        # Update first element (and second element if there are two required material types) by a random integer between 1 to 3 inclusive
        self.materialDict[materialListTemp[0]] = prodRng.integers(1,4)
        if self.materialTypeCtr>1:
            self.materialDict[materialListTemp[1]] = prodRng.integers(1,4)

    def increaseProduced(self, produceInc):
        self.produced += produceInc
        
    def setProduced(self, producedIn):
        self.produced = producedIn
    
    # Add demands to the appropriate raw materials    
    def incMaterialDemands(self):
        for k in self.matObjectDict:
            self.matObjectDict[k].increaseDemand(self.produced*self.materialDict[k])
    
    # Calculate product cost per item, based on raw material prices which are determined once demands from all products are entered to each raw material type
    def getMaterialCostPerItem(self):
        self.materialCostPerItem = sum([self.materialDict[k]*self.matObjectDict[k].getPrice() for k in self.materialDict])
        return self.materialCostPerItem
    
    # Total product costs
    def getTotalMaterialCost(self):
        self.getMaterialCostPerItem()
        self.totalMaterialCost = self.materialCostPerItem * self.produced
        return self.totalMaterialCost
        
    # Print info related to the product        
    def printInfo(self):
        print("Product name is:{0}".format(self.name))
        print("Total produced quantity: {0}".format(self.produced))
        print("Raw material requirements per item are:")
        for k in self.materialDict:
            print("Material: {0}, Requirement: {1}, Cost Per Required Material: {2}".format(k,self.materialDict[k],self.matObjectDict[k].getPrice()))
        print("Cost per product: {0}, and cost for all products: {1}".format(self.materialCostPerItem, self.totalMaterialCost))
        