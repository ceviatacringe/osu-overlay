import win32api
import win32con
import time
import keyboard


keyboard.wait('f4')

def press_1():
    win32api.keybd_event(0x31, 0, 0, 0)
    time.sleep(0.005)
    win32api.keybd_event(0x31, 0, win32con.KEYEVENTF_KEYUP, 0)

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    
press_1()