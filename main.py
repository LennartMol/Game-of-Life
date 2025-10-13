import engine
import test_arrays
import pyglet
import window

game_engine = engine.Engine(array=test_arrays.pulsar,
                            debug=True)

game_window = window.Window(game_engine=game_engine,
                            cell_size=20,
                            window_title='Game of Life')

def game_loop(self):
    game_engine.simulate_single_generation()
    game_window.draw_window()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_loop, 1) # update game loop every second
    pyglet.app.run()
