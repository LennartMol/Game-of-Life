import engine
import test_arrays

game_engine = engine.Engine(array=test_arrays.pulsar,
                            debug=True)


def game_loop():
    while(True):
        game_engine.simulate_single_generation()

if __name__ == "__main__":
    game_loop()