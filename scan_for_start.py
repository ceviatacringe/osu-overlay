import pyautogui
import pyperclip
import requests

def get_first_object_pos():
    # Get the location of the first hitcircle and translate it to screen x,y
    mapID = pyperclip.paste().split("beatmaps/")[1]
    response = (requests.get(f"https://osu.ppy.sh/osu/{mapID}").text).split("[HitObjects]")[1].split("\n")[1:-1]
    first_hit_coords = (int(int(response[0].split(',')[0]) * 2.25 + 373), int(int(response[0].split(',')[1]) * 2.25 + 113))
    return first_hit_coords

def scan_for_start():
    # Scan the first pixel and see it if changes, meaning that it appeared on screen
    # and the map started, now we can load the rest of the script with the right timing
    start_pos = get_first_object_pos()
    while True:
        if pyautogui.pixel(start_pos[0],start_pos[1]) == (0, 0, 0):
            #If the beatmap is loading
            while True:
                if pyautogui.pixel(start_pos[0],start_pos[1]) != (0, 0, 0):
                    #if the first circle appears
                    break
            break