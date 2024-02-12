# Main function of market sim
import numpy as np
import matplotlib.pyplot as plt
import supplySide as sup
import products as prod

# Testing imported classes and their functionalities

# 
#mat1 = sup.RawMaterial("wood")
#mat1.setRandomSupplyPars()
#mat1.increaseDemand(100)
#mat1.getPrice()
#mat1.printInfo()

#ax = mat1.plotSupplyCurve()
#plt.show()

#mat1.printInfo()

# Create raw material objects with random supply pars
print("Creating raw material objects and their supply curves")
matNameList = ["wood","clay","metal","wheat","meat"]
matList = [sup.RawMaterial(s) for s in matNameList]
for i in range(len(matList)):
    matList[i].setRandomSupplyPars()
    matList[i].printInfo()
    print("\n --- \n")
print("{0} raw material types are initialized".format(sup.RawMaterial.nRawMaterials))

# Create product objects
print("Creating product objects and their material requirements!")
prodNameList = ["plank","brick","knife","flour","steak"]
prodList = [prod.Product(s,matNameList) for s in prodNameList]
for i in range(len(prodList)):
    prodList[i].setMaterialObjects(matList)
    prodList[i].setRandomMaterialReqs()
    prodList[i].printInfo()
    print("\n --- \n")
print("{0} product types are initialized".format(prod.Product.nProducts))

# Testing accessing material object from a product object
prodList[0].matObjectDict["wood"].printInfo()
prodList[1].matObjectDict["wood"].increaseDemand(100)
prodList[0].matObjectDict["wood"].printInfo()
prodList[1].matObjectDict["wood"].setDemand(0)

# Calculate total price for the required product amounts below
prodReqs = [100,200,50,10,1000]
for i in range(len(prodList)):
    prodList[i].setProduced(prodReqs[i])
    prodList[i].incMaterialDemands() # End loop here, need to enter all demands before taking further actions

# Check whether raw material demand and price updated correctly
print("Checking raw material demand and price after entry of required product amounts")
for i in range(len(matList)):
    matList[i].getPrice()
    matList[i].printInfo()
    print("\n --- \n")

# Now calculate total cost of required products due to raw material requirements
for i in range(len(prodList)):
    prodList[i].getMaterialCostPerItem()
    prodList[i].getTotalMaterialCost()
    prodList[i].printInfo()
    print("\n --- \n")
