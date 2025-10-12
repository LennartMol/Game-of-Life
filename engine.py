import test_arrays


selected_cell = [2,2]
selected_array = test_arrays.arr_test_count_4

for row in selected_array:
    print(row)


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


def decide_fate_cell(arr, target_cell, number_of_neighbours):
    targetRow = target_cell[0]
    targetCol = target_cell[1]


    # question? do you exist
    if (arr[targetRow][targetCol]):
        # yes

        # rule 1: thou shall cease if they neighbours are fewer than 2
        if (number_of_neighbours < 2):
            arr[targetRow][targetCol] = 0
        # rule 2: thou shall live this generation if they neighbours are 2 or 3
        if (number_of_neighbours >= 2 and number_of_neighbours <= 3 ):
            return
        # rule 3: thou shall case if they neighbours are greater than 3
        if (number_of_neighbours > 3): 
            arr[targetRow][targetCol] = 0
    
    else:
        # no

        # do you want to live?
        # rule 4: thou shall be give the essence of the almighty '1' if they neighbours are EXACTLY 3
        if (number_of_neighbours == 3):
            arr[targetRow][targetCol] = 1

number_of_neighbours = count_neighbours(selected_array, selected_cell)
print(number_of_neighbours)

decide_fate_cell(selected_array, selected_cell, number_of_neighbours)

for row in selected_array:
    print(row)
