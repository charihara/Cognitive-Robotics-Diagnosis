import pandas as pd

def generate_cnf(filename):
    # Read excel file
    df = pd.read_excel(filename)

    # Initialize an empty clause list
    clauses = []

    # Iterate over rows
    for index, row in df.iterrows():
        clause = []
        for var in df.columns[1:-1]:  # skip "Term" and Function Output "I"
            if row[var] == 0:
                clause.append(var) #if 0, keep variable as is, otherwise must be negated
            else:
                clause.append('~' + var)
        # Add clause to cnf if output is 0 to check for maxterms
        if row['I'] == 0:
            clauses.append(' OR '.join(clause))
    # Join clauses with AND and number them
    cnf_string = '\n'.join(f'{i+1}. (' + clause + ') *' for i, clause in enumerate(clauses))
    return cnf_string

input_file='Drone_Truth_Table.xlsx'
print(generate_cnf(input_file))