# import statements
import pandas as pd
import itertools

# Function that checks which variable assignments are different by 1 value
# Inputs: dictionary with keys that are names of minterms and values that are binary representations of the minterms
# Output: list of lists. Each sublist is a pair of minterms that can be combined
def check_differences(mintermDict):
    canCombineSolution = []
    for minterm1 in mintermDict.keys():
        for minterm2 in mintermDict.keys():
            if minterm1 != minterm2:
                # compare the binary representations for 2 minterms and count how many values they share
                numMatchingVals = 0
                for i in range(numberofVariables):
                    if mintermDict[minterm1][i] == mintermDict[minterm2][i]:
                        numMatchingVals += 1
                # if minterms only vary by 1 value, they can be combined
                if numMatchingVals == numberofVariables - 1:
                    # only add pair that is not already in the list of matches
                    if [minterm1,minterm2] not in canCombineSolution and [minterm2,minterm1] not in canCombineSolution:
                        canCombineSolution.append([minterm1,minterm2])
    return canCombineSolution

# Function that finds the minterms that cannot be combined
# Input: list of lists where each sublist is a pair of minterms that can be combined
# Output: list of minterms that cannot be combined
def find_uncombined_minterms(canCombineSolution):
    uncombinedMinterms = []
    #list of all the minterms that can be combined
    mintermsInCombinedList = list(itertools.chain(*canCombineSolution))
    # print("MINTERMS IN COMBINED LIST: ", mintermsInCombinedList)
    for minterm in mintermDict.keys():
        if minterm not in mintermsInCombinedList:
            uncombinedMinterms.append(minterm)
    return uncombinedMinterms

# Function: find reduced implicants (that have a dash instead of a binary value)
# Input: list of lists where each sublist is a pair of minterms that can be combined
# Output: Dictionary that keys: the names of combined minterms  and the values: the binary representation of the combined minterms
def find_reduced_minterms(canCombineSolution):
    combinedMinterms = {}
    for pair in canCombineSolution:
        minterm1 = mintermDict[pair[0]]
        minterm2 = mintermDict[pair[1]]
        newMinterm = []
        # print("MINTERM 1: ", minterm1)
        # print("MINTERM 2: ", minterm2)
        # print("========================")
        # constructing the new minterm value by value
        for i in range(numberofVariables):
            if minterm1[i] != minterm2[i]:
                newMinterm.append("-")
            else:
                newMinterm.append(minterm1[i])
        newMintermLabel = pair[0] + "," + pair[1]
        #print(newMintermLabel)
        if newMinterm not in combinedMinterms.values():
            combinedMinterms[newMintermLabel] = newMinterm

    return combinedMinterms

# convert a dictionary containing binarry representations to a formula
# dictionary has keys that are the names of the minterms and values that are the binary representations
# output: string that represents the final equation, e.g. A'B' + ACDE
def binary_rep_to_equation(truthTable, mintermDict):
    # Make a list with just the variable names
    columnNames = list(truthTable.columns)
    columnNames.pop(0)
    columnNames.pop()

    equationString = ""

    numTerms = 0
    for minNames, binRep in mintermDict.items():
        numTerms += 1
        for i in range(len(binRep)):
            # if the value is a 0, the equation has the not of a variable, e.g. B'
            if binRep[i] == 0:
                equationString = equationString + columnNames[i] + "'"
            # if the value is a 1, the equation has the variable, e.g. B
            elif binRep[i] == 1:
                equationString = equationString + columnNames[i]
            # if the value is "-", that means the variable is not included in the statement
            else:
                continue
        # add a "+" after each term of the equaation, except the last term
        if numTerms != len(mintermDict):
            equationString = equationString + " + "

    return equationString

# Count how often a minterm is included in a dictionary of implicants
# Input: Dictionary where the keys are implicant names and the values are binary representations of minterms
# Input: list with the minterms we want to count
# Output: list with the count of each minterm (the indexes line up)
def count_minterms(oneMinterms,solutionDict):
    countList = [0]*len(oneMinterms)
    for i in range(len(oneMinterms)):
        for allMinNames in solutionDict.keys():
            # make a list where each element is the name of a minterm
            listMinNames = list(allMinNames.split(","))
            for indvMinName in listMinNames:
                # if the solution covers that minterm, add to the count
                if indvMinName == oneMinterms[i]:
                    countList[i] += 1

    return(countList)
    
################################# FIND PRIME IMPLICANTS #################################

## Initial Data Processing
# read by in the truth table/model for the system:
truthTable = pd.read_excel('Test_Problem_Input.xlsx')
# number of variables is number of columns - 2 (to remove the "terms" column and "f" column)
numberofVariables = len(truthTable.columns) - 2
locationOfFirstVar = 1

# find the minterms that have a truthTable value of 1 or indifferent (x)
mintermsValOne = (truthTable.loc[truthTable['f'] == 1])
mintermsValX = (truthTable.loc[truthTable['f'] == "x"])
mintermRows = pd.concat([mintermsValOne,mintermsValX])

# make a dictionary to store the solutions
# keys: combinations of minterms, e.g. "m1,m2,m3,m4"
# values: binary representation of minterms, e.g. "1-0-"
solutionDict = {}

## Initial dictionary
# make a dictionary that stores the minterm name and the binary representation
# key is the name of the minterm and the value is the binary representation of the minterm
mintermDict = {}
for row in mintermRows.values.tolist():
    mintermDict[row[0]] = row[locationOfFirstVar:numberofVariables+locationOfFirstVar]

originalEquation = binary_rep_to_equation(truthTable, mintermDict)
print("Original Equation: ", originalEquation, "\n")

stopLoop = False
while stopLoop == False:
    # save a copy of the previous mintermDict (will be helpful in extracting solutions)
    prevMintermDict = mintermDict.copy()

    # check each combination of minterms to find which combinations are only different by 1 value
    canCombineSolution = check_differences(mintermDict)
    # print("canCombineSolution: ", canCombineSolution, "\n")

    # # find the minterms that could not be combined
    uncombinedMinterms = find_uncombined_minterms(canCombineSolution)
    for key in uncombinedMinterms:
        solutionDict[key] = prevMintermDict[key]
    # print("uncombinedMinterms: ", uncombinedMinterms, "\n")

    # find reduced implicants (that have a dash instead of a binary value)
    combinedMinterms = find_reduced_minterms(canCombineSolution)
    # print("combinedMinterms: ", combinedMinterms, "\n")

    # if no more minterms can be combined, the algorithm can stop
    if len(combinedMinterms) == 0:
        stopLoop = True

    # re-define the mintermDict
    mintermDict = combinedMinterms.copy()
    # print("MINTERM DICT: ", mintermDict,"\n")

    # print("///////////////////// END OF LOOP //////////////////////////",'\n')

################################# USE PRIME IMPLICANT CHART TO MAKE SHORTENED EQUATION#################################

# make a dictionary to store the primeImplicats
# keys: combinations of minterms, e.g. "m1,m2,m3,m4"
# values: binary representation of minterms, e.g. "1-0-"
primeDict = {}

# Find the terms that output 1 (excluding "don't care" terms). These will be the column headers
oneMinterms = mintermsValOne['Term'].to_list()

# Count how often a minterm is covered by the solution (i.e. number of check marks per column)
countList = count_minterms(oneMinterms,solutionDict)

# When a minterm only shows up once, make sure the implicant that includes it is added to the prime implicant dictionary
# Make a list of minterms that only show up once
uniqueMintermsList = []
for i in range(len(oneMinterms)):
    if countList[i] == 1:
        uniqueMintermsList.append(oneMinterms[i])

# Iterate through the implicants. If one has a minterm that only shows up once, add it to the solution set
for implicant in solutionDict.keys():
    listMinNames = list(implicant.split(","))
    for indvMinName in listMinNames:
        if indvMinName in uniqueMintermsList:
            primeDict[implicant] = solutionDict[implicant]

# Check which minterms were not covered by the unique implicants
# The minterms that are not included yet will have a count of 0
countOfCurrentMinterms = count_minterms(oneMinterms,primeDict)

# Make a list of the minterms that have not been included yet
unincludedMinterms = []
for i in range(len(oneMinterms)):
    if countOfCurrentMinterms[i] == 0:
        unincludedMinterms.append(oneMinterms[i])

# For each minterm that has a count of 0 (has not been included yet), add the first implicant that covers the minterm
for minterm in unincludedMinterms:
    mintermNotIncluded = False
    for implicant in solutionDict:
        listMinNames = list(implicant.split(","))
        for indvMinName in listMinNames:
            if indvMinName == minterm and mintermNotIncluded == False:
                primeDict[implicant] = solutionDict[implicant]
                mintermNotIncluded = True

newEquation = binary_rep_to_equation(truthTable, primeDict)
print("New Equation: ", newEquation, "\n")