import copy
from numba import njit, prange
import numpy as np

class Engine():

    def __init__(self, array, cells_loop_border=False, caching=True, precompiler=True, debug=False):
        
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

        # Performance settings
        self.cells_loop_border = cells_loop_border
        self.caching = caching
        self.precompiler = precompiler

        # Compiled functions to simulate a next generation
        self.simulate_function = njit(parallel=True, fastmath=True, cache=caching)(simulate_numba_generation)
        self.simulate_function_loop = njit(parallel=True, fastmath=True, cache=caching)(simulate_numba_generation_loop)

        if self.precompiler: self.precompile_numba_code()

        # Debug flag
        self.debug = debug
    
    def precompile_numba_code(self):
        if self.cells_loop_border:
            self.simulate_function_loop(np.zeros((5,5), dtype=np.uint8))
        else: 
            self.simulate_function(np.zeros((5,5), dtype=np.uint8))

    
    def print_array(self, array, selected_cell = False):
        
        array_to_be_printed = copy.deepcopy(array)

        if(selected_cell != False):
            selRow = selected_cell[0]
            selCol = selected_cell[1]
            array_to_be_printed[selRow][selCol] = 'x'

        for row in array_to_be_printed:
            print(row)

    def simulate_single_generation(self):
        if self.cells_loop_border:
            self.old_generation_array = self.simulate_function_loop(self.old_generation_array)
        else: 
            self.old_generation_array = self.simulate_function(self.old_generation_array)


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

def simulate_numba_generation(arr):
    rows, cols = arr.shape
    new_arr = np.zeros_like(arr, dtype=np.uint8)

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

def simulate_numba_generation_loop(arr):
    rows, cols = arr.shape
    new_arr = np.zeros_like(arr, dtype=np.uint8)

    row_above = np.empty(rows, np.int64)
    row_below = np.empty(rows, np.int64)
    col_left  = np.empty(cols, np.int64)
    col_right = np.empty(cols, np.int64)

    for r in range(rows):
        row_above[r] = (r - 1 + rows) % rows
        row_below[r] = (r + 1) % rows
    for c in range(cols):
        col_left[c]  = (c - 1 + cols) % cols
        col_right[c] = (c + 1) % cols

    for r in prange(rows):
        ra = row_above[r]
        rb = row_below[r]
        for c in range(cols):
            cl = col_left[c]
            cr = col_right[c]

            n = (
                arr[ra, cl] + arr[ra, c] + arr[ra, cr] +
                arr[r,  cl]               + arr[r,  cr] +
                arr[rb, cl] + arr[rb, c] + arr[rb, cr]
            )

            if arr[r, c] == 1:
                new_arr[r, c] = 1 if n == 2 or n == 3 else 0
            else:
                new_arr[r, c] = 1 if n == 3 else 0

    return new_arr