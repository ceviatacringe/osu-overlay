import pyautogui
import pyperclip
import requests


def scan_for_start(pixeladd: int, HR):
    # Get first circle position
    mapID = pyperclip.paste().split("beatmaps/")[1]
    response = (requests.get(f"https://osu.ppy.sh/osu/{mapID}").text).split("[HitObjects]")[1].split("\n")[1:-1]
    if HR:
        start_pos = (int(int(response[0].split(',')[0]) * 2.25 + 373), 1090-int(int(response[0].split(',')[1]) * 2.25 + 113))
    else:
        start_pos = (int(int(response[0].split(',')[0]) * 2.25 + 373), int(int(response[0].split(',')[1]) * 2.25 + 113))
    # Scan the first pixel and see it if changes, meaning that it appeared on screen
    # and the map started, now we can load the rest of the script with the right timing
    while True:
        # Sometimes the value isn't precisely 0,0,0 on restarts, so I need to add a threshhold of a few pixels
        # Adding the RGB together to see if it's close enough to black.
        scan = pyautogui.pixel(start_pos[0],start_pos[1])
        if scan[0]+scan[1]+scan[2] < pixeladd:
            #If the beatmap is loading
            while True:
                scan = pyautogui.pixel(start_pos[0],start_pos[1])
                if scan[0]+scan[1]+scan[2] > pixeladd:
                    #if the first circle appears
                    break
            break
