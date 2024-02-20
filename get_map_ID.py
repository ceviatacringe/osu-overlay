import time
import win32api
import win32con
import keyboard
import pyperclip
import pyautogui


TIME_TO_SLEEP = 0.03
TAB_LOADING_TIME = 0.2


def press_key_1():
    win32api.keybd_event(0x31, 0, 0, 0)  # Key down
    time.sleep(0.005)
    win32api.keybd_event(0x31, 0, win32con.KEYEVENTF_KEYUP, 0)  # Key up


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # Mouse down
    time.sleep(0.005)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # Mouse up


def get_map_macro():
    print("Got here")
    #Automatically get the map ID through browser URL
    left_click()
    time.sleep(TIME_TO_SLEEP)

    press_key_1()  # Opens the osu map in the website using the osu menu
    pyperclip.copy("")  # Clear the clipboard content

    time.sleep(TAB_LOADING_TIME)
    keyboard.press_and_release('ctrl+l')  # Highlight address bar
    time.sleep(TIME_TO_SLEEP)

    keyboard.press_and_release('ctrl+c')  # Copy URL
    time.sleep(TIME_TO_SLEEP)

    keyboard.press_and_release('ctrl+w')  # Close the tab
    time.sleep(TIME_TO_SLEEP)

    # Bring up osu once finished
    windows = pyautogui.getWindowsWithTitle("osu!")
    if windows:
        windows[0].activate()

    # Check if clipboard has content (if everything ran successfully)
    if pyperclip.paste():
        print("Map ID found")
    else:
        print("Failed to get beatmap ID\nTrying again...")
        get_map_macro()

