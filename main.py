from overlay import initialize_script
from get_map_ID import get_map_macro

HOTKEY = 'f4'

if __name__ == "__main__":
    while True:
        get_map_macro(HOTKEY)
        initialize_script()