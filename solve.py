import pycosat

# function to assign a cell (i,j) with a digit d into a single SAT variable
def value(i,j,d):
    return (81 * (i-1) + 9 * (j-1) + d)   

clauses = []  # list to hold all CNF clauses

# function to generate the base constraints of Sudoku in CNF
def gen_clauses():
    # Rule 1: each cell must have exactly one number (1–9)
    for x in range(1,10): 
        for y in range(1,10):  
            # At least one number per cell
            clauses.append([value(x,y,k) for k in range(1,10)])
            # At most one number per cell (no two values at the same cell)
            for z in range(1,9):
                for i in range(z+1,10):
                    clauses.append([-value(x,y,z),-value(x,y,i)])
                    
    # Rule 2: each number appears at most once in each row
    for y in range(1,10):
        for z in range(1,10):
            for x in range(1,9):
                for i in range(x+1,10):
                    clauses.append([-value(x,y,z),-value(i,y,z)])
    
    # Rule 3: each number appears at most once in each column
    for x in range(1,10):
        for z in range(1,10):
            for y in range(1,9):
                for i in range(y+1,10):
                    clauses.append([-value(x,y,z),-value(x,i,z)])

    # Rule 4: each number appears at most once in each 3x3 sub-grid
    for z in range(1,10):
        for i in range(0,3):
            for j in range(0,3):
                for x in range(1,4):
                    for y in range(1,4):
                        # horizontal pairwise constraint inside sub-grid
                        for k in range(y+1,4):
                            clauses.append([-value(3*i+x,3*j+y,z), -value(3*i+x,3*j+k,z)])
                        # vertical pairwise constraint inside sub-grid
                        for k in range(x+1,4):
                            for l in range(1,4):
                                clauses.append([-value(3*i+x,3*j+y,z), -value(3*i+k,3*j+l,z)])

# add initial values from a Sudoku puzzle into the clause set
def clauseria(sample):
    for idx, x in enumerate(sample):
        if x != 0:  
            i = idx // 9 +1  # row index (1-based)
            j = idx % 9  +1  # column index (1-based)
            clauses.append([value(i, j, x)])  # add known value constraint

# decode SAT solver output into a 9x9 Sudoku grid
def decode_solution(solution):
    sudoku_grid = [[0 for _ in range(9)] for _ in range(9)]
    for val in solution:
        if val > 0:  # consider only variables that are true
            val -= 1  # adjust to 0-based index
            row = val // 81
            col = (val % 81) // 9
            num = (val % 9) + 1  # convert index back to number 1–9

            if 0 <= row < 9 and 0 <= col < 9:  # bounds check
                sudoku_grid[row][col] = num
            else:
                print(f"Error: Invalid index ({row}, {col}) from value {val + 1}")

    return sudoku_grid

# convert Sudoku grid into a string format ('.' for empty)
def print_sudoku(grid):
    return "".join(str(cell) if cell != 0 else "." for row in grid for cell in row)

# parse Sudoku puzzles from input file
def parseFile(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    sudokus = []  # contains all the parsed sudokus'
    current_sudoku = []  # stores the current sudoku
 
    for line in lines:
        # convert line characters to integers (0 for blanks)
        current_sudoku.extend([int(c) if c.isdigit() else 0 for c in line])
        
        if len(current_sudoku) == 81:  #complete Sudoku grid
            sudokus.append(current_sudoku)
            current_sudoku = []  # reset for next Sudoku
    
    return sudokus

file_path = "p.txt"  # file path
output_file = "solved_sudokus.txt"  # output file 
sudoku_puzzles = parseFile(file_path)  # read Sudoku puzzles

# solve each puzzle and write solutions to output file
with open(output_file, "w") as f:
    for idx, puzzle in enumerate(sudoku_puzzles):
        gen_clauses()  # generate base rules
        clauseria(puzzle)  # add clauses from current puzzle
        solution = pycosat.solve(clauses)  # solve using SAT solver

        if solution == "UNSAT":  #if no sol is found
            f.write("No solution found!\n")
        else:
            sudoku_solution = decode_solution(solution)  # decode SAT solution
            formatted_output = print_sudoku(sudoku_solution)  # format output
            f.write(formatted_output + "\n")  # write to file
        clauses.clear()  # clear clause list for next puzzle

print(f"All solutions written to {output_file}")
