import time
import win32api
import win32con
import keyboard
import pyperclip
import pyautogui
import win32gui
import os 


class GetStart:
    def __init__(self, time_to_sleep, tab_loading_time, hotkey, browser_to_minimize):
        self.time_to_sleep = time_to_sleep
        self.tab_loading_time = tab_loading_time
        self.hotkey = hotkey
        self.browser_to_minimize = browser_to_minimize
        self.mods = ""
        self.map_id = ""

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_focus(self):
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "osu!":
            return True
        return False

    def press_key_1(self):
        win32api.keybd_event(0x31, 0, 0, 0)  # Key down
        time.sleep(self.time_to_sleep)
        win32api.keybd_event(0x31, 0, win32con.KEYEVENTF_KEYUP, 0)  # Key up

    def left_click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # Mouse down
        time.sleep(self.time_to_sleep)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # Mouse up

    def mod_selection(self):
        self.clear_screen()
        print("Mod selection opened")
        print("Use keys to select mods (D,F,H) -> DT HD FL for example")
        print("Once you're done exit with esc, 2, for F1")
        time.sleep(0.03)
        self.press_key_1()
        while True:
            if self.check_focus():
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'q':
                        self.mods += " EZ "
                    elif event.name == 'e':
                        self.mods += " HT "
                    elif event.name == 'a':
                        self.mods += " HR "
                    elif event.name == 'd':
                        self.mods += " DT "
                    elif event.name == 'f':
                        self.mods += " HD "
                    elif event.name == 'g':
                        self.mods += " FL "
                    elif event.name == "f1" or event.name == 'esc' or event.name == '2':
                        self.clear_screen()
                        return self.mods

    def get_map_macro(self):
        return_to = win32api.GetCursorPos()
        win32api.SetCursorPos((490, 178))
        time.sleep(self.time_to_sleep)
        self.left_click()
        time.sleep(self.time_to_sleep)
        win32api.SetCursorPos(return_to)

        self.press_key_1()  # Opens the osu map in the website using the osu menu
        pyperclip.copy("")  # Clear the clipboard content

        time.sleep(self.tab_loading_time)
        keyboard.press_and_release('ctrl+l')  # Highlight address bar
        time.sleep(self.time_to_sleep)

        keyboard.press_and_release('ctrl+c')  # Copy URL
        time.sleep(self.time_to_sleep)

        keyboard.press_and_release('ctrl+w')  # Close the tab
        time.sleep(self.time_to_sleep)

        if self.browser_to_minimize:
            windows = pyautogui.getWindowsWithTitle(self.browser_to_minimize)
            if windows:
                windows[0].minimize()

        windows = pyautogui.getWindowsWithTitle("osu!")
        if windows:
            windows[0].activate()

        if pyperclip.paste():
            print("Map ID found")
            self.map_id = pyperclip.paste()
            return self.map_id
        else:
            print("Failed to get beatmap ID\nTrying again...")
            self.start_hotkeys()

    def start_hotkeys(self):
        self.clear_screen()
        print(f"{self.hotkey.upper()} to start")
        print("F1 to change mods\n")
        print("Make sure osu is in focus and you have your browser open.")
        while True:
            if self.check_focus():
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'f1':
                        self.mods = self.mod_selection()
                        print(f"{self.hotkey.upper()} to start")
                        print("F1 to change mods\n")
                        print("Make sure osu is in focus and you have your browser open.")
                    elif event.name == 'f4':
                        print("Starting")
                        self.get_map_macro()
                        return self.mods

