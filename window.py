import pyglet
import time
import numpy as np

class Window():

    def __init__(self, game_engine, cell_size=20, window_title='Game of Life', debug=False):

        # Game engine
        self.game_engine = game_engine

        # Grid
        self.number_of_rows = self.game_engine.number_of_rows
        self.number_of_columns = self.game_engine.number_of_columns
        self.cell_size = cell_size

        # window
        self.title = window_title
        self.simulation_window_offset = 800
        self.window_width = self.cell_size * self.number_of_columns + self.simulation_window_offset
        self.window_height = self.cell_size * self.number_of_rows
        self.window = pyglet.window.Window(self.window_width, self.window_height, self.title)
    
        self.debug_state = debug

        self.batch = pyglet.graphics.Batch()
        self.cells = self.create_batch_cells()

        self.window.push_handlers(on_draw=self.on_draw)
        self.window.push_handlers(on_mouse_press=self.on_mouse_press)
 
        self.decrease_pressed = pyglet.resource.image("button_decrease_pressed.png", border=1)
        self.decrease_pressed.width = 50
        self.decrease_pressed.height = 50   
        self.decrease_unpressed = pyglet.resource.image("button_decrease_unpressed.png", border=1)
        self.decrease_unpressed.width = 50 
        self.decrease_unpressed.height = 50                                                                                                                               

        self.decrease_fps_button = pyglet.gui.PushButton(x=0, 
                                                         y= self.window_height - 50, 
                                                         pressed=self.decrease_pressed,
                                                         unpressed=self.decrease_unpressed,
                                                         hover=None,
                                                         batch=self.batch,
                                                         group=None)
        
        self.increase_pressed = pyglet.resource.image("button_increase_pressed.png")
        self.increase_pressed.width = 50
        self.increase_pressed.height = 50   
        self.increase_unpressed = pyglet.resource.image("button_increase_unpressed.png")
        self.increase_unpressed.width = 50 
        self.increase_unpressed.height = 50 

        self.increase_fps_button = pyglet.gui.PushButton(x=100, 
                                                         y= self.window_height - 50, 
                                                         pressed=self.increase_pressed,
                                                         unpressed=self.increase_unpressed,
                                                         hover=None,
                                                         batch=self.batch,
                                                         group=None)
        
        self.window.push_handlers(self.decrease_fps_button)
        self.window.push_handlers(self.increase_fps_button)
        self.decrease_fps_button.set_handler('on_press', self.decrease_fps_button_on_press_handler)
        self.increase_fps_button.set_handler('on_press', self.increase_fps_button_on_press_handler)

        self.FPS_text_input = pyglet.gui.TextEntry(str(game_engine.get_generations_per_second()),
                                                   x= 55,
                                                   y= self.window_height - 35,
                                                   width=40,
                                                   batch=self.batch)
        
        self.window.push_handlers(self.FPS_text_input)
        self.FPS_text_input.set_handler('on_commit', self.FPS_text_input_on_commit_handler)
    
    def FPS_text_input_on_commit_handler(self, widget, input):
        if (int(input) >= 181):
            real_value = int(input) - int(input) % 180
            self.game_engine.update_generations_per_second(real_value)
            self.FPS_text_input.value = str(real_value)
        else:
            self.game_engine.update_generations_per_second(int(input))
    
    def decrease_fps_button_on_press_handler(self, widget):
        if(self.game_engine.get_generations_per_second() == 1 and self.game_engine.get_number_of_generations_per_game_loop() == 0):
            return
        elif((self.game_engine.get_generations_per_second() % 180 == 0) and not self.game_engine.get_number_of_generations_per_game_loop() == 1):
            self.FPS_text_input.value = str(int(self.FPS_text_input.value) - 180)
        else: 
            self.FPS_text_input.value = str(int(self.FPS_text_input.value) - 1)
        self.game_engine.update_generations_per_second(int(self.FPS_text_input.value))

    def increase_fps_button_on_press_handler(self, widget):
        if(self.game_engine.get_generations_per_second() % 180 == 0):
            real_value = int(self.FPS_text_input.value) - int(self.FPS_text_input.value) % 180
            self.FPS_text_input.value = str(real_value + 180)

        else:
            self.FPS_text_input.value = str(int(self.FPS_text_input.value) + 1)
        self.game_engine.update_generations_per_second(int(self.FPS_text_input.value))
    
    def on_mouse_press(self, x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            if(x <= 800):
                return
            
            col = np.rint((x - x % 20 - self.simulation_window_offset) / 20).astype(int)
            row = np.rint((y - y % 20) / 20).astype(int)



            if(self.game_engine.old_generation_array[row][col]):
                 self.game_engine.old_generation_array[row][col] = 0
            else:
                 self.game_engine.old_generation_array[row][col] = 1



        pass

    def on_draw(self):
        if(self.debug_state):
            start = time.time()

        self.window.clear()

        self.update_cell_positions()
        self.batch.draw()
        
        if(self.debug_state):
            print(f"Drawing took {(time.time() - start)*1000:.2f} ms")
        
    
    def update_cell_positions(self):
        for i, cell in enumerate(self.cells):
            row = i // self.number_of_columns
            col = i % self.number_of_columns
            cell.color = (255, 255, 255) if self.game_engine.old_generation_array[row][col] else (0, 0, 0)

    def create_batch_cells(self):
        cells = []
        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                x = col * self.cell_size + self.simulation_window_offset
                y = row * self.cell_size
                color = (255, 255, 255) if self.game_engine.old_generation_array[row][col] else (0, 0, 0)
                cell = pyglet.shapes.Rectangle(x, y, self.cell_size, self.cell_size, color=color, batch=self.batch)
                cells.append(cell)
        
        return cells