import pyglet
import time

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
        self.window_width = self.cell_size * self.number_of_columns
        self.window_height = self.cell_size * self.number_of_rows
        self.window = pyglet.window.Window(self.window_width , self.window_height, self.title)
    
        self.debug_state = debug

        self.batch = pyglet.graphics.Batch()
        self.cells = self.create_batch_cells()

        self.window.push_handlers(on_draw=self.on_draw)

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
                x = col * self.cell_size
                y = row * self.cell_size
                color = (255, 255, 255) if self.game_engine.old_generation_array[row][col] else (0, 0, 0)
                cell = pyglet.shapes.Rectangle(x, y, self.cell_size, self.cell_size, color=color, batch=self.batch)
                cells.append(cell)
        
        return cells