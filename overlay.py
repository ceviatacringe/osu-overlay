import tkinter as tk
from pynput.mouse import Listener as MouseListener
import keyboard
import requests
import win32con
import win32gui
import win32api
import pyperclip
import os
from scan_for_start import scan_for_start

class OsuOverlay:
    def __init__(self, DT, HR):
        self.DT = DT
        self.HR = HR
        self.mouse_x, self.mouse_y = 0, 0
        self.circle_objects = {}
        self.canvas = None
        self.start_flag = False
        self.root = None
        self.listener = None
        self.is_closing = False
        self.scheduled_tasks = []
        self.circle_removal_delay = 400 # How fast the circle will disappear after appearing this gets changed by the AR scan automatically
        self.circle_size = 4
        
# Make a semi-transparent click-through window.
    def set_click_through(self, hwnd):
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_style = style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(99, 99, 99), 90, win32con.LWA_ALPHA)

# So that it doesn't minimize when osu is interacted with
    def keep_on_top(self):
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.scheduled_tasks.append(self.root.after(100, self.keep_on_top))

    def cancel_scheduled_tasks(self):
        while self.scheduled_tasks:
            task_id = self.scheduled_tasks.pop()
            self.root.after_cancel(task_id)

    def mouse_move(self, x, y):
        self.mouse_x, self.mouse_y = x, y

    def remove_circle(self, circle_id):
        if self.canvas:
            self.canvas.delete(circle_id)
            self.circle_objects.pop(circle_id, None)

    def draw_circle(self, x, y, object_type):
        if self.canvas:
            fill_color = 'green' if object_type == 'slider' else 'pink'
            circle_id = self.canvas.create_oval(x - self.circle_size, y - self.circle_size, x + self.circle_size, y + self.circle_size, fill=fill_color)
            self.circle_objects[circle_id] = {'x': x, 'y': y}
            self.scheduled_tasks.append(self.root.after(self.circle_removal_delay, lambda: self.remove_circle(circle_id)))

# Checks for mouse collision in order to remove circles that have been hit
    def check_interaction(self):
        to_remove = [circle_id for circle_id, info in self.circle_objects.items()
                     if ((self.mouse_x - info['x']) ** 2 + (self.mouse_y - info['y']) ** 2) ** 0.5 < 30]
        for circle_id in to_remove:
            self.remove_circle(circle_id)
        self.scheduled_tasks.append(self.root.after(10, self.check_interaction))

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_stats(self, text) -> int:
        sections = text.split('\n\n')
        for section in sections:
            if '[Difficulty]' in section:
                lines = section.split('\n')
                for line in lines:
                    # Get the circle size
                    if 'CircleSize:' in line:
                        # Osu pixel from CS formula -> Radius in pixels = 109 - (9*CS)
                        # This will be used in draw_circle to get an accurate size for each map
                        self.circle_size = int(109 - (9 * float(line.split(':')[1].strip())))
                    if 'ApproachRate:' in line:
                        # Extract and return the ApproachRate value
                        AR = float(line.split(':')[1].strip())
                        if self.HR:
                            AR = AR * 1.4
                            if AR > 10:
                                AR = 10
                        if AR < 5:
                            preempt = 1200 + 600 * (5 - AR) / 5
                        if AR == 5:
                            preempt = 1200
                        if AR > 5:
                            preempt = 1200 - 750 * (AR - 5) / 5
                        if self.DT:
                            preempt =  int(preempt*(2/3))
                        if preempt > 300:
                            return int(preempt)
                        else:
                            return(300)

# Parsing beatmap info into coords and delay and putting them into an array, gets displayed over time
# Gets the approach rate from beatmap info, modifies existing delay to the new accurate one.
    def load_circle_info(self):
        mapID = pyperclip.paste().split("beatmaps/")[1]
        response = requests.get(f"https://osu.ppy.sh/osu/{mapID}").text
        # Set the removal timing to the map approach rate
        self.circle_removal_delay = self.get_stats(response)
        circles_info = [(int(int(components[0]) * 2.25 + 384), int(int(components[1]) * 2.25 + 126), int(components[2]), 'slider' if len(components) > 6 else 'circle') for components in (line.split(',') for line in response.split("[HitObjects]")[1].split("\n")[1:-1]) if len(components) > 2]
        if circles_info:
            initial_delay = (circles_info[0][2])
            # If the map starts with a spinner the pixel scanning is delayed, this accounts for it
            if int(str(response.split("[HitObjects]")[1].split("\n")[1:-1][0]).count(",")) == 6:
                initial_delay += 70
            if self.DT and self.HR:
                circles_info = [(x, 1090-y, int(delay/1.5 - (initial_delay/1.5)), object_type) for x, y, delay, object_type in circles_info]
            elif self.DT:
                circles_info = [(x, y, int(delay/1.5 - (initial_delay/1.5)), object_type) for x, y, delay, object_type in circles_info]
            elif self.HR:
                circles_info = [(x, 1090-y, delay - initial_delay, object_type) for x, y, delay, object_type in circles_info]
            else:
                circles_info = [(x, y, delay - initial_delay, object_type) for x, y, delay, object_type in circles_info]
        return circles_info

# When the user restarts the map by holding "`"
    def reset_game(self):
        self.cancel_scheduled_tasks()
        self.start_flag = False
        self.circle_objects.clear()
        if self.canvas:
            self.canvas.delete("all")

    def start_sequence(self):
        self.clear_screen()
        print("Started")
        for x, y, delay, object_type in self.circles_info:
            self.scheduled_tasks.append(self.root.after(max(0, delay), lambda x=x, y=y, object_type=object_type: self.draw_circle(x, y, object_type)))

    def close_canvas(self):
        if self.root and not self.is_closing:
            self.is_closing = True
            self.cancel_scheduled_tasks()
            if self.canvas:
                self.canvas.delete("all")
            self.circle_objects.clear()
            if self.listener:
                self.listener.stop()
                self.listener = None
            def safely_close():
                if self.root:
                    self.root.quit()
                    self.root.destroy()
                    self.root = None
                self.is_closing = False
                self.start_flag = False
            self.root.after(0, safely_close)
        elif not self.root:
            self.is_closing = False
            self.start_flag = False

    def on_key_press(self, event):
        # Press enter to start the first hitobject scanning (this is also the hotkey to start a map in osu)
        # Automatic start. Will start at the wrong time if the user hovers over the initial position with their cursor in osu.
        if event.name == 'enter' and not self.start_flag and self.root:
            self.circles_info = self.load_circle_info()
            print("Scanning for first hitobject")
            scan_for_start(1, self.HR)
            self.start_flag = True
            self.start_sequence()
        elif event.name == '`' and self.root:
            self.reset_game()
            print("Resetting game")
            # Sometimes the map doesn't fully fade to black on resets, added pixel range to correct that
            scan_for_start(31, self.HR)
            print("Starting sequence")
            self.start_sequence()
        elif event.name == 'esc':
            if self.start_flag == True:
                print("Closing canvas and waiting for reinitialization")
            self.close_canvas()
            self.clear_screen()

    def initialize_script(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.root.update()

        self.set_click_through(win32gui.FindWindow(None, self.root.title()))
        self.keep_on_top()

        self.listener = MouseListener(on_move=self.mouse_move)
        self.listener.start()

        keyboard.on_press(self.on_key_press)
        self.check_interaction()
        self.root.mainloop()