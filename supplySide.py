# This file handles the supply of raw materials
import numpy as np
import matplotlib.pyplot as plt

supSeed = 122807528840384100672342137672332423405
supRng = np.random.default_rng(supSeed)

# Generic function to describe supply
def genericSupplyFormula(supCoeff, supExp, supInter):
    return lambda price : supCoeff*(price**supExp)+supInter

# Class for raw materials, contains supply curve, and hence a function to get price as based on demand
class RawMaterial:
    
    def __init__(self, name, supCoeffIn=5, supExpIn=1, supInterIn=10):
        self.name = name
        self.updateSupplyPars(supCoeffIn, supExpIn, supInterIn)
        self.demanded = 0
        self.price = 0
        self.totalPrice = 0
    
    def updateSupplyPars(self, supCoeffIn, supExpIn, supInterIn):
        self.supCoeff = supCoeffIn
        self.supExp = supExpIn
        self.supInter = supInterIn
        
    def setRandomSupplyPars(self):
        supCoeff = supRng.normal(1,0.1,1)
        supExp = supRng.normal(1.25,0.05,1)
        supInter = (5-1)*supRng.random() + 1
        self.updateSupplyPars(supCoeff, supExp, supInter)
    
    # Generate supply formula from parameters and get price from demand
    def getPriceFromDemand(self, demand):
        supplyFormula = genericSupplyFormula(self.supCoeff, self.supExp, self.supInter)
        self.price = supplyFormula(demand)
        return self.price
    
    # Use self.demand as input for supply Formula
    def getPrice(self): 
        return self.getPriceFromDemand(self.demanded)
        
    # Increase demand
    def increaseDemand(self, newDemand):
        self.demanded = self.demanded + newDemand
    
    # Print Object Info
    def printInfo(self):
        print("Info for raw material: {0}".format(self.name))
        print("Supply Curve for this material is: P(Q)={0}*Q**{1}+{2}".format(self.supCoeff, self.supExp, self.supInter))
        print("Current demanded quantity is: {0}$".format(self.demanded))
        print("Price per quantity to produce the demanded quantity is: {0}$".format(self.price))
        
    # Make a standard supply curve graph
    def plotSupplyCurve(self):
        # Save current demand and price to be restored later
        demandedSave = self.demanded
        priceSave = self.price
        # Loop over some example demands and calculate the corresponding prices
        testDemands = np.linspace(0,1000,1000)
        testPrices = [self.getPriceFromDemand(d) for d in testDemands]
        # Restore demand and price
        self.demanded = demandedSave
        self.price = priceSave
        # Prepare plot
        f, ax = plt.subplots()
        ax.plot(testDemands,testPrices)
        ax.set_title("{0} supply curve".format(self.name))
        ax.set_xlabel("Demanded Quantity")
        ax.set_ylabel("Price per Item ($)")
        return ax