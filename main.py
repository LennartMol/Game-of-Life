import engine
import grids
import pyglet
import window
import time
import threading

debug_state = False

game_engine = engine.Engine(array=grids.glider_gun_array,
                            cells_loop_border=True,
                            caching=True,
                            precompiler=True,
                            debug="Frames")

game_window = window.Window(game_engine=game_engine,
                            cell_size=1,
                            window_title='Game of Life',
                            debug=debug_state)

def game_loop():

    if(game_window.exit_program):
        quit()

    if(debug_state):
        start = time.time()


    threading.Timer((1/game_engine.get_generations_per_second()), game_loop).start()

    for simulations in range(game_engine.get_number_of_generations_per_game_loop()):
        game_engine.simulate_single_generation()

    if(debug_state):
        print(f"Calculating next generation of cells took {(time.time() - start)*1000:.2f} ms")

if __name__ == "__main__":
    game_engine.update_generations_per_second(0)
    game_loop()
    pyglet.app.run()
