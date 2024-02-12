# Main function of market sim
import numpy as np
import matplotlib.pyplot as plt
import supplySide as sup

# Testing imported classes and their functionalities

# 
mat1 = sup.RawMaterial("wood")
mat1.setRandomSupplyPars()
mat1.increaseDemand(100)
mat1.getPrice()
mat1.printInfo()

ax = mat1.plotSupplyCurve()
plt.show()

mat1.printInfo()

#supplyFormula = supplySide.genericSupplyFormula(10,2,12)
#print(supplyFormula(100))