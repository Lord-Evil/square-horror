def find_cells_on_level(matrix, lvl):
    rows = len(matrix)
    cols = len(matrix[0])

    if lvl < 0 or lvl >= min(rows, cols):
        raise ValueError("Invalid level")

    level_cells = []

    # Верхняя горизонталь
    for col in range(lvl, cols - lvl):
        level_cells.append((lvl, col))

    # Правая вертикаль
    for row in range(lvl + 1, rows - lvl):
        level_cells.append((row, cols - lvl - 1))

    # Нижняя горизонталь
    if lvl * 2 < rows:
        for col in range(cols - lvl - 2, lvl - 1, -1):
            level_cells.append((rows - lvl - 1, col))

    # Левая вертикаль
    if lvl * 2 < cols:
        for row in range(rows - lvl - 2, lvl, -1):
            level_cells.append((row, lvl))

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
