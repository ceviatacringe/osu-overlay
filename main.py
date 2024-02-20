from overlay import initialize_script
from get_map_ID import get_map_macro

HOTKEY = 'f4'
TIME_TO_SLEEP = 0.05
TAB_LOADING_TIME = 0.2

if __name__ == "__main__":
    while True:
        get_map_macro(TIME_TO_SLEEP, TAB_LOADING_TIME, HOTKEY)
        initialize_script()