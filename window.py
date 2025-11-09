import pyglet
import time
import numpy as np
from pyglet.gl import gl

class Window():

    def __init__(self, game_engine, cell_size=20, window_title='Game of Life', debug=False):

        # Game engine instance
        self.game_engine = game_engine

        # Grid variables
        self.number_of_rows = self.game_engine.number_of_rows
        self.number_of_columns = self.game_engine.number_of_columns
        
        # Window settings
        self.title = window_title
        self.simulation_window_offset = 200
        self.window_width = self.number_of_rows + self.simulation_window_offset
        self.window_height = self.number_of_columns
        self.window = pyglet.window.Window(self.window_width, self.window_height, self.title)

        # Viewed simulation window
        # 1024x1024 -> Size 1 (1024), size 2 (512), size 4 (256), size 8 (128), 16 (64), 32 (32)
        self.cell_size = cell_size
        self.view_center = [self.number_of_rows//2, self.number_of_columns//2]
        self.view_size = 1024//self.cell_size
        

        # Textures & batch
        self.texture = None
        self.batch = pyglet.graphics.Batch()
                                                                                                                        
        # Create UI elements
        self.decrease_fps_button = self.create_decrease_fps_button()
        self.increase_fps_button = self.create_increase_fps_button()
        self.FPS_text_input = self.create_FPS_text_input_field()
        
        # Push and setcustom handlers
        self.window.push_handlers(on_draw=self.on_draw)
        self.window.push_handlers(on_mouse_press=self.on_mouse_press)
        self.window.push_handlers(on_mouse_scroll=self.on_mouse_scroll)  
        self.window.push_handlers(self.decrease_fps_button)
        self.window.push_handlers(self.increase_fps_button)
        self.window.push_handlers(self.FPS_text_input)
        self.FPS_text_input.set_handler('on_commit', self.FPS_text_input_on_commit_handler)
        self.decrease_fps_button.set_handler('on_press', self.decrease_fps_button_on_press_handler)
        self.increase_fps_button.set_handler('on_press', self.increase_fps_button_on_press_handler)

        # Debug flag
        self.debug_state = debug
    
    def create_decrease_fps_button(self):
        self.decrease_pressed = pyglet.resource.image("Images/button_decrease_pressed.png", border=1)
        self.decrease_pressed.width = 50
        self.decrease_pressed.height = 50   
        self.decrease_unpressed = pyglet.resource.image("Images/button_decrease_unpressed.png", border=1)
        self.decrease_unpressed.width = 50 
        self.decrease_unpressed.height = 50                                                                                                                               

        return pyglet.gui.PushButton(x=0, 
                                     y= self.window_height - 50, 
                                     pressed=self.decrease_pressed,
                                     unpressed=self.decrease_unpressed,
                                     hover=None,
                                     batch=self.batch,
                                     group=None)
        
    def create_increase_fps_button(self):
        self.increase_pressed = pyglet.resource.image("Images/button_increase_pressed.png")
        self.increase_pressed.width = 50
        self.increase_pressed.height = 50   
        self.increase_unpressed = pyglet.resource.image("Images/button_increase_unpressed.png")
        self.increase_unpressed.width = 50 
        self.increase_unpressed.height = 50 

        return pyglet.gui.PushButton(x=100, 
                                     y= self.window_height - 50, 
                                     pressed=self.increase_pressed,
                                     unpressed=self.increase_unpressed,
                                     hover=None,
                                     batch=self.batch,
                                     group=None)

    def create_FPS_text_input_field(self):
        return pyglet.gui.TextEntry(str(self.game_engine.get_generations_per_second()),
                                    x= 55,
                                    y= self.window_height - 35,
                                    width=40,
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
    
    def on_mouse_press(self, x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            if(x <= self.simulation_window_offset):
                return
            col = np.rint((((x-self.simulation_window_offset) // self.cell_size) + (self.number_of_columns - self.view_size)//2) - ((x-self.simulation_window_offset) % self.cell_size // self.view_size)).astype(int)
            row = np.rint(((y // self.cell_size) + (self.number_of_rows - self.view_size)//2) - (y % self.cell_size // self.view_size)).astype(int)

            if(self.game_engine.old_generation_array[row][col]):
                 self.game_engine.old_generation_array[row][col] = 0
            else:
                 self.game_engine.old_generation_array[row][col] = 1

        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            if self.cell_size == 32:
                pass
            else:
                self.cell_size = self.cell_size * 2
                self.texture = None
        else:
            if self.cell_size == 1:
                pass
            else: 
                self.cell_size = self.cell_size / 2 
                self.texture = None

    def on_draw(self):
        if(self.debug_state):
            start = time.time()

        self.window.clear()

        self.draw_texture()

        self.batch.draw()
        
        if(self.debug_state):
            print(f"Drawing took {(time.time() - start)*1000:.2f} ms")

    def draw_texture(self):

        arr = np.array(self.game_engine.old_generation_array, dtype=np.uint8)

        self.view_size = np.rint(1024//self.cell_size).astype(int)

        r0 = self.view_center[0] - self.view_size//2
        r1 = self.view_center[0] + self.view_size//2
        c0 = self.view_center[1] - self.view_size//2
        c1 = self.view_center[1] + self.view_size//2

        arr_center = arr[r0:r1, c0:c1]
        
        img_data = np.zeros((self.view_size, self.view_size, 3), dtype=np.uint8)
        img_data[arr_center == 1] = (255, 255, 255)  # white for alive, black by default

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