import test_arrays
import time
import copy

class Engine():

    def __init__(self, array, debug=True,):
        
        # Array size
        self.number_of_rows = len(array)
        self.number_of_columns = len(array)
        
        # Arrays
        self.old_generation_array = array
        self.new_array = [[0 for i in range(self.number_of_columns)] for j in range(self.number_of_rows)]
        self.next_generation_array = copy.deepcopy(self.new_array)

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
                if(self.debug == 'detail'):
                    print("Selected cell: " +str(selected_cell))
                    self.print_array(old_array, selected_cell = selected_cell)
                    
                number_of_neighbours = self.count_neighbours(old_array, selected_cell)
                if(self.debug == 'detail'):
                    print("Number of neighbours: " + str(number_of_neighbours))
                    print()
                
                n_array = self.decide_fate_cell(n_array, old_array, selected_cell, number_of_neighbours)
        
        if(self.debug):
            print() 
            print("Old generation array: ")        
            self.print_array(old_array)
        
        if(self.debug):
            print() 
            print("Next generation array: ")        
            self.print_array(n_array)


        return n_array
    
    def print_array(self, array, selected_cell = False):
        
        array_to_be_printed = copy.deepcopy(array)

        if(selected_cell != False):
            selRow = selected_cell[0]
            selCol = selected_cell[1]
            array_to_be_printed[selRow][selCol] = 'x'

        for row in array_to_be_printed:
            print(row)

    def simulate_single_generation(self):

        temp_array = self.loop_through_array(self.old_generation_array, self.next_generation_array)
        self.old_generation_array = temp_array
        self.next_generation_array = copy.deepcopy(self.new_array)
