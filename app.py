# Visual application for marketSim with shiny core
from shiny import App, reactive, render, ui, module, Inputs, Outputs, Session
# Python modules
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# Project modules
import supplySide as sup
import products as prod
import demandSide as dem
import companies as comp

# Create raw material objects with random supply pars
print("Creating raw material objects and their supply curves")
matNameList = ["nqh345","nqa344","trm222","crystals","nanites"]
matList = [sup.RawMaterial(s) for s in matNameList]
for i in range(len(matList)):
    matList[i].setRandomSupplyPars()
    matList[i].printInfo()
    print("\n --- \n")
print("{0} raw material types are initialized".format(sup.RawMaterial.nRawMaterials))

# Create product objects
print("Creating product objects and their material requirements!")
prodNameList = ["F302","X304","Viper","Starfury","Jumper"]
prodList = [prod.Product(s,matNameList) for s in prodNameList]
for i in range(len(prodList)):
    prodList[i].setMaterialObjects(matList)
    prodList[i].setRandomMaterialReqs()
    prodList[i].printInfo()
    print("\n --- \n")
print("{0} product types are initialized".format(prod.Product.nProducts))




# Create costumers
costumerNameList = ["C{0}".format(i+1) for i in range(1000)]
costumerList = [dem.Costumer(s, prodNameList) for s in costumerNameList]
dem.Costumer.setRandomBudgetMean(25,5)
for c in costumerList:
    # Random initialization routine
    c.setProductObjects(prodList)
    c.setRandomTotalBudget()
    c.setRandomProductProbabilities()
    
# Set values
testCompanyCapital = 100000
#capitalPerProduct = np.ones(len(prodList))*(testCompanyCapital/len(prodList))
capitalPerProduct = np.array([20000,20000,30000,20000,10000])
testCompanyProfitPercentage = 5
#plannedProfitPerProduct = np.ones(len(prodList))*testCompanyProfitPercentage
plannedProfitPerProduct = np.array([5,10,5,1,3])

# Create company and buy products
testCompany = comp.Company("testCompany",prodNameList,matNameList,testCompanyCapital)
testCompany.setMaterialObjects(matList)
testCompany.setProductObjects(prodList)
testCompany.softResetProductsAndMaterials()
testCompany.setProductInvestments(capitalPerProduct)
testCompany.setProductProfitPercentages(plannedProfitPerProduct)
productArray, argTuple = testCompany.calcProductsFromInvestment()
testCompany.makeProducts()

# Reset costumers to start, and let them buy products
for c in costumerList:
    c.softReset()
    c.buyProducts()

testCompany.calcProfits()
testCompany.printInfo()

# To be shown in the app in tables:
# Function to init a constant valued data frame to be used as a table

def initTableDataFrame(columnNames,rowNames,initValue=0.0):
    tempDict = dict.fromkeys(columnNames,[])
    tempVals = [rowNames] + [[initValue for r in rowNames] for c in range(len(columnNames)-1)]
    tempDict = {k:v for (k,v) in zip(tempDict.keys(),tempVals)}
    return pd.DataFrame(tempDict)

# Init production plan data frame
prodPlanColumns = ["Product Name","Invested","Produced","Cost Per Item","Price Per Item","Profit Per Sale", "Cost", "Price", "Expected Profit"]
prodPlanRows = prodNameList + ["All products"]
prodPlanDf = initTableDataFrame(prodPlanColumns,prodPlanRows,0.0)
# Init product sales data frame
prodSalesColumns = ["Product Name", "Produced", "Sold", "Remaining", "Expected Profit", "Actual Profit"]
prodSalesRows = prodNameList + ["All products"]
prodSalesDf = initTableDataFrame(prodSalesColumns,prodSalesRows,0.0)

# Some functions for the app

# To track changes in server function
counter = reactive.Value()
counter.set(0)

# UI function for plots in materials tab
@module.ui
def materialPlotUi(matName):
    return ui.nav_panel(matName, ui.output_plot("supplyCurve"))
# server function for plots in materials tab
@module.server
def materialPlotServer(input: Inputs, output: Outputs, session: Session, matNameIn):
    @output
    @render.plot
    @reactive.event(counter)
    def supplyCurve(matName=matNameIn):       
        f, ax = matList[matNameList.index(matName)].plotSupplyCurve()
        return f

@module.ui
def productInvestUi(pName):
    return ui.panel_well(
        ui.h1("Product: {0}".format(pName)),
        ui.row(
            ui.column(5,ui.input_slider("inv","Investment",0,testCompany.totalCapital,0)),
            ui.column(5,ui.input_slider("prof","Profit",0,100,0)),
        ),
    )
    
@module.server
def productInvestServer(input: Inputs, output: Outputs, session: Session):
    return (input.inv(), input.prof())
    


app_ui = ui.page_fluid(
    # Application title
    ui.panel_title(
        ui.h1("WELCOME TO MARKET SIMULATOR!")
    ),
    ui.page_navbar(
        # Tab 1
        ui.nav_panel("Company",
            # Tab title
            ui.panel_title(
                ui.h5("Decide on your investments and profit margins"),
            ),
            ui.row(
                ui.column(5,ui.output_text("totalCap")),
                ui.column(5,ui.output_text("remCap")),
            ),
            # Sidebars
            ui.layout_sidebar(
                # Sidebar
                ui.panel_sidebar(
                    [productInvestUi(p,p) for p in prodNameList],
                    ui.input_action_button("butProdProp","Update Plan"),
                    ui.input_action_button("butSell","Sell Products"),
                    ui.input_action_button("butReset","Reset All"),
                ),
                # Main
                ui.panel_main(
                    ui.h5("INVESTMENT PLAN"),
                    ui.output_data_frame("prodPlanDfVis"),
                    ui.h5("AFTER SALE REPORT"),
                    ui.output_data_frame("prodSalesDfVis"),
                ),
            ),
         ),
        
        #Tab 2
        ui.nav_panel("Materials",
            ui.panel_title(
                ui.h5("MATERIAL SUPPLY CURVES!"),
            ),
            ui.page_navbar(
                [materialPlotUi(m,m) for m in matNameList]
            )
        ),
        #Tab 3
        ui.nav_panel("Products",
            ui.h5("Material Requirements of Products"),
            ui.output_data_frame("matReqDfVis"),
        ),
        
        #Tab 4
        ui.nav_panel("Costumers",
            ui.row(
                ui.column(6,ui.output_plot("budgetDist")),
                ui.column(6,
                    ui.h5("Budget per Product"),
                    ui.output_plot("productMarketShare"),
                ),
            ),
        ),
        #Tab 5
        ui.nav_panel("Control Panel",
            ui.h5("Generate new parameters for the simulation"),
            ui.input_action_button("randomize","Generate Random Market"),
        )
        
    ),
)

def server(input: Inputs, output: Outputs, session: Session):
    
    # Company Tab: Render total and remaining capitals
    @output
    @render.text
    @reactive.event(counter)
    def totalCap():
        return "Total Capital: {0:.1f}$".format(testCompany.totalCapital)
    @output
    @render.text
    @reactive.event(counter)
    def remCap():
        return "Remaining Capital: {0:.1f}$".format(testCompany.remCapital)
    

    # Company Tab: Button effects for calculations
    @reactive.Effect
    @reactive.event(input.butProdProp)
    def updateInvestmentPlan():
        # Call company functions
        inputTupleList = [productInvestServer(p) for p in prodNameList]
        testCompany.setProductInvestments([i for (i,p) in inputTupleList])
        testCompany.setProductProfitPercentages([p for (i,p) in inputTupleList])
        productArray, argTuple = testCompany.calcProductsFromInvestment()
        testCompany.makeProducts()
        global prodPlanDf
        #Update prodPlanDf (a bit inelegantly):
        #prodPlanColumns = ["Product Name","Invested","Produced","Cost Per Item","Price Per Item","Profit Per Sale", "Cost", "Price", "Expected Profit"]
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[1]] = [testCompany.prodInvestDict[p] for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[1]] = sum([testCompany.prodInvestDict[p] for p in prodNameList])
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[2]] = [testCompany.prodCountDict[p] for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[2]] = sum([testCompany.prodCountDict[p] for p in prodNameList])
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[3]] = [testCompany.prodObjectDict[p].getMaterialCostPerItem() for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[3]] = sum([testCompany.prodObjectDict[p].getMaterialCostPerItem() for p in prodNameList])
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[4]] = [testCompany.prodObjectDict[p].getSellPrice() for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[4]] = sum([testCompany.prodObjectDict[p].getSellPrice() for p in prodNameList])
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[5]] = [testCompany.prodObjectDict[p].getProfit() for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[5]] = sum([testCompany.prodObjectDict[p].getProfit() for p in prodNameList])
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[6]] = [testCompany.prodObjectDict[p].getTotalMaterialCost() for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[6]] = sum([testCompany.prodObjectDict[p].getTotalMaterialCost() for p in prodNameList])
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[7]] = [testCompany.prodObjectDict[p].getPotTotalPrice() for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[7]] = sum([testCompany.prodObjectDict[p].getPotTotalPrice() for p in prodNameList])
        prodPlanDf.loc[0:len(prodNameList)-1,prodPlanColumns[8]] = [testCompany.prodObjectDict[p].getPotTotalProfit() for p in prodNameList]
        prodPlanDf.loc[len(prodNameList),prodPlanColumns[8]] = sum([testCompany.prodObjectDict[p].getPotTotalProfit() for p in prodNameList]) 
    
        counter.set(counter()+1)
    
    @reactive.Effect
    @reactive.event(input.butSell)
    def updateSales():
        # Call functions for selling
        for c in costumerList:
            c.softReset()
            c.buyProducts()
        testCompany.calcProfits()
        #Update data frame for sales and profit
        global prodSalesDf
        #prodSalesColumns = ["Product Name", "Produced", "Sold", "Remaining", "Expected Profit", "Actual Profit"]
        prodSalesDf.loc[0:len(prodNameList)-1,prodSalesColumns[1]] = [testCompany.prodObjectDict[p].getProduced() for p in prodNameList]
        prodSalesDf.loc[len(prodNameList),prodSalesColumns[1]] = sum([testCompany.prodObjectDict[p].getProduced() for p in prodNameList])
        prodSalesDf.loc[0:len(prodNameList)-1,prodSalesColumns[2]] = [testCompany.prodObjectDict[p].getSales() for p in prodNameList]
        prodSalesDf.loc[len(prodNameList),prodSalesColumns[2]] = sum([testCompany.prodObjectDict[p].getSales() for p in prodNameList])
        prodSalesDf.loc[0:len(prodNameList)-1,prodSalesColumns[3]] = [testCompany.prodObjectDict[p].getRemaining() for p in prodNameList]
        prodSalesDf.loc[len(prodNameList),prodSalesColumns[3]] = sum([testCompany.prodObjectDict[p].getRemaining() for p in prodNameList])
        prodSalesDf.loc[0:len(prodNameList)-1,prodSalesColumns[4]] = [testCompany.prodObjectDict[p].getPotTotalProfit() for p in prodNameList]
        prodSalesDf.loc[len(prodNameList),prodSalesColumns[4]] = sum([testCompany.prodObjectDict[p].getPotTotalProfit() for p in prodNameList])
        prodSalesDf.loc[0:len(prodNameList)-1,prodSalesColumns[5]] = [testCompany.prodObjectDict[p].getTotalProfit() for p in prodNameList]
        prodSalesDf.loc[len(prodNameList),prodSalesColumns[5]] = sum([testCompany.prodObjectDict[p].getTotalProfit() for p in prodNameList])
        
        counter.set(counter()+1)
    
    @reactive.Effect
    @reactive.event(input.butReset)
    def resetPlanAndSales():
        # Soft reset material, product and costumer values
        testCompany.softResetProductsAndMaterials()
        testCompany.setCapital(testCompanyCapital)
        for c in costumerList:
            c.softReset()
        # Reset data frames
        global prodPlanDf
        prodPlanDf = initTableDataFrame(prodPlanColumns,prodPlanRows,0.0)
        global prodSalesDf
        prodSalesDf = initTableDataFrame(prodSalesColumns,prodSalesRows,0.0)
        counter.set(counter()+1)
    
    # Company Tab: Render data frames as tables
    # Product Plan
    @output
    @render.data_frame
    @reactive.event(counter)
    def prodPlanDfVis():
        counter.set(0)
        return render.DataTable(prodPlanDf.round(2))
        # Product Plan
    @output
    @render.data_frame
    @reactive.event(counter)
    def prodSalesDfVis():
        counter.set(0)
        pd.set_option("display.precision", 2)
        return render.DataTable(prodSalesDf.round(2))
    
    # Materials Tab: Plot material supply curves
    [materialPlotServer(m,m) for m in matNameList]
    
    #Products Tab: Show product requirements
    @output
    @render.data_frame
    @reactive.event(counter)
    def matReqDfVis():
        # Make a data frame for material requirements of products (For visualization in table form):
        matReqDict = dict.fromkeys(["Material"]+prodNameList,[]) # Set keys
        matReqVals = [matNameList] + [[p.materialDict[m] for m in matNameList] for p in prodList]
        matReqDict = {k:v for (k,v) in zip(matReqDict.keys(),matReqVals)}
        matReqDf = pd.DataFrame(matReqDict)
        return render.DataTable(matReqDf)
    
    #Costumers Tab: Plot costumer distributions:
    @output
    @render.plot
    @reactive.event(counter)
    def budgetDist():
        f, ax = dem.plotBudgetDist(costumerList)
        return f
    
    @output
    @render.plot
    @reactive.event(counter)
    def productMarketShare():
        f, ax = dem.plotBudgetPerProduct(costumerList)
        return f
    
    # Control Panel Tab: 
    #randomize:
    @reactive.Effect
    @reactive.event(input.randomize)
    def generateNewParameters():
        #First call soft reset
        testCompany.softResetProductsAndMaterials()
        testCompany.setCapital(testCompanyCapital)
        # Now re-rerandomize:
        for m in matList:
            m.setRandomSupplyPars()
        for p in prodList:
            p.setRandomMaterialReqs()
        dem.Costumer.setRandomBudgetMean(25,5)
        for c in costumerList:
            c.softReset()
            c.setRandomTotalBudget()
            c.setRandomProductProbabilities()
        
        # Inc counter state to alert other functions
        counter.set(counter()+1)
    
    

        
    

app = App(app_ui, server)


