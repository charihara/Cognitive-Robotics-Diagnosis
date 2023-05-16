import ttg

# Writes an equation that describes the functionality of an and gate
def and_function(input1, input2, andGate):
    term1 = f"({input1} and {input2} and {andGate})"
    term2 = f"((~{input1}) and (~{andGate}))"
    term3 = f"((~{input2}) and (~{andGate}))"
    expression = f"{term1} or {term2} or {term3}"
    # When will the expression be 1?
    return expression

# Writes an equation that describes the functionality of an xor gate
def xor_function(input1, input2, xorGate):
    term1 = f"({input1} and {input2} and (~{xorGate}))"
    term2 = f"((~{input1}) and (~{input2}) and (~{xorGate}))"
    term3 = f"({input1} and (~{input2}) and {xorGate})"
    term4 = f"((~{input1}) and {input2} and {xorGate})"
    expression = f"{term1} or {term2} or {term3} or {term4}"
    # When will the expression be 1?
    return expression

x = and_function("a", "c", "A1")
y = and_function("b", "d", "A2")
z = and_function("c", "e", "A3")

f = xor_function(f"({x})", f"({y})", "X1")
g = xor_function(f"({y})", f"({z})", "X2")

table = ttg.Truths(['a','b','c','d','e','A1','A2','A3','X1','X2'], [f,g])
#table = ttg.Truths(['a','b','c','d','e','A1','A2','A3','X1','X2'], [x,y,z,f,g]) # shows intermediate varaibles

tableDF = table.as_pandas()
tableDF.to_excel("Polycell_Truth_Table.xlsx")
