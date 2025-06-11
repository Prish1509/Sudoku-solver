# Sudoku Solver using PycoSAT

## Team Members:
- Ankit Gupta   - 112301010
- Italiya Prisha  - 142301011

## Overview

This Python script solves Sudoku puzzles using the PycoSAT SAT solver. It reads Sudoku puzzles from an input file, converts them into SAT clauses, solves them using a SAT solver, and writes the solutions to an output file.

## Dependencies

### Required Packages

Ensure you have Python 3 installed along with the following dependency:

- `pycosat` (Install using `pip install pycosat`)

## How It Works

### 1. Clause Generation

The script generates constraints to represent Sudoku rules in the form of SAT clauses:

- **Uniqueness Constraint**: Each cell contains exactly one number (1-9)  (Each cell in puzzle contains at least one value and each cell in the puzzle contains at most one value.)
    
- **Row Constraint**: Each number appears exactly once in each row.
    
- **Column Constraint**: Each number appears exactly once in each column.
    
- **3x3 Sub-grid Constraint**: Each number appears exactly once in each 3x3 sub-grid and all the numbers from 1-9 are included.

Code:
```
for x in range(1,10): 
    for y in range(1,10):  
        clauses.append([value(x,y,k) for k in range(1,10)])
        for z in range(1,9):
            for i in range(z+1,10):
                clauses.append([-value(x,y,z),-value(x,y,i)])

for y in range(1,10):
    for z in range(1,10):
        for x in range(1,9):
            for i in range(x+1,10):
                clauses.append([-value(x,y,z),-value(i,y,z)])

for x in range(1,10):
    for z in range(1,10):
        for y in range(1,9):
            for i in range(y+1,10):
                clauses.append([-value(x,y,z),-value(x,i,z)])

for z in range(1,10):
    for i in range(0,3):
        for j in range(0,3):
            for x in range(1,4):
                for y in range(1,4):
                    for k in range(y+1,4):
                        clauses.append([-value(3*i+x,3*j+y,z), -value(3*i+x,3*j+k,z)])
                    for k in range(x+1,4):
                        for l in range(1,4):
                            clauses.append([-value(3*i+x,3*j+y,z), -value(3*i+k,3*j+l,z)])

```

### 2. Encoding Given Sudoku

Each Sudoku puzzle from the input file is converted into a set of logical clauses, incorporating given numbers and constraints along with the predefined clauses present initially.

```
for idx, x in enumerate(sample):
	if x != 0:
	i = idx // 9 +1 # Row index
	j = idx % 9 +1 # Column index
	clauses.append([value(i, j, x)])
```
### 3. Solving with PycoSAT

The clauses are passed to PycoSAT, which attempts to find a valid assignment of numbers satisfying all constraints.

### 4. Decoding the Solution

The returned solution is converted from SAT representation back into a readable Sudoku grid format.

```
def decode_solution(solution):
	sudoku_grid = [[0 for _ in range(9)] for _ in range(9)]
	for val in solution:
		if val > 0: # Only consider positive values
		val -= 1 # Convert to 0-based indexing
		row = val // 81
		col = (val % 81) // 9
		num = (val % 9) + 1 # Convert back to 1-9 numbering
		
		if 0 <= row < 9 and 0 <= col < 9: # Bounds check
			sudoku_grid[row][col] = num
		else:
			print(f"Error: Invalid index ({row}, {col}) from value {val + 1}")
			return sudoku_grid
```

### 5. Output

The solved Sudokus are written into `solved_sudokus.txt`.

## File Structure

- `p.txt`: Input file containing Sudoku puzzles in a single-line format.
    
- `solved_sudokus.txt`: Output file containing solved puzzles.
    
- `solve.py`: The main script implementing the solver.
    

## Usage Instructions

### 1. Prepare the Input File

Create a text file `p.txt` containing Sudoku puzzles in a single-line format. Each line must be exactly 81 characters long.

- Digits `1-9` represent given numbers.
    
- `.` or `0` represents an empty cell.
    

Example input file (`p.txt`):

```
530070000600195000098000060800060003400803001700020006060000280000419005000080079
200000000000000000000000000000000000000000000000000000000000000000000000000000000
```

### 2. Run the Script

Execute the script with Python:

```sh
python3 solve.py
```

### 3. Check the Output

The solutions will be saved in `solved_sudokus.txt`. Each solved Sudoku is stored in a single-line format, corresponding to the input format.

Example output (`solved_sudokus.txt`):

```
534678912672195348198342567859761423426853791713924856961537284287419635345286179
No solution found!(If the solution does not exist)
```

## Error Handling

- If a Sudoku is unsolvable, the script will output `No solution found!` in `solved_sudokus.txt`.
    
- Ensure `p.txt` contains valid Sudoku grids (exactly 81 characters per puzzle).
    
- The script will print an error message if an invalid input format is detected.
    
---
