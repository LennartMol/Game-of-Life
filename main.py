import engine
import test_arrays

game_engine = engine.Engine(array=test_arrays.arr_vert,
                            debug=True)


def game_loop():
    game_engine.loop()

if __name__ == "__main__":
    game_loop()