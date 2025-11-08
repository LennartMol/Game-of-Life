import copy
from numba import njit, prange
import numpy as np

class Engine():

    def __init__(self, array, debug=False,):
        
        # Array size
        self.number_of_rows = len(array)
        self.number_of_columns = len(array)
        
        # Arrays
        self.old_generation_array = np.array(array, dtype=np.uint8)

        # simulation speed
        self.__generations_per_second = 0
        self.__number_of_generations_per_game_loop = 1
        self.frame_counter = 1
        self.skip_most_frames = None
        self.divider = None

        # Debug flag
        self.debug = debug
        
    
    def print_array(self, array, selected_cell = False):
        
        array_to_be_printed = copy.deepcopy(array)

        if(selected_cell != False):
            selRow = selected_cell[0]
            selCol = selected_cell[1]
            array_to_be_printed[selRow][selCol] = 'x'

        for row in array_to_be_printed:
            print(row)

    def simulate_single_generation(self):
        self.old_generation_array = simulate_next_generation(self.old_generation_array)

    def update_generations_per_second(self, GPS):
        if (GPS < 1):
            self.__generations_per_second = 60
            self.__number_of_generations_per_game_loop = 0

        elif(GPS <= 180):
            self.__generations_per_second = GPS
            self.__number_of_generations_per_game_loop = 1

        else:
            self.__generations_per_second = 180
            self.__number_of_generations_per_game_loop = round(GPS/180)
            

    def get_generations_per_second(self):
        return self.__generations_per_second

    def get_number_of_generations_per_game_loop(self):
        return self.__number_of_generations_per_game_loop

@njit(parallel=True, fastmath=True)
def simulate_next_generation(arr):
    rows, cols = arr.shape
    new_arr = np.zeros_like(arr, dtype=np.uint8)

    # skip borders for simplicity (keeps edges dead)
    for r in prange(1, rows - 1):
        for c in range(1, cols - 1):
            n = (
                arr[r-1, c-1] + arr[r-1, c] + arr[r-1, c+1] +
                arr[r, c-1]               + arr[r, c+1] +
                arr[r+1, c-1] + arr[r+1, c] + arr[r+1, c+1]
            )

            if arr[r, c] == 1:
                new_arr[r, c] = 1 if n == 2 or n == 3 else 0
            else:
                new_arr[r, c] = 1 if n == 3 else 0

    return new_arr
    
    arr = self.old_generation_array

    # Count neighbours using fast array shifting
    neighbours = (
        np.roll(arr,  1, axis=0) + np.roll(arr, -1, axis=0) +  # up/down
        np.roll(arr,  1, axis=1) + np.roll(arr, -1, axis=1) +  # left/right
        np.roll(np.roll(arr, 1, axis=0),  1, axis=1) +          # top-left
        np.roll(np.roll(arr, 1, axis=0), -1, axis=1) +          # top-right
        np.roll(np.roll(arr, -1, axis=0), 1, axis=1) +          # bottom-left
        np.roll(np.roll(arr, -1, axis=0), -1, axis=1)           # bottom-right
    )

    # Apply Game of Life rules (vectorized)
    new_arr = ((arr == 1) & ((neighbours == 2) | (neighbours == 3))) | \
                ((arr == 0) & (neighbours == 3))

    self.old_generation_array = new_arr.astype(np.uint8)

    if(self.debug == True):
        self.print_array(self.old_generation_array)