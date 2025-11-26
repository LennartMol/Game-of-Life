import pyglet
import time
import numpy as np
from pyglet.gl import gl
import grids

class Window():

    def __init__(self, game_engine, game_grids, cell_size=20, window_title='Game of Life', debug=False):

        # Game engine instance
        self.game_engine = game_engine
        self.game_grid = game_grids

        # Grid variables
        self.number_of_rows = self.game_engine.number_of_rows
        self.number_of_columns = self.game_engine.number_of_columns
        
        # Window settings
        self.title = window_title
        self.simulation_window_offset = 200
        self.window_width = self.number_of_rows + self.simulation_window_offset
        self.window_height = self.number_of_columns
        self.window = pyglet.window.Window(self.window_width, self.window_height, self.title)
        self.exit_program = False
        self.check_if_reset_successful = False

        # Viewed simulation window
        self.cell_size = cell_size
        self.view_center = [self.number_of_rows//2, self.number_of_columns//2]
        self.view_size = 1024//self.cell_size
        self.distance_moved_x_pan = 0
        self.distance_moved_y_pan = 0
        self.distance_moved_x_select = 0
        self.distance_moved_y_select = 0

        # Textures & batch
        self.texture = None
        self.batch = pyglet.graphics.Batch()
                                                                                                                        
        # Create UI elements
        self.decrease_fps_button = self.create_decrease_fps_button()
        self.increase_fps_button = self.create_increase_fps_button()
        self.FPS_text_input = self.create_FPS_text_input_field()
        self.generations_passed_label = self.create_generations_passed_label()
        self.status_label = self.create_status_label()
        self.pause_button = self.create_pause_button()
        self.start_button = self.create_start_button()
        self.reset_button = self.create_reset_button()
        
        
        # Push and setcustom handlers
        self.window.push_handlers(on_draw=self.on_draw)
        self.window.push_handlers(on_close=self.on_close)
        self.window.push_handlers(on_mouse_press=self.on_mouse_press)
        self.window.push_handlers(on_mouse_drag=self.on_mouse_drag)
        self.window.push_handlers(on_mouse_scroll=self.on_mouse_scroll)  
        self.window.push_handlers(self.decrease_fps_button)
        self.window.push_handlers(self.increase_fps_button)
        self.window.push_handlers(self.start_button)
        self.window.push_handlers(self.pause_button)
        self.window.push_handlers(self.reset_button)
        self.window.push_handlers(self.FPS_text_input)
        self.FPS_text_input.set_handler('on_commit', self.FPS_text_input_on_commit_handler)
        self.decrease_fps_button.set_handler('on_press', self.decrease_fps_button_on_press_handler)
        self.increase_fps_button.set_handler('on_press', self.increase_fps_button_on_press_handler)
        self.start_button.set_handler('on_press', self.start_button_handler)
        self.pause_button.set_handler('on_press', self.pause_button_handler)
        self.reset_button.set_handler('on_press', self.reset_button_handler)

        # Debug flag
        self.debug_state = debug
    
    def create_decrease_fps_button(self):
        self.decrease = pyglet.resource.image("Images/button_minus.png")
        self.decrease.width = self.decrease.height = 40                                                                                                                                
        return pyglet.gui.PushButton(x=0, 
                                     y= self.window_height - 50, 
                                     pressed=self.decrease,
                                     unpressed=self.decrease,
                                     batch=self.batch)
        
    def create_increase_fps_button(self):
        self.increase = pyglet.resource.image("Images/button_plus.png")
        self.increase.width = self.increase.height = 40   
        return pyglet.gui.PushButton(x=100, 
                                     y= self.window_height - 50, 
                                     pressed=self.increase,
                                     unpressed=self.increase,
                                     batch=self.batch)
    
    def create_start_button(self):
        self.start = pyglet.resource.image("Images/button_start.png")
        self.start.width = self.start.height = 40
        return pyglet.gui.PushButton(x=100,
                                     y=self.window_height - 200,
                                     pressed=self.start,
                                     unpressed=self.start,
                                     batch=self.batch)
    
    def create_pause_button(self):
        self.pause = pyglet.resource.image("Images/button_pause.png")
        self.pause.width = self.pause.height = 40
        return pyglet.gui.PushButton(x=50,
                                     y=self.window_height - 200,
                                     pressed=self.pause,
                                     unpressed=self.pause,
                                     batch=self.batch)
    
    def create_reset_button(self):
        self.reset = pyglet.resource.image("Images/button_reset.png")
        self.reset.width = self.reset.height = 40
        return pyglet.gui.PushButton(x=50,
                                     y=self.window_height - 250,
                                     pressed=self.reset,
                                     unpressed=self.reset,
                                     batch=self.batch)
        
    def create_FPS_text_input_field(self):
        return pyglet.gui.TextEntry(str(self.game_engine.get_generations_per_second()),
                                    x= 55,
                                    y= self.window_height - 35,
                                    width=40,
                                    batch=self.batch)
    
    def create_generations_passed_label(self):
        return pyglet.text.Label('0',
                                 font_size=20,
                                 x=55,
                                 y=self.window_height - 55,
                                 anchor_x='center',
                                 anchor_y='center',
                                 batch=self.batch)
    
    def create_status_label(self):
        return pyglet.text.Label('Simulation paused',
                                 font_size=10,
                                 x=55,
                                 y=self.window_height - 100,
                                 anchor_x='center',
                                 anchor_y='center',
                                 batch=self.batch)

    def FPS_text_input_on_commit_handler(self, widget, input):
        if(int(input) > 1260 ):
            self.game_engine.update_generations_per_second(1260)
            self.FPS_text_input.value = str(1260)
        elif (int(input) >= 181):
            real_value = int(input) - int(input) % 180
            self.game_engine.update_generations_per_second(real_value)
            self.FPS_text_input.value = str(real_value)
        else:
            self.game_engine.update_generations_per_second(int(input))
    
    def decrease_fps_button_on_press_handler(self, widget):
        if(self.game_engine.get_generations_per_second() == 60 and self.game_engine.get_number_of_generations_per_game_loop() == 0):
            return
        elif((self.game_engine.get_generations_per_second() % 180 == 0) and not self.game_engine.get_number_of_generations_per_game_loop() == 1):
            self.FPS_text_input.value = str(int(self.FPS_text_input.value) - 180)
        else: 
            self.FPS_text_input.value = str(int(self.FPS_text_input.value) - 1)
        self.game_engine.update_generations_per_second(int(self.FPS_text_input.value))

    def increase_fps_button_on_press_handler(self, widget):
        if (int(self.FPS_text_input.value) == 1260):
           return
        elif(self.game_engine.get_generations_per_second() % 180 == 0):
            real_value = int(self.FPS_text_input.value) - int(self.FPS_text_input.value) % 180
            self.FPS_text_input.value = str(real_value + 180)

        else:
            self.FPS_text_input.value = str(int(self.FPS_text_input.value) + 1)
        self.game_engine.update_generations_per_second(int(self.FPS_text_input.value))

    def start_button_handler(self, widget):
        text_value = int(self.FPS_text_input.value)
        
        if (text_value == 0):
            self.FPS_text_input.value = str(5)
        elif (text_value > 1260):
            self.FPS_text_input.value = str(1260)
        self.game_engine.update_generations_per_second(int(self.FPS_text_input.value))
        self.game_engine.paused = False
        self.status_label.text = "Simulation running"

    def pause_button_handler(self, widget):
        self.game_engine.update_generations_per_second(0)
        self.game_engine.paused = True
        self.status_label.text = "Simulation paused"
    
    def reset_button_handler(self, widget):
        self.game_engine.update_generations_per_second(0)
        self.game_engine.paused = True
        self.status_label.text = "Simulation reset"
        self.game_engine.number_of_generations_passed = 0
        self.game_engine.old_generation_array = self.game_grid.create_empty_array()
        self.check_if_reset_successful = True

    def on_mouse_press(self, x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            self.toggle_cell_based_on_position(x, y, turn_on=True)

        if(button == pyglet.window.mouse.RIGHT):
            self.toggle_cell_based_on_position(x, y, turn_on=False)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        
        if buttons & pyglet.window.mouse.LEFT:
            if not dx == 0:
                self.distance_moved_x_select = self.distance_moved_x_select + dx
                if self.distance_moved_x_select > self.cell_size :
                    distance_to_move = np.rint(self.distance_moved_x_select / self.cell_size).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=True)
                    self.distance_moved_x_select = self.distance_moved_x_select - distance_to_move * self.cell_size
            
                elif self.distance_moved_x_select < (self.cell_size * -1):
                    distance_to_move = np.rint(self.distance_moved_x_select / (self.cell_size * -1)).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=True)
                    self.distance_moved_x_select = self.distance_moved_x_select - distance_to_move * (self.cell_size * -1)
            
            if not dy == 0:
                self.distance_moved_y_select = self.distance_moved_y_select + dy
                if self.distance_moved_y_select > self.cell_size :
                    distance_to_move = np.rint(self.distance_moved_y_select / self.cell_size).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=True)
                    self.distance_moved_y_select = self.distance_moved_y_select - distance_to_move * self.cell_size
            
                elif self.distance_moved_y_select < (self.cell_size * -1):
                    distance_to_move = np.rint(self.distance_moved_y_select / (self.cell_size * -1)).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=True)
                    self.distance_moved_y_select = self.distance_moved_y_select - distance_to_move * (self.cell_size * -1)
            
        if buttons & pyglet.window.mouse.RIGHT:
            if not dx == 0:
                self.distance_moved_x_select = self.distance_moved_x_select + dx
                if self.distance_moved_x_select > self.cell_size :
                    distance_to_move = np.rint(self.distance_moved_x_select / self.cell_size).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=False)
                    self.distance_moved_x_select = self.distance_moved_x_select - distance_to_move * self.cell_size
            
                elif self.distance_moved_x_select < (self.cell_size * -1):
                    distance_to_move = np.rint(self.distance_moved_x_select / (self.cell_size * -1)).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=False)
                    self.distance_moved_x_select = self.distance_moved_x_select - distance_to_move * (self.cell_size * -1)
            
            if not dy == 0:
                self.distance_moved_y_select = self.distance_moved_y_select + dy
                if self.distance_moved_y_select > self.cell_size :
                    distance_to_move = np.rint(self.distance_moved_y_select / self.cell_size).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=False)
                    self.distance_moved_y_select = self.distance_moved_y_select - distance_to_move * self.cell_size
            
                elif self.distance_moved_y_select < (self.cell_size * -1):
                    distance_to_move = np.rint(self.distance_moved_y_select / (self.cell_size * -1)).astype(int)
                    self.toggle_cell_based_on_position(x, y, turn_on=False)
                    self.distance_moved_y_select = self.distance_moved_y_select - distance_to_move * (self.cell_size * -1)

        if buttons & pyglet.window.mouse.MIDDLE:
            
            if not dx == 0:
                # calculate total pixels moved between handler events. eg DMX: 15 and DX: 30
                self.distance_moved_x_pan = self.distance_moved_x_pan + dx
                # check if distance moved is greater than a cell. eg Cell: 16, so check if 15+30 > 16
                if self.distance_moved_x_pan > self.cell_size :
                    # calculate if multiple cells have been crossed. eg 45/16 = 2.8125, so 2 have been crossed
                    distance_to_move = np.rint(self.distance_moved_x_pan / self.cell_size).astype(int)
                    # move distance based on cells crossed. eg 2.8125 > 2 cells crossed
                    self.view_center[1] = self.view_center[1] - distance_to_move
                    # remainder 0.8125 times cellsize is distance moved for next event: 0.8125 * 16 = 13
                    # save this distance
                    self.distance_moved_x_pan = self.distance_moved_x_pan - distance_to_move * self.cell_size
                
                elif self.distance_moved_x_pan < (self.cell_size * -1):
                    distance_to_move = np.rint(self.distance_moved_x_pan / (self.cell_size * -1)).astype(int)
                    self.view_center[1] = self.view_center[1] + distance_to_move
                    self.distance_moved_x_pan = self.distance_moved_x_pan - distance_to_move * (self.cell_size * -1)
            
            
            if not dy == 0:
                self.distance_moved_y_pan = self.distance_moved_y_pan + dy
                if self.distance_moved_y_pan > self.cell_size :
                    distance_to_move = np.rint(self.distance_moved_y_pan / self.cell_size).astype(int)
                    self.view_center[0] = self.view_center[0] - distance_to_move
                    self.distance_moved_y_pan = self.distance_moved_y_pan - distance_to_move * self.cell_size
                elif self.distance_moved_y_pan < (self.cell_size * -1):
                    distance_to_move = np.rint(self.distance_moved_y_pan / (self.cell_size * -1)).astype(int)
                    self.view_center[0] = self.view_center[0] + distance_to_move
                    self.distance_moved_y_pan= self.distance_moved_y_pan - distance_to_move * (self.cell_size * -1)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            if self.cell_size == 32:
                return
            else:
                self.cell_size = self.cell_size * 2
                self.texture = None
        else:
            if self.cell_size == 1:
                return
            else: 
                self.cell_size = self.cell_size / 2 
                self.texture = None
    
    def on_close(self):
        self.exit_program = True
    
    def on_draw(self):
        if(self.debug_state):
            start = time.time()

        self.window.clear()

        self.generations_passed_label.text = str(self.game_engine.number_of_generations_passed)

        self.draw_texture()

        self.batch.draw()

        if(self.check_if_reset_successful):
            if(int(self.generations_passed_label.text) != 0):
                if(self.debug_state):
                    print("Reset improperly performed")
                self.game_engine.number_of_generations_passed = 0
                self.game_engine.old_generation_array = self.game_grid.create_empty_array()    
            self.check_if_reset_successful = False
            
        
        if(self.debug_state):
            print(f"Drawing took {(time.time() - start)*1000:.2f} ms")

    def toggle_cell_based_on_position(self, x, y, turn_on):
        if(x <= self.simulation_window_offset):
                return
            
        # calculate y position to toggle cell
        cell_position_y = y//self.cell_size
        pos_relative_to_view_size_y = cell_position_y - (self.view_size/2)
        row = np.rint(self.view_center[0] + pos_relative_to_view_size_y).astype(int)
        
        # calculate x position to toggle cell
        cell_position_x = (x - self.simulation_window_offset)//self.cell_size
        pos_relative_to_view_size_x = cell_position_x - (self.view_size/2)
        col = np.rint(self.view_center[1] + pos_relative_to_view_size_x).astype(int)
        
        # out of bounds click
        if row >= 1024 or col >= 1024:
            return

        if turn_on:
                self.game_engine.old_generation_array[row][col] = 1
        else:
                self.game_engine.old_generation_array[row][col] = 0
    
    def draw_texture(self):

        arr = np.array(self.game_engine.old_generation_array, dtype=np.uint8)

        self.view_size = np.rint(1024//self.cell_size).astype(int)

        offset_y = 0
        r0 = self.view_center[0] - self.view_size//2
        if r0 < 0:
            offset_y = r0
            r0 = 0
        r1 = self.view_center[0] + self.view_size//2
        if r1 > 1024:
            offset_y = r1 - 1024
            r1 = 1024
        elif r1 < 0:
            r1 = 0
        
        offset_x = 0
        c0 = self.view_center[1] - self.view_size//2
        if c0 < 0:
                offset_x = c0 
                c0 = 0
        c1 = self.view_center[1] + self.view_size//2
        if c1 > 1024:
            offset_x = c1 - 1024
            c1 = 1024
        elif c1 < 0:
            c1 = 0

        arr_center = arr[r0:r1, c0:c1]

        end_arr = arr_center        
        if (not offset_x == 0 or not offset_y == 0):
            array_x_offset = np.full((arr_center.shape[0], abs(offset_x)), 100)
            
            if offset_x >= self.view_size or offset_x <= -abs(self.view_size) or offset_y >= 1024 or offset_y <= -abs(self.view_size):
                end_arr = np.full((self.view_size, self.view_size), 100)
            else:
                if offset_x > 0:
                    end_arr = np.hstack((arr_center, array_x_offset))
                else:
                    end_arr = np.hstack((array_x_offset, arr_center))
                
                array_y_offset = np.full((np.abs(offset_y),end_arr.shape[1]), 100)
                if offset_y > 0:
                    end_arr = np.vstack((end_arr, array_y_offset))
                else:
                    end_arr = np.vstack((array_y_offset, end_arr))
        
        
        img_data = np.zeros((self.view_size, self.view_size, 3), dtype=np.uint8)
        img_data[end_arr == 1] = (255, 255, 255)  # white for alive, black by default
        img_data[end_arr == 100] = (100, 100, 100) # out of bounds color

        raw_bytes = img_data[::].tobytes()

        if self.texture is None:
            image_data = pyglet.image.ImageData(
                self.view_size, self.view_size, 'RGB', raw_bytes
            )
            tex = image_data.get_texture()
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex.id)
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
            self.texture = tex
            
        else:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture.id)
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
            gl.glTexSubImage2D(
                gl.GL_TEXTURE_2D, 0, 0, 0,
                self.view_size, self.view_size,
                gl.GL_RGB, gl.GL_UNSIGNED_BYTE, raw_bytes
            )

        
        sim_width  = self.window_width  - self.simulation_window_offset
        sim_height = self.window_height
        self.texture.blit(
            self.simulation_window_offset, 0,
            width=sim_width,
            height=sim_height
        )