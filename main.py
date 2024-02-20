import tkinter as tk
from pynput.mouse import Listener as MouseListener
import keyboard
import requests
import win32con
import win32gui
import win32api

# Global variables
mouse_x, mouse_y = 0, 0
circle_objects = {}
canvas = None
start_flag = False

# Fetch and parse circle information from the API
response = requests.get("https://osu.ppy.sh/osu/1961270").text
circles_info = [(int(int(components[0]) * 2.25 + 373),
                 int(int(components[1]) * 2.25 + 113),
                 int(components[2]),
                 'slider' if len(components) > 6 else 'circle')
                for components in (line.split(',') for line in response.split("[HitObjects]")[1].split("\n")[1:-1])
                if len(components) > 2]

# Adjust circle timings and remove the first circle if not needed
if circles_info:
    initial_delay = circles_info[0][2]
    circles_info = [(x, y, delay - initial_delay, object_type) for x, y, delay, object_type in circles_info][1:]

#Make the transparent click-through window
def set_click_through(hwnd):
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(99, 99, 99), 90, win32con.LWA_ALPHA)

#Keep the window on top so it can be interacted through while displaying
def keep_on_top(root):
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: keep_on_top(root))

def mouse_move(x, y):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

def remove_circle(circle_id, root):
    global canvas
    if canvas:
        canvas.delete(circle_id)
        circle_objects.pop(circle_id, None)

def draw_circle(x, y, root, object_type):
    global canvas
    if canvas:
        fill_color = 'green' if object_type == 'slider' else 'pink'
        circle_id = canvas.create_oval(x - 50, y - 50, x + 70, y + 70, fill=fill_color)
        circle_objects[circle_id] = {'x': x, 'y': y}
        #The int value represents the ms that a circle is displayed for before expiring if not clicked
        root.after(400, lambda: remove_circle(circle_id, root))

#Check for mouse collision to remove hovered circles
def check_interaction(root):
    global circle_objects, mouse_x, mouse_y
    to_remove = [circle_id for circle_id, info in circle_objects.items()
                 if ((mouse_x - info['x']) ** 2 + (mouse_y - info['y']) ** 2) ** 0.5 < 50]
    for circle_id in to_remove:
        remove_circle(circle_id, root)
    root.after(10, lambda: check_interaction(root))

def start_sequence(root):
    global start_flag, circles_info
    if not start_flag:
        start_flag = True
        for x, y, delay, object_type in circles_info:
            root.after(max(0, delay), lambda x=x, y=y, root=root, object_type=object_type: draw_circle(x, y, root, object_type))

#Press W or E to start the circle display once ready.
def on_key_press(event, root):
    global start_flag
    if event.name in ['w', 'e'] and not start_flag:
        print("Starting sequence")
        start_sequence(root)

def create_overlay():
    global canvas, start_flag
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    root.update()

    set_click_through(win32gui.FindWindow(None, root.title()))
    keep_on_top(root)

    with MouseListener(on_move=mouse_move) as listener:
        keyboard.on_press(lambda event: on_key_press(event, root))
        check_interaction(root)
        root.mainloop()

if __name__ == "__main__":
    create_overlay()
