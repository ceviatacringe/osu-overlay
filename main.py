from overlay import OsuOverlay
from get_map_ID import get_map_macro

HOTKEY = 'f4'
TIME_TO_SLEEP = 0.03
TAB_LOADING_TIME = 0.2

def main():
    # Main function to run the application loop
    while True:
        # Get map details and prepare initialization
        get_map_macro(TIME_TO_SLEEP, TAB_LOADING_TIME, HOTKEY)
        overlay = OsuOverlay()
        # Run the canvas and circle rendering script
        overlay.initialize_script()

if __name__ == '__main__':
    main()