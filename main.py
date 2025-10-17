import engine
import test_arrays
import pyglet
import window
import time
import threading

debug_state = True

game_engine = engine.Engine(array=test_arrays.glider_gun_array,
                            debug=False)

game_window = window.Window(game_engine=game_engine,
                            cell_size=20,
                            window_title='Game of Life',
                            debug=debug_state)

def game_loop():
    
    threading.Timer((1/400), game_loop).start()

    if(debug_state):
        start = time.time()

    game_engine.simulate_single_generation()
    
    if(debug_state):
        print(f"Generation took {(time.time() - start)*1000:.2f} ms")

if __name__ == "__main__":
    game_loop()
    pyglet.app.run()
