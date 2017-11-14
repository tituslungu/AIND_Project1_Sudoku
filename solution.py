def cross(A, B):
	return [a+b for a in A for b in B] #cross product, returns all possible combinations of elements in A and B

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# diag_units1 = [rows[i]+cols[i] for i in range(len(rows))] # find all boxes on first diagonal
# diag_units2 = [rows[i]+cols[len(rows)-i-1] for i in range(len(rows))] # find all boxes on second diagonal
# unitlist = row_units + column_units + square_units + [diag_units1] + [diag_units2]

diag_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# unitlist = row_units + column_units + square_units + [diag_units1] + [diag_units2] # update unitlist to include diagonal elements

# check if a box is part of a diagonal, and if so, add all elements on that diagonal (except for itself and any elements already in peer list) to it's set of peers
# middle box will get all diagonal units (from both diagonals) added as peers
# for peer in peers:
# 	if peer in diag_units1:
# 		for unit in diag_units1:
# 			if unit != peer:
# 				peers[peer].add(unit)
# 	if peer in diag_units2:
# 		for unit in diag_units2:
# 			if unit != peer:
# 				peers[peer].add(unit)

def assign_value(values, box, value):
	"""
	Please use this function to update your values dictionary!
	Assigns a value to a given box. If it updates the board record it.
	"""

	# Don't waste memory appending actions that don't actually change any values
	if values[box] == value:
		return values

	values[box] = value
	if len(value) == 1:
		assignments.append(values.copy())
	return values

def naked_twins(values):
	"""Eliminate values using the naked twins strategy.
	Args:
		values(dict): a dictionary of the form {'box_name': '123456789', ...}

	Returns:
		the values dictionary with the naked twins eliminated from peers.
	"""

	# Find all instances of naked twins
	# Eliminate the naked twins as possibilities for their peers
	for unit in unitlist:
		for box in unit:
			for box2 in unit:
				if box != box2 and values[box] == values[box2] and len(values[box]) == 2 and len(values[box2]) == 2:
					for other in unit:
						if other != box and other != box2:
							for box_val in values[box]:
								values = assign_value(values, other, values[other].replace(box_val,''))

	return values

def grid_values(grid):
	"""
	Convert grid into a dict of {square: char} with '123456789' for empties.
	Args:
		grid(string) - A grid in string form.
	Returns:
		A grid in dictionary form
			Keys: The boxes, e.g., 'A1'
			Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
	"""
	new_grid = []
	for box in grid:
		if box is '.':
			new_grid.append('123456789') # if box is empty, assign all possible values
		else:
			new_grid.append(box) # otherwise, keep the value(s) in that box

	return dict(zip(boxes, new_grid))

def display(values):
	"""
	Display the values as a 2-D grid.
	Args:
		values(dict): The sudoku in dictionary form
	"""
	width = 1+max(len(values[s]) for s in boxes)
	line = '+'.join(['-'*(width*3)]*3)
	for r in rows:
		print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
					  for c in cols))
		if r in 'CF': print(line)
	return


def eliminate(values):
	"""
	For each solved box, eliminate assignmenet value from all of it's peers
	Args:
		values(dict): Sudoku in dict form
	Returns:
		Updated values(dict) ie Sudoku
	"""
	solved = [box for box in values if len(values[box]) is 1]
	
	for box in solved:
		num = values[box]
		for peer in peers[box]:
			values = assign_value(values, peer, values[peer].replace(num,''))

	return values

def only_choice(values):
	"""
	For each list of units, if a value appears in only one box as a possible assignment, then assign that value to that box
	Args:
		Sudoku as dictionary called values
	Return:
		Updated Sudoku
	"""
	for unit in unitlist:
		for num in cols:
			where = [box for box in unit if num in values[box]]
			if len(where) == 1:
				values = assign_value(values, where[0], num)
	return values

def reduce_puzzle(values):
	"""
	Alternate between elimination and only choice methods until sudoku is solved, an unsolvable state is reached, or a box becomes empty
	Args:
		Sudoku as dictionary called values
	Return:
		Updated Sudoku
	"""
	stalled = False
	while not stalled:
		# Check how many boxes have a determined value
		solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
		# apply eliminate
		values = eliminate(values)
		# apply only choice
		values = only_choice(values)
		# apply naked twins
		# values = naked_twins(values)
		# Check how many boxes have a determined value, to compare
		solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
		# If no new values were added, stop the loop.
		stalled = solved_values_before == solved_values_after
		# check if a box has become empty, indicating failure of puzzle
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False
	return values

def search(values):
	"""
	Try to reduce the puzzle first. If an answer is not found but it also doesn't fail, try choosing an available values for remaining boxes
	to be solved (with least options) and recursively run function until board is solved.
	Args:
		Sudoku as dictionary called values
	Return:
		Updated Sudoku
	"""
	# reduce puzzle as much as possible
	values = reduce_puzzle(values)
	if values is False:
		return False
	if all(len(values[s])==1 for s in boxes):
		return values
	# Choose one of the unfilled squares with the fewest possibilities
	n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
	# Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
	for value in values[s]:
		new_sudoku = values.copy()
		new_sudoku[s] = value
		attempt = search(new_sudoku)
		if attempt:
			return attempt

def solve(grid):
	"""
	Find the solution to a Sudoku grid.
	Args:
		grid(string): a string representing a sudoku grid.
			Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	Returns:
		The dictionary representation of the final sudoku grid. False if no solution exists.
	"""
	values = grid_values(grid)
	values = search(values)

	return values

if __name__ == '__main__':
	diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'#'2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	display(solve(diag_sudoku_grid))

	try:
		from visualize import visualize_assignments
		visualize_assignments(assignments)

	except SystemExit:
		pass
	except:
		print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
