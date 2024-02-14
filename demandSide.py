# This file handles the demands from the costumers
import numpy as np
import matplotlib.pyplot as plt
import copy
import products as prod

demSeed = 321867528840384100622142137672332423491
demRng = np.random.default_rng(demSeed)

class Costumer:
    
    nCostumers = 0
    combinedBudget = 0
    combinedRemBudget = 0
    
    def __init__(self, name, productNamesIn):
        self.name = name
        self.productKeys(productNamesIn)
        self.totalBudget = 0
        self.remBudget = 0
        Costumer.nCostumers += 1
    
    # For resetting global class vars if needed
    def resetClassVars():
        Costumer.nCostumers = 0
        Costumer.combinedBudget = 0
        Costumer.combinedRemBudget = 0
        
    # Prepare dictionary keys based on products on sale
    def productKeys(self, productNamesIn):
        self.prodProbDict = dict.fromkeys(productNamesIn,0)
        self.prodObjectDict = dict.fromkeys(productNamesIn,[])
        self.boughtProdDict = dict.fromkeys(productNamesIn,0)
        
    # Prepare dictionary for relative product probabilities
    def setProductProbabilities(self, productProbs):
        self.prodProbDict = {k:v for (k,v) in zip(self.prodProbDict.keys(),productProbs)}
        
    # Get probabilities
    def getProductProbabilities(self):
        return list(self.prodProbDict.values())
    
    # Set product objects (which should be created earlier)
    def setProductObjects(self, prodObjects):
        self.prodObjectDict = {k:v for (k,v) in zip(self.prodObjectDict.keys(),prodObjects)}
    
    # Randomly determine product probabilities for a costumer
    def setRandomProductProbabilities(self):
        nProbs = len(self.prodProbDict)
        # Need nProbs random variables within [0,1) with the constraint their sum is 1
        # nProbs randoms - 1 constraint means generating nProbs-1 random variables and using their sorted difference. Below is example for nProb=5
        # For uncorrelated but sorted random variables 1,r1,r2,r3,r4,0 where r1>r2>r3>r4, 1-r1,r1-r2,r2-r3,r3-r4,r4-0 will be 5 random variables adding up to 1
        randProbs = -1*np.diff( np.concatenate((np.concatenate((1,sorted(np.random.random(nProbs-1), reverse=True)),axis=None),0), axis=None) )
        self.setProductProbabilities(randProbs)
    
    # Set total costumer budget, and equate remaining budget to the total budget
    def setTotalBudget(self, totalBudgetIn):
        self.totalBudget = totalBudgetIn
        self.remBudget = copy.copy(self.totalBudget)
        
    # Set budget randomly from global costumer budget distribution, and equate remaining budget to the total budget
    def setRandomTotalBudget(self):
        # First parameter determines the shape of the distribution (falls faster with larger par), the multiplicative factor just scales the budget 
        self.totalBudget = float(demRng.pareto(2,1)*1000)
        self.remBudget = copy.copy(self.totalBudget)
        return self.totalBudget
    
    # Costumers will keep buying products based on the assigned probabilities, as long as they can afford it
    def buyProducts(self):
        # Put prices and probs into numpy arrays
        prices = np.array([self.prodObjectDict[k].getSellPrice() for k in self.prodObjectDict])
        probs = np.array([self.prodProbDict[k] for k in self.prodProbDict])
        
        while True:
            # Get number of remaining products
            prodCounts = np.array([self.prodObjectDict[k].getRemaining() for k in self.prodObjectDict])
            # Set products outside the costumer budget (or out of stock) to 0 probability
            probsWithinBudget = np.array([probs[i] if ( (self.remBudget-prices[i])>=0 and prodCounts[i]>0 ) else 0 for i in range(len(probs))])
            # Set up break condition: if all probabilities are 0, then cannot buy items anymore
            if sum(probsWithinBudget) <=0:
                break
            # Renormalize the probabilities (now there is no issue to divide by 0)
            probsWithinBudget = probsWithinBudget/sum(probsWithinBudget)
            # Buy a product based on the probabilities and update remaining costumer budget, total product sale count, and products of this type bought by this costumer
            selProductIndex = demRng.choice(list(self.prodObjectDict.keys()),p=probsWithinBudget)
            self.remBudget -= self.prodObjectDict[selProductIndex].getSellPrice()
            self.prodObjectDict[selProductIndex].sales += 1
            self.boughtProdDict[selProductIndex] += 1
            #print("In buyProducts function: Bought {0} with cost {1}, remaining budget is {2} of total budget {3}" \
            #    .format(selProductIndex,self.prodObjectDict[selProductIndex].getSellPrice(), self.remBudget, self.totalBudget))
    
    # Add total budget and remaining budget to the combined costumer budgets
    def setCombinedBudgets(self):
        combinedBudget += self.totalBudget
        combinedRemBudget += self.remBudget

    # Print important quantities
    def printInfo(self):
        print("Costumer name is: {0}".format(self.name))
        print("Total costumer budget was: {0:.2f}".format(self.totalBudget))
        for k in self.prodProbDict:
            print("Price of product: {0} is {1:.2f}".format(k,self.prodObjectDict[k].getSellPrice()))
            print("Probability of buying product (as budget permits): {0} is {1:.2f}".format(k,self.prodProbDict[k]))
            print("Number of bought products of type: {0} is {1}".format(k,self.boughtProdDict[k]))
        print("Remaining budget after purchases:{0:.2f}".format(self.remBudget))


# Function to plot budget distribution of the costumers
def plotBudgetDist(costumerList):
        totalBudgets = np.array([c.totalBudget for c in costumerList])
        nBins = round(len(totalBudgets)/10) if len(totalBudgets)>10 else 1
        f, ax = plt.subplots()
        ax.hist(totalBudgets,nBins)
        ax.set_title("Costumer Budget Distribution")
        ax.set_xlabel("Total Budget of A Costumer")
        ax.set_ylabel("Counts")
        return ax
    
# Function to return all costumers budget distribution
def plotBudgetPerProduct(costumerList):
    # Get product names from first costumer
    prodNames = list(costumerList[0].prodProbDict.keys())
    # Estimate product budgets as sum over costumers totalBudget*probability of product
    prodBudgets = sum([c.totalBudget*np.array(list(c.prodProbDict.values())) for c in costumerList])
    print(prodBudgets)
    # Plot
    fig, ax = plt.subplots()
    ax.pie(prodBudgets, labels=prodNames)
