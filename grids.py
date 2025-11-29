import numpy as np

class Grids():

    def __init__(self):
        
        self.glider_gun_array = self.create_glider_gun_array_2()

    def create_empty_array(self):
        temp = [[0 for i in range(1024)] for j in range(1024)]
        return np.array(temp, dtype=np.uint8)
    
    def create_glider_gun_array(self):
        temp_array = [[0 for i in range(1024)] for j in range(1024)]

        coords = [
            (5, 1), (5, 2), (6, 1), (6, 2),                       # Small square on the left

            (5, 11), (6, 11), (7, 11),                            # Left vertical bar
            (4, 12), (8, 12),
            (3, 13), (9, 13),
            (3, 14), (9, 14),
            (6, 15),
            (4, 16), (8, 16),
            (5, 17), (6, 17), (7, 17),
            (6, 18),                                               # Right side of first module

            (3, 21), (4, 21), (5, 21),
            (3, 22), (4, 22), (5, 22),                            # Second small block

            (2, 23), (6, 23),
            (1, 25), (2, 25), (6, 25), (7, 25),

            (3, 35), (4, 35), (3, 36), (4, 36)                    # Rightmost small square
        ]

        for (r, c) in coords:
            temp_array[r][c] = 1
        
        return temp_array
    
    def create_glider_gun_array_2(self):
        temp_array = [[0 for i in range(1024)] for j in range(1024)]

        coords = []

        glider = [
            (1, 1), (1, 3), (2, 2), (2, 3), (2, 3), (3, 2),                      
        ]

        coords.extend(glider)

        

        for total_gliders in range(205):
            
            temp_glider = glider.copy()
            
            for x in range(6):
                temp_glider[x] = (temp_glider[x][0], temp_glider[x][1] + (total_gliders*5))

            coords.extend(temp_glider)

        for total_y_gliders in range(102):

            for total_gliders in range(205):
                
                temp_glider = glider.copy()
                
                for x in range(6):
                    temp_glider[x] = (temp_glider[x][0] + (total_y_gliders*10), temp_glider[x][1] + (total_gliders*5))

                coords.extend(temp_glider)

        for (r, c) in coords:
            temp_array[r][c] = 1
        
        return temp_array