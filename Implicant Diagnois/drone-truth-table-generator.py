import ttg

# Writes an equation that describes the functionality of an AND gate
def and_function(input1, input2, andGate):
    term1 = f"{input1} and {input2} and {andGate}"
    # When will the expression be 1?
    expression = f"{term1}"
    return expression

def and_function_one_input(input1, andGate):
    term1 = f"{input1} and {andGate}"
    expression = f"{term1}"
    # When will the expression be 1?
    return expression

# Writes an equation that describes the functionality of an XOR gate
def xor_function_no_gate(input1, input2):
    term1 = f"({input1} and (~{input2}))"
    term2 = f"((~{input1}) and {input2})"
    expression = f"{term1} or {term2}"
    # When will the expression be 1?
    return expression

# Writes an equation that describes the functionality of an OR gate
def or_function(input1, input2, orGate):
    term1 = f"((~{input1}) and (~{input2}) and (~{orGate}))"
    term2 = f"({input1} and {orGate})"
    term3 = f"({input2} and {orGate})"
    expression = f"{term1} or {term2} or {term3}"
    # When will the expression be 1?
    return expression

### Add logic describing the system below
U = and_function("E", "R", "BB")
V = and_function_one_input("R", "MB")
W = and_function("R", "C", "WH")
X = and_function_one_input("F","FH")

Y = f"({U}) or ({V})"
Z = xor_function_no_gate(f"({W})",f"({X})")
I = and_function(f"({Y})", f"({Z})", "TIC")

### Create the truth table
table = ttg.Truths(["E","R","C","F","BB","MB","WH","FH","TIC"],[I])
tableDF = table.as_pandas()
tableDF.rename(columns = {I:'I'}, inplace = True)
tableDF.to_excel("Drone_Truth_Table.xlsx")
