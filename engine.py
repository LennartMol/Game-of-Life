import test_arrays
import time

class Engine():

    def __init__(self, array, debug=True,):
        
        # Array size
        self.number_of_rows = len(array)
        self.number_of_columns = len(array)
        
        # Arrays
        self.original_array = array
        self.old_array = array
        self.new_array = [[0 for i in range(self.number_of_columns)] for j in range(self.number_of_rows)]

        # simulation speed
        self.generations_per_second = 0

        # Debug flag
        self.debug = debug
        
    def count_neighbours(self, arr, target_cell):
        targetRow = target_cell[0]
        targetCol = target_cell[1]
        total_neighbours = 0

        for col in range(-1, 2,):
            selectedCol = targetCol + col

            for row in range(-1, 2):
                selectedRow = targetRow + row
                # prevent counting the cell itself
                if not (selectedCol == targetCol and selectedRow == targetRow):
                    total_neighbours += arr[selectedRow][selectedCol]

        return total_neighbours
    


    def decide_fate_cell(self, newArr, oldArr, target_cell, number_of_neighbours):
        targetRow = target_cell[0]
        targetCol = target_cell[1]


        # question? do you exist
        if (oldArr[targetRow][targetCol]):
            # yes

            # rule 1: thou shall cease if they neighbours are fewer than 2
            if (number_of_neighbours < 2):
                newArr[targetRow][targetCol] = 0
            # rule 2: thou shall live this generation if they neighbours are 2 or 3
            if (number_of_neighbours >= 2 and number_of_neighbours <= 3 ):
                newArr[targetRow][targetCol] = 1
            # rule 3: thou shall case if they neighbours are greater than 3
            if (number_of_neighbours > 3): 
                newArr[targetRow][targetCol] = 0
        
        else:
            # no

            # do you want to live?
            # rule 4: thou shall be give the essence of the almighty '1' if they neighbours are EXACTLY 3
            if (number_of_neighbours == 3):
                newArr[targetRow][targetCol] = 1

        return newArr

    def loop_through_array(self, old_array, n_array):
        rows = len(old_array)

        # for now, skip cells at the edges
        for curRow in range (1, rows - 1):
            for curCol in range (1, rows - 1):
                selected_cell = [curRow, curCol]
                number_of_neighbours = self.count_neighbours(old_array, selected_cell)
                # print(number_of_neighbours)

                n_array = self.decide_fate_cell(n_array, old_array, selected_cell, number_of_neighbours)
                # for row in new_array:
                #    print(row)
        
        print()
        for row in n_array:
            print(row)
        return n_array

    def loop(self):
        old_array = self.original_array
        row_size = len(old_array)
        col_size = len(old_array)

        new_array = [[0 for i in range(col_size)] for j in range(row_size)]
        

        print()
        for row in old_array:
            print(row)
        
        
        while True:
            temp_array = self.loop_through_array(old_array, new_array)
            old_array = temp_array
            new_array = [[0 for i in range(col_size)] for j in range(row_size)]
            time.sleep(1)