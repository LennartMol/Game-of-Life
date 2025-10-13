import pyglet

class Window():

    def __init__(self, game_engine, cell_size=20, window_title='Game of Life'):

        # Game engine
        self.game_engine = game_engine

        # Grid
        self.number_of_rows = self.game_engine.number_of_rows
        self.number_of_columns = self.game_engine.number_of_columns
        self.cell_size = cell_size
        self.array = self.game_engine.old_generation_array

        # window
        self.title = window_title
        self.window_width = self.cell_size * self.number_of_columns
        self.window_height = self.cell_size * self.number_of_rows
        self.window = pyglet.window.Window(self.window_width , self.window_height, self.title)
    
        self.rectangles = []
        self.create_rectangles()

    def draw_window(self):
        self.window.clear()
        for rect in self.rectangles:
            rect.draw()

    def create_rectangles(self):
        self.rectangles = []
        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                x = col * self.cell_size
                y = row * self.cell_size
                color = (255, 255, 255) if self.array[row][col] else (30, 30, 30)
                rect = pyglet.shapes.Rectangle(x, y, self.cell_size, self.cell_size, color=color)
                self.rectangles.append(rect)
