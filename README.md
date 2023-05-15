# Cognitive-Robotics-Diagnosis
Diagnosis using implicates and implicants

## Project Description
The focus of this project is to explore the benefits of using implicants and implicates in the diagnosis process. Our motivation is centered around the diagnosis of faults in search-and-rescue (SAR) drones.

## Prerequisties
Make sure you have Python installed on your system. You can download Python [here](https://www.python.org/downloads/).

The project also requires the following Python packages:

* pandas
* itertools
* ttg

You can install these packages using pip:
```bash
pip install pandas
pip install itertools
pip install truth-table-generator
```
## Built With
* Python - The programming language used 
* pandas - Data manipulation and analysis library
* itertools - Functions creating iterators for efficient looping
* ttg - Simplifies the process of creating truth tables by providing a convenient interface to define logical expressions and automatically generate corresponding truth tables. With ttg, you can quickly evaluate logical expressions, validate Boolean functions, and analyze logical relationships.

## Usage
#### truth-table-generator.py:
* This file outputs a truth table in excel format. Users can define their observation variables along with associated mode variables to generate a full truth table. The truth tables for all python scripts have already been included in the repository, not requiring users to run this file.
#### quine_mccluskey.py:
* This file outputs the prime implicants of the truth table generated by "Polycell_Truth_Table.xlsx" The purpose of this file was to create an initial proof of concept to create the prime implicants given a truth table.
#### quine_mccluskey_cnf.py:
* This file outputs the conjunctive normal form (prime implicates as a product of sums) of the truth table generated by "Polycell_Truth_Table.xlsx" The purpose of this file was to create an initial proof of concept to create the conjunctive normal form given a truth table.
#### drone-QM-implementation.py:
* This file outputs the most likely diagnosis given our drone truth table ("Drone_Truth_Table.xlsx") as an input. This algorithm simplifies the drone theory into prime implicants. Users may also adjust the gate probabilities to see how the algorithm outputs a different most likely diagnosis.
#### drone-QM-implementation_cnf.py:
* This file outputs the conjunctive normal form (implicates as a product of sums) of the truth table generated by "Drone_Truth_Table.xlsx". The output of 240 clauses are the implicates for the drone function, but are not simplified to prime implicates. Further research would simplify the output to reduce the number of conflicts to be checked.


## Authors
* Caeley Harihara - charihara
* Steven Hubbard - shubbardjr
