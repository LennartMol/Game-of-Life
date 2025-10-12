
# empty 2d array
rows, cols = (5, 5)
arr = [[0 for i in range(cols)] for j in range(rows)]

# array with 3 vertical cells filled
arr_vert = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

# array for testing count_neighbours
arr_test_count = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

# array for testing count_neighbours
arr_test_count_2 = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]


for row in arr_test_count_2:
    print(row)

selected_cell = [2,2]

# rules
# Any live cell with fewer than two live neighbours dies, as if by underpopulation.

def count_neighbours(arr, target_cell):
    targetRow = target_cell[0]
    targetCol = target_cell[1]
    total_neighbours = 0

    for col in range(-1, 2,):
        selectedCol = targetCol + col

        for row in range(-1, 2):
            selectedRow = targetRow + row
            # prevent counting the cell itself
            if not (selectedCol == targetRow and selectedRow == targetCol):
                total_neighbours += arr[selectedRow][selectedCol]

    return total_neighbours


print(count_neighbours(arr_test_count_2, selected_cell))