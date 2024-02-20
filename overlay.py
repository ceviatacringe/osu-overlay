import tkinter as tk
from pynput.mouse import Listener as MouseListener
import keyboard
import requests
import win32con
import win32gui
import win32api

mouse_x, mouse_y = 0, 0
circle_objects = {}
canvas = None
start_flag = False
root = None
scheduled_tasks = []


#Define the canvas
def set_click_through(hwnd):
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    new_style = style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
    #The fourth int value represents the transparency of the window
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(99, 99, 99), 90, win32con.LWA_ALPHA)


def keep_on_top():
    root.lift()
    root.attributes('-topmost', True)
    scheduled_tasks.append(root.after(100, keep_on_top))


def cancel_scheduled_tasks():
    while scheduled_tasks:
        task_id = scheduled_tasks.pop()
        root.after_cancel(task_id)


def mouse_move(x, y):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y


def remove_circle(circle_id):
    if canvas:
        canvas.delete(circle_id)
        circle_objects.pop(circle_id, None)


def draw_circle(x, y, object_type):
    if canvas:
        fill_color = 'green' if object_type == 'slider' else 'pink'
        circle_id = canvas.create_oval(x - 50, y - 50, x + 50, y + 50, fill=fill_color)
        circle_objects[circle_id] = {'x': x, 'y': y}
        #The first int value represents the ms that the circle will disappear after appearing
        scheduled_tasks.append(root.after(400, lambda: remove_circle(circle_id)))


#Checks for cursor collision with the circles, making them disappear
def check_interaction():
    to_remove = [circle_id for circle_id, info in circle_objects.items()
                 if ((mouse_x - info['x']) ** 2 + (mouse_y - info['y']) ** 2) ** 0.5 < 30]
    for circle_id in to_remove:
        remove_circle(circle_id)
    scheduled_tasks.append(root.after(10, check_interaction))


#Parser for beatmap files -> getting hitobject locations and timings
def load_circle_info():
    response = requests.get("https://osu.ppy.sh/osu/1961270").text
    circles_info = [(int(int(components[0]) * 2.25 + 373),
                     int(int(components[1]) * 2.25 + 113),
                     int(components[2]),
                     'slider' if len(components) > 6 else 'circle')
                    for components in (line.split(',') for line in response.split("[HitObjects]")[1].split("\n")[1:-1])
                    if len(components) > 2]
    if circles_info:
        initial_delay = circles_info[0][2]
        circles_info = [(x, y, delay - initial_delay, object_type) for x, y, delay, object_type in circles_info][1:]
    return circles_info


def reset_game():
    cancel_scheduled_tasks()
    global start_flag
    start_flag = False
    circle_objects.clear()
    canvas.delete("all")


def start_sequence():
    global circles_info
    circles_info = load_circle_info()
    for x, y, delay, object_type in circles_info:
        scheduled_tasks.append(root.after(max(0, delay), lambda x=x, y=y: draw_circle(x, y, object_type)))


def close_canvas():
    if root:
        cancel_scheduled_tasks()
        root.destroy()
    global start_flag
    start_flag = False
    circle_objects.clear()


def on_key_press(event):
    global start_flag
    if event.name in ['w', 'e'] and not start_flag and root:
        print("Starting sequence")
        start_flag = True
        start_sequence()
    elif event.name == '`' and root:
        print("Resetting game")
        reset_game()
    elif event.name == 'esc':
        print("Closing canvas and waiting for reinitialization")
        close_canvas()



def initialize_script():
    global root, canvas
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    root.update()

    set_click_through(win32gui.FindWindow(None, root.title()))
    keep_on_top()

    listener = MouseListener(on_move=mouse_move)
    listener.start()

    keyboard.on_press(on_key_press)
    check_interaction()
    root.mainloop()
