def find_cells_on_level(matrix, lvl):
    rows = len(matrix)
    cols = len(matrix[0])

    if lvl < 0 or lvl >= min(rows, cols):
        raise ValueError("Invalid level")

    level_cells = []

    for row in range(rows):
        for col in range(cols):
            if col == lvl:
                level_cells.append((row, col))       # left
                level_cells.append((row, -(col+1)))  # right

    return level_cells



def set_cells_to_value(matrix, lvl, value):
    replaced_cells = {}
    level_cells = find_cells_on_level(matrix, lvl)
    for row, col in level_cells:
        if replaced_cells.get(matrix[row][col]):
            replaced_cells[matrix[row][col]] += 1
        else:
            replaced_cells[matrix[row][col]] = 1;  
        
        matrix[row][col] = value
    return (matrix, replaced_cells)
