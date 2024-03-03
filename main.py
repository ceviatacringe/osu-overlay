from overlay import OsuOverlay
from get_map_ID import get_map_macro

HOTKEY = 'f4'
TIME_TO_SLEEP = 0.03
TAB_LOADING_TIME = 0.08
# This will automatically minimize the browser after opening a map
# To enable, put in your own path, to disable, set to: None
BROWSER_TO_MINIMIZE = 'Chrome'

# Select appropriate osu mods
DT = False
HR = False
EZ = False

def main():
    # Main function to run the application loop
    while True:
        # Get map details and prepare initialization
        get_map_macro(TIME_TO_SLEEP, TAB_LOADING_TIME, HOTKEY, BROWSER_TO_MINIMIZE)
        overlay = OsuOverlay(DT, HR, EZ)
        # Run the canvas and circle rendering script
        overlay.initialize_script()

if __name__ == '__main__':
    main()