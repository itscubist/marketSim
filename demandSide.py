# This file handles the demands from the costumers
import numpy as np
import matplotlib.pyplot as plt

demSeed = 321867528840384100622142137672332423491
demRng = np.random.default_rng(demSeed)

class Costumer:
    
    nCostumers = 0
    
    def __init__(self, name, productNamesIn):
        self.name = name
        self.productKeys(productNamesIn)
        self.totalBudget = 0
        self.remBudget = 0
        nCostumers += 1
        
    # Prepare dictionary keys based on products on sale
    def productKeys(self, productNamesIn):
        self.prodProbDict = dict.fromkeys(productNamesIn,0)
        self.prodObjectDict = dict.fromkeys(productNamesIn,[])
        self.boughtProducts = dict.fromkeys(productNamesIn,0)
        
    # Prepare dictionary for relative product probabilities
    def setProductProbabilities(self, productProbs):
        self.prodProbDict = {k:v for (k,v) in zip(self.prodProbDict.keys(),productProbs)}
    
    # Set product objects (which should be created earlier)
    def setProductObjects(self, prodObjects):
        self.prodObjectDict = {k:v for (k,v) in zip(self.prodObjectDict.keys(),prodObjects)}
    
    # Randomly determine product probabilities for a costumer
    def setRandomProductProbabilities(self):
        nProbs = len(self.prodProbDict)
        # Need nProbs random variables within [0,1) with the constraint their sum is 1
        # nProbs randoms - 1 constraint means generating nProbs-1 random variables and using their sorted difference. Below is example for nProb=5
        # For uncorrelated but sorted random variables 1,r1,r2,r3,r4,0 where r1>r2>r3>r4, 1-r1,r1-r2,r2-r3,r3-r4,r4-0 will be 5 random variables adding up to 1
        randProbs = -1*np.diff( np.concatenate((np.concatenate((1,sorted(np.random.random(nProbs), reverse=True)),axis=None),0), axis=None) )
        self.setProductProbabilities(randProbs)
    
    # Set total costumer budget, and equate remaining budget to the total budget
    def setTotalBudget(self, totalBudgetIn):
        self.totalBudget = totalBudgetIn
        self.remBudget = self.totalBudget
        
    # Set budget randomly from global costumer budget distribution, and equate remaining budget to the total budget
    def setRandomTotalBudget(self):
        # First parameter determines the shape of the distribution (falls faster with larger par), the multiplicative factor just scales the budget 
        self.totalBudget = demRng.pareto(2,1)*10000
        self.remBudget = self.totalBudget
        return self.totalBudget
    
    # Costumers will keep buying products based on the assigned probabilities, as long as they can afford it
    def buyProducts(self):
        pass
    
    # Print important quantities
    def printInfo(self):
        print("Costumer name is: {0}".format(self.name))
        print("Total costumer budget is: {0}".format(self.totalBudget))
        for k in self.prodProbDict:
            print("Probability of buying product: {0} is {1}".format(k,self.prodProbDict(k)))
        