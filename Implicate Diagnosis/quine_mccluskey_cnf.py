# import statements
import pandas as pd
import itertools

# Function that checks which variable assignments are different by 1 value
# Inputs: dictionary with keys that are names of maxterms and values that are binary representations of the maxterms
# Output: list of lists. Each sublist is a pair of maxterms that can be combined
def check_differences(maxtermDict):
    canCombineSolution = []
    for maxterm1 in maxtermDict.keys():
        for maxterm2 in maxtermDict.keys():
            if maxterm1 != maxterm2:
                # compare the binary representations for 2 maxterms and count how many values they share
                numMatchingVals = 0
                for i in range(numberofVariables):
                    if maxtermDict[maxterm1][i] == maxtermDict[maxterm2][i]:
                        numMatchingVals += 1
                # if maxterms only vary by 1 value, they can be combined
                if numMatchingVals == numberofVariables - 1:
                    # only add pair that is not already in the list of matches
                    if [maxterm1,maxterm2] not in canCombineSolution and [maxterm2,maxterm1] not in canCombineSolution:
                        canCombineSolution.append([maxterm1,maxterm2])
    return canCombineSolution

# Function that finds the maxterms that cannot be combined
# Input: list of lists where each sublist is a pair of maxterms that can be combined
# Output: list of maxterms that cannot be combined
def find_uncombined_maxterms(canCombineSolution):
    uncombinedmaxterms = []
    #list of all the maxterms that can be combined
    maxtermsInCombinedList = list(itertools.chain(*canCombineSolution))
    # print("maxTERMS IN COMBINED LIST: ", maxtermsInCombinedList)
    for maxterm in maxtermDict.keys():
        if maxterm not in maxtermsInCombinedList:
            uncombinedmaxterms.append(maxterm)
    return uncombinedmaxterms

# Function: find reduced implicants (that have a dash instead of a binary value)
# Input: list of lists where each sublist is a pair of maxterms that can be combined
# Output: Dictionary that keys: the names of combined maxterms  and the values: the binary representation of the combined maxterms
def find_reduced_maxterms(canCombineSolution):
    combinedmaxterms = {}
    for pair in canCombineSolution:
        maxterm1 = maxtermDict[pair[0]]
        maxterm2 = maxtermDict[pair[1]]
        newmaxterm = []
        # print("maxTERM 1: ", maxterm1)
        # print("maxTERM 2: ", maxterm2)
        # print("========================")
        # constructing the new maxterm value by value
        for i in range(numberofVariables):
            if maxterm1[i] != maxterm2[i]:
                newmaxterm.append("-")
            else:
                newmaxterm.append(maxterm1[i])
        newmaxtermLabel = pair[0] + "," + pair[1]
        #print(newmaxtermLabel)
        if newmaxterm not in combinedmaxterms.values():
            combinedmaxterms[newmaxtermLabel] = newmaxterm

    return combinedmaxterms

# convert a dictionary containing binarry representations to a formula
# dictionary has keys that are the names of the maxterms and values that are the binary representations
# output: string that represents the final equation, e.g. A'B' + ACDE
def binary_rep_to_equation(truthTable, maxtermDict):
    columnNames = list(truthTable.columns)
    columnNames.pop(0)
    columnNames.pop()

    equationString = ""

    numTerms = 0
    for maxNames, binRep in maxtermDict.items():
        numTerms += 1
        equationString += "("
        for i in range(len(binRep)):
            if binRep[i] == 0:
                equationString = equationString + columnNames[i] + " + "
            elif binRep[i] == 1:
                equationString = equationString + columnNames[i] + "'" + " + "
            else:
                continue
        # Remove the trailing ' + ' from the term
        equationString = equationString.rstrip(' + ')
        equationString += ")"
        if numTerms != len(maxtermDict):
            equationString = equationString + " * "

    return equationString

# Count how often a maxterm is included in a dictionary of implicants
# Input: Dictionary where the keys are implicant names and the values are binary representations of maxterms
# Input: list with the maxterms we want to count
# Output: list with the count of each maxterm (the indexes line up)
def count_maxterms(onemaxterms,solutionDict):
    countList = [0]*len(onemaxterms)
    for i in range(len(onemaxterms)):
        for allmaxNames in solutionDict.keys():
            # make a list where each element is the name of a maxterm
            listmaxNames = list(allmaxNames.split(","))
            for indvmaxName in listmaxNames:
                # if the solution covers that maxterm, add to the count
                if indvmaxName == onemaxterms[i]:
                    countList[i] += 1

    return(countList)
    Test_Problem_Input
################################# FIND PRIME IMPLICANTS #################################

## Initial Data Processing
# read by in the truth table/model for the system:
truthTable = pd.read_excel('Test_Problem_Input.xlsx')
# number of variables is number of columns - 2 (to remove the "terms" column and "f" column)
numberofVariables = len(truthTable.columns) - 2
locationOfFirstVar = 1

# find the maxterms that have a truthTable value of 1 or indifferent (x)
maxtermsValOne = (truthTable.loc[truthTable['f'] == 0])
maxtermsValX = (truthTable.loc[truthTable['f'] == "x"])
maxtermRows = pd.concat([maxtermsValOne,maxtermsValX])

# make a dictionary to store the solutions
# keys: combinations of maxterms, e.g. "m1,m2,m3,m4"
# values: binary representation of maxterms, e.g. "1-0-"
solutionDict = {}

## Initial dictionary
# make a dictionary that stores the maxterm name and the binary representation
# key is the name of the maxterm and the value is the binary representation of the maxterm
maxtermDict = {}
for row in maxtermRows.values.tolist():
    maxtermDict[row[0]] = row[locationOfFirstVar:numberofVariables+locationOfFirstVar]

originalEquation = binary_rep_to_equation(truthTable, maxtermDict)
print("Original Equation: ", originalEquation, "\n")

stopLoop = False
while stopLoop == False:
    # save a copy of the previous maxtermDict (will be helpful in extracting solutions)
    prevmaxtermDict = maxtermDict.copy()

    # check each combination of maxterms to find which combinations are only different by 1 value
    canCombineSolution = check_differences(maxtermDict)
    # print("canCombineSolution: ", canCombineSolution, "\n")

    # # find the maxterms that could not be combined
    uncombinedmaxterms = find_uncombined_maxterms(canCombineSolution)
    for key in uncombinedmaxterms:
        solutionDict[key] = prevmaxtermDict[key]
    # print("uncombinedmaxterms: ", uncombinedmaxterms, "\n")

    # find reduced implicants (that have a dash instead of a binary value)
    combinedmaxterms = find_reduced_maxterms(canCombineSolution)
    # print("combinedmaxterms: ", combinedmaxterms, "\n")

    # if no more maxterms can be combined, the algorithm can stop
    if len(combinedmaxterms) == 0:
        stopLoop = True

    # re-define the maxtermDict
    maxtermDict = combinedmaxterms.copy()
    # print("maxTERM DICT: ", maxtermDict,"\n")

    # print("///////////////////// END OF LOOP //////////////////////////",'\n')

################################# USE PRIME IMPLICANT CHART TO MAKE SHORTENED EQUATION#################################

# make a dictionary to store the primeImplicats
# keys: combinations of maxterms, e.g. "m1,m2,m3,m4"
# values: binary representation of maxterms, e.g. "1-0-"
primeDict = {}

# Find the terms that output 1 (excluding "don't care" terms). These will be the column headers
onemaxterms = maxtermsValOne['Term'].to_list()

# Count how often a maxterm is covered by the solution (i.e. number of check marks per column)
countList = count_maxterms(onemaxterms,solutionDict)

# When a maxterm only shows up once, make sure the implicant that includes it is added to the prime implicant dictionary
# Make a list of maxterms that only show up once
uniquemaxtermsList = []
for i in range(len(onemaxterms)):
    if countList[i] == 1:
        uniquemaxtermsList.append(onemaxterms[i])

# Iterate through the implicants. If one has a maxterm that only shows up once, add it to the solution set
for implicant in solutionDict.keys():
    listmaxNames = list(implicant.split(","))
    for indvmaxName in listmaxNames:
        if indvmaxName in uniquemaxtermsList:
            primeDict[implicant] = solutionDict[implicant]

# Check which maxterms were not covered by the unique implicants
# The maxterms that are not included yet will have a count of 0
countOfCurrentmaxterms = count_maxterms(onemaxterms,primeDict)

# Make a list of the maxterms that have not been included yet
unincludedmaxterms = []
for i in range(len(onemaxterms)):
    if countOfCurrentmaxterms[i] == 0:
        unincludedmaxterms.append(onemaxterms[i])

# For each maxterm that has a count of 0 (has not been included yet), add the first implicant that covers the maxterm
for maxterm in unincludedmaxterms:
    maxtermNotIncluded = False
    for implicant in solutionDict:
        listmaxNames = list(implicant.split(","))
        for indvmaxName in listmaxNames:
            if indvmaxName == maxterm and maxtermNotIncluded == False:
                primeDict[implicant] = solutionDict[implicant]
                maxtermNotIncluded = True

newEquation = binary_rep_to_equation(truthTable, primeDict)
print("New Equation: ", newEquation, "\n")