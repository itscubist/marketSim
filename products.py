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
        self.sellPrice = 0
        self.profitPerItem = 0
        self.sales = 0
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

    # Increase produced amount
    def increaseProduced(self, produceInc):
        self.produced += produceInc
        
    # Set produced amount to a value
    def setProduced(self, producedIn):
        self.produced = producedIn
        
    # Get produced amount
    def getProduced(self):
        return self.produced
    
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
        #self.getMaterialCostPerItem()
        self.totalMaterialCost = self.materialCostPerItem * self.produced
        return self.totalMaterialCost
    
    # Set sales
    def setSales(self, sellCountIn):
        self.sales = sellCountIn
    
    #Increment sales
    def incSales(self):
        self.sales += 1
        
    # Get sales (sold products of this type)
    def getSales(self):
        return self.sales
    
    #Get remaining number of products
    def getRemaining(self):
        return self.produced - self.sales
    
    # Set profit per item -> call after setting material costs
    def setProfit(self, profitIn):
        self.profitPerItem = profitIn
        self.sellPrice = self.materialCostPerItem + self.profitPerItem
        
    # Set profit as percentage of cost -> call after material costs
    def setProfitPercentage(self, profitPercentIn):
        profitIn = self.materialCostPerItem * (profitPercentIn/100.0)
        self.setProfit(profitIn)
        
    # Get determined sell price
    def getSellPrice(self):
        return self.sellPrice
    
    # Get determined profit
    def getProfit(self):
        return self.profitPerItem
    
    # Get total potential profit (If all produced items are sold at the sell price)
    def getPotTotalProfit(self):
        return self.profitPerItem * self.produced
    
    # Get total potential price (If all produced items are sold at the sell price)
    def getPotTotalPrice(self):
        return self.sellPrice * self.produced
    
    # Get total price (Total of actually sold products of this type)
    def getTotalPrice(self):
        return self.sellPrice * self.sales
    
    # Get total actual profit (Based on number of actual products sales)
    def getTotalProfit(self):
        return self.getTotalPrice() - self.getTotalMaterialCost()
        
    # Print info related to the product        
    def printInfo(self):
        print("Product name is:{0}".format(self.name))
        print("Total produced quantity: {0}".format(self.produced))
        print("Raw material requirements per item are:")
        for k in self.materialDict:
            print("Material: {0}, Requirement: {1}, Cost Per Required Material: {2}".format(k,self.materialDict[k],self.matObjectDict[k].getPrice()))
        print("Cost per product: {0}, and cost for all products: {1}".format(self.materialCostPerItem, self.totalMaterialCost))
        print("Designated profit per item: {0}. Corresponding price per item: {1}".format(self.profitPerItem,self.sellPrice))
        print('Total potential profit (if all products are sold): {0}. Corresponding total price: {1}'.format(self.getPotTotalProfit(),self.getPotTotalPrice()))
        print('Total actual profit (based on actual sold products): {0}. Corresponding total price: {1}'.format(self.getTotalProfit(),self.getTotalPrice()))
        print('Produced: {0}, Sold:{1}, Remaining:{2}'.format(self.produced,self.sales,self.getRemaining()))
        
        