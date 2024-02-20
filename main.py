from overlay import initialize_script
from get_map_ID import get_map_macro
import keyboard

if __name__ == "__main__":
    while True:
        print("Waitin")
        keyboard.wait('f4')
        get_map_macro()
        initialize_script()