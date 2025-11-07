import copy
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
    
    def simulate(self):
        if(self.__generations_per_second == 0):
            return

        if(self.skip_most_frames):
            if(self.debug == "Frames"):
                print(f"Skip_most_frames: {self.skip_most_frames}")
                print(f"Frame_count: {self.frame_counter}")
            
            # checks if frame does not have to be skipped, otherwise skips frame
            if( not (self.divider / self.frame_counter % 1) == 0):
                self.simulate_single_generation()
                if(self.debug == "Frames"):
                    print(f"Frame not skipped")
            
        else:
            if( not (self.divider / self.frame_counter % 1) == 0):
                self.simulate_single_generation()
        


        if(self.frame_counter >= 60):
            self.frame_counter = 1
            return
        
        self.frame_counter = self.frame_counter + 1

    def update_generations_per_second(self, GPS):
        if(GPS <= 60):
            
            self.divider = GPS / 60
            
            # if lower than 0.5 -> less than 50% of frames simulate a new generation
            if (self.divider <= 0.5):
                self.skip_most_frames = True
            # opposite is true, most frames do simulate new generation
            else:
                self.skip_most_frames = False
            
            self.__generations_per_second = GPS