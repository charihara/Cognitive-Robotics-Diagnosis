# import statements
import pandas as pd
import itertools
# numberofOutputs = 2 ### STEVEN I changed this part to accomdate multiple outputs.

# Function that checks which variable assignments are different by 1 value
# Inputs: dictionary with keys that are names of minterms and values that are binary representations of the minterms and the number of variables in each minterm
# Output: list of lists. Each sublist is a pair of minterms that can be combined
def check_differences(mintermDict, numberofVariables):
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
# Input: list of lists where each sublist is a pair of minterms that can be combined and dictionary with minterm name and binary representation
# Output: list of minterms that cannot be combined
def find_uncombined_minterms(canCombineSolution, mintermDict):
    uncombinedMinterms = []
    #list of all the minterms that can be combined
    mintermsInCombinedList = list(itertools.chain(*canCombineSolution))
    for minterm in mintermDict.keys():
        if minterm not in mintermsInCombinedList:
            uncombinedMinterms.append(minterm)
    return uncombinedMinterms

# Function: find reduced implicants (that have a dash instead of a binary value)
# Input: list of lists where each sublist is a pair of minterms that can be combined, the number of variables in each minterm, and dictionary with minterm name and binary representation
# Output: Dictionary that keys: the names of combined minterms  and the values: the binary representation of the combined minterms
def find_reduced_minterms(canCombineSolution, numberofVariables, mintermDict):

    combinedMinterms = {}
    for pair in canCombineSolution:
        minterm1 = mintermDict[pair[0]]
        minterm2 = mintermDict[pair[1]]
        newMinterm = []

        # constructing the new minterm value by value
        for i in range(numberofVariables):
            if minterm1[i] != minterm2[i]:
                newMinterm.append("-")
            else:
                newMinterm.append(minterm1[i])
        newMintermLabel = str(pair[0]) + "," + str(pair[1])

        if newMinterm not in combinedMinterms.values():
            combinedMinterms[newMintermLabel] = newMinterm

    return combinedMinterms

# convert a dictionary containing binarry representations to a formula
# dictionary has keys that are the names of the minterms and values that are the binary representations
# output: string that represents the final equation, e.g. A'B' + ACDE
def binary_rep_to_equation(truthTable, mintermDict):
    print("TRUTH TABLE:")
    print(truthTable,'\n')
    print("MINTERM DICT:", mintermDict,'\n')
    # Make a list with just the variable names
    columnNames = list(truthTable.columns)

    equationString = ""

    numTerms = 0
    for minNames, binRep in mintermDict.items():
        numTerms += 1
        for i in range(len(binRep)):
            # if the value is a 0, the equation has the not of a variable, e.g. B'
            if binRep[i] == 0:
                equationString = equationString + columnNames[i] + "'" + " & "
            # if the value is a 1, the equation has the variable, e.g. B
            elif binRep[i] == 1:
                equationString = equationString + columnNames[i] + " & "
            # if the value is "-", that means the variable is not included in the statement
            else:
                continue

        # add a "+" after each term of the equation, except the last term
        if numTerms != len(mintermDict):
            equationString = equationString[:-3] # Remove the extra & sign
            equationString = equationString + " + "
        else:
            equationString = equationString[:-3]

    return equationString

# Count how often a minterm is included in a dictionary of implicants
# Input 1: Dictionary where the keys are implicant names and the values are binary representations of minterms
# Input 2: list with the minterms we want to count
# Output: list with the count of each minterm (the indexes line up)
def count_minterms(oneMinterms,primeDict):
    countList = [0]*len(oneMinterms)
    for i in range(len(oneMinterms)):
        for allMinNames in primeDict.keys():
            if "," not in str(allMinNames): #if the key just has 1 value (not combined)
                if str(allMinNames) == str(oneMinterms[i]):
                    countList[i] += 1
            else:
                # make a list where each element is the name of a minterm
                listMinNames = list(str(allMinNames).split(","))
                for indvMinName in listMinNames:
                    # if the solution covers that minterm, add to the count
                    if str(indvMinName) == str(oneMinterms[i]):
                        countList[i] += 1

    return(countList)

# Count unincluded minterms (minterms that are not covered by the prime implicants)
# Input 1: Dictionary where the keys are implicant names and the values are binary representations of minterms
# Input 2: Dictionary that has the current prime implicants that will be included in the solution
# Output: list of minterms that are not included by the solution set
def unincluded_minterms(oneMinterms,finalDict):

    # Check which minterms were not covered by the unique implicants
    # The minterms that are not included yet will have a count of 0
    countOfCurrentMinterms = count_minterms(oneMinterms,finalDict)

    # Make a list of the minterms that have not been included yet
    unincludedMinterms = []
    for i in range(len(oneMinterms)):
        if countOfCurrentMinterms[i] == 0:
            unincludedMinterms.append(oneMinterms[i])

    return unincludedMinterms

# Converts an equation's term (e.g. A'BC') to a binary representation
# Input: Term name and names of the variables
# Output: list with the binary variable assignments (e.g. [0, 1, 0, -"])
def convert_term_to_string(termName, variableNames):

    binaryList = []
    termCharacters = [*termName] #turn the term into a list of characters e.g. [A, ', B, C, ']

    for variable in variableNames:
        # When variable is missing it should be a "-" in the binary assignment
        if variable not in termCharacters:
            binaryList.append("-")
        else:
            charSpot = termCharacters.index(variable)
            # if the character is last, that means it can't be a "NOT":
            if charSpot == len(termCharacters) - 1:
                binaryList.append(1)
            else:
                # If variable is a "NOT" e.g. A'
                if termCharacters[charSpot + 1] == "'":
                    binaryList.append(0)
                else:
                    binaryList.append(1)
    return binaryList


############################################# End of Helper Functions #############################################

#### FIND PRIME IMPLICANT Chart ########
## Input: truth table for whole system, relevant input variables, relevant outputVariables
## Output: tuple of (originalEquation, mintermRows, primeDict)
## Where originalEquation is the original theory expression, mintermRows are all the minterms that have an output we want and the primeDict has the minterm expressions and bollean representations
def find_prime_implicants(fileName, inputDict, outputDict):
    numberofOutputs = len(outputDict)
    numberofInputs = len(inputDict)

    mintermRows = pd.read_excel(fileName)
    for (input,value) in inputDict.items():
        mintermRows = mintermRows.loc[(mintermRows[input] == value)]
    for (output,value) in outputDict.items():
        mintermRows = mintermRows.loc[(mintermRows[output] == value)]

    # make a dictionary to store the prime implicants
    # keys: combinations of minterms, e.g. "m1,m2,m3,m4"
    # values: binary representation of minterms, e.g. "1-0-"
    primeDict = {}

    ## Initial dictionary
    # make a dictionary that stores the minterm name and the binary representation
    # key is the name of the minterm and the value is the binary representation of the minterm
    mintermDict = {}
    for row in mintermRows.values.tolist():
        termName = row.pop(0)
        #mintermDict[row[0]] = row[locationOfFirstVar:numberofVariables+locationOfFirstVar]
        mintermDict[termName] = row[numberofInputs:-numberofOutputs]

    #Make a truth table to write the original equation
    numOfColsToKeep = len(mintermRows.columns) - numberofOutputs - numberofInputs
    truthTable = mintermRows.iloc[:,numberofInputs+1:numberofInputs+numOfColsToKeep]
    originalEquation = binary_rep_to_equation(truthTable, mintermDict)

    numberofVariables = len(truthTable.columns)

    stopLoop = False
    while stopLoop == False:
        # save a copy of the previous mintermDict (will be helpful in extracting solutions)
        prevMintermDict = mintermDict.copy()

        # check each combination of minterms to find which combinations are only different by 1 value
        canCombineSolution = check_differences(mintermDict,numberofVariables)

        # # find the minterms that could not be combined
        uncombinedMinterms = find_uncombined_minterms(canCombineSolution, mintermDict)
        for key in uncombinedMinterms:
            primeDict[key] = prevMintermDict[key]

        # find reduced implicants (that have a dash instead of a binary value)
        combinedMinterms = find_reduced_minterms(canCombineSolution, numberofVariables, mintermDict)

        # if no more minterms can be combined, the algorithm can stop
        if len(combinedMinterms) == 0:
            stopLoop = True

        # re-define the mintermDict
        mintermDict = combinedMinterms.copy()

    return(originalEquation, mintermRows, primeDict, truthTable)

##### CAELEY COME BACK TO THIS ########
####### Use Prime Implicant Chart to Make Shortened Equation ########
## Input: File name that has the theory
## Output: (Original theory expression, new theory expression)
def find_min_expression(fileName,inputDict,outputDict):

    ## Get information from prime implicant chart
    (originalEquation, mintermRows, primeDict, truthTable) = find_prime_implicants(fileName,inputDict,outputDict)
    numberofOutputs = len(outputDict)
    numberofVariables = len(mintermRows.columns) - numberofOutputs - 1     ### STEVEN I changed this part to accomdate multiple outputs.

    # make a dictionary to store the final implicants that will be used to represent the theory
    # keys: combinations of minterms, e.g. "m1,m2,m3,m4"
    # values: binary representation of minterms, e.g. "1-0-"
    finalDict = {}

    # Find the terms that output 1 (excluding "don't care" terms). These will be the column headers
    oneMinterms = mintermRows['Term'].to_list()
    print("oneMinterms:")
    print(oneMinterms)
    # Count how often a minterm is covered by the solution (i.e. number of check marks per column)
    print("BEFORE primeDict: ", primeDict)
    countList = count_minterms(oneMinterms,primeDict)
    print("CountList:", countList)

    # When a minterm only shows up once, make sure the implicant that includes it is added to the prime implicant dictionary
    # Make a list of minterms that only show up once
    uniqueMintermsList = []
    for i in range(len(oneMinterms)):
        if countList[i] == 1:
            uniqueMintermsList.append(str(oneMinterms[i]))

    # Iterate through the implicants. If one has a minterm that only shows up once, add it to the solution set
    for implicant in primeDict.keys():
        listMinNames = list(str(implicant).split(","))
        for indvMinName in listMinNames:
            if indvMinName in uniqueMintermsList:
                finalDict[implicant] = primeDict[implicant]

    # Check which minterms were not covered by the unique implicants
    unincludedMinterms = unincluded_minterms(oneMinterms,finalDict)
    print(unincludedMinterms)
    ## While there are minterms that have not yet been included, add more implicants to the prime implicant list until they're all covered
    # i = 0
    # while i < 3:
    while len(unincludedMinterms) > 0:
        print("Looping")
        # Count dictionary will have keys be the implicants and values be the count of missing minterms covered
        countDict = primeDict.copy()
        for implicant in primeDict:
            countDict[implicant] = 0

        # Count how many missing minterms each implicant will cover
        for implicant in primeDict:
            listMinNames = list(str(implicant).split(","))
            for term in listMinNames:
                for minterm in unincludedMinterms:
                    if term == minterm:
                        countDict[implicant] += 1

        # Add the implicant that covers the most missing minterms
        implicantToAdd = max(countDict, key = countDict.get)
        finalDict[implicantToAdd] = primeDict[implicantToAdd]

        # Re-evaluate which minterms are missing
        unincludedMinterms = unincluded_minterms(oneMinterms,finalDict)

        # i+=1

    ## Write an equation that represents the solution
    newEquation = binary_rep_to_equation(truthTable, finalDict)

    return(originalEquation, newEquation)

#Given a list of prime implicants and the probability of each piece failing, find the most likely diagnosis
def diagnose(newEquation, probDict):
    # Key: the implicant term
    # Value: the probability that the implicant is causing the problem
    implicantDict = {}

    terms = list(str(newEquation).split(" + "))

    for term in terms:
        implicantDict[term] = 1
        individualVars = list(str(term).split(" & "))
        for variable in individualVars:
            implicantDict[term] = implicantDict[term] * probDict[variable]

    for (implicant,probability) in implicantDict.items():
        implicantDict[implicant] = [probability]

    implicantDF = pd.DataFrame.from_dict(implicantDict)

    mostLikelyDiagnosis = implicantDF.idxmax(axis=1).values.flatten().tolist()[0]

    return (implicantDF, mostLikelyDiagnosis)


############### MAIN ##########################
inputDict = {'E': 1,'R': 1,'C': 1,'F': 0}
outputDict = {'I':0}
gateProbabilities = {"BB": 0.90, "BB'": 0.1,"MB": 0.95, "MB'": 0.05,"WC": 0.99, "WC'": 0.01,"FC": 0.98, "FC'": 0.02,"TIC": 0.80, "TIC'": 0.2}

(originalEquation, newEquation) = find_min_expression('Drone_Truth_Table.xlsx', inputDict,outputDict)
print("Original Equation: ", originalEquation,'\n')
print("New Equation:      ", newEquation, '\n')

(implicantDF, mostLikelyDiagnosis) = diagnose(newEquation, gateProbabilities)
print("Probabilites of each implicant: ")
print(implicantDF,'\n')
print("MOST LIKELY DIAGNOSIS: ", mostLikelyDiagnosis,'\n')
