import time, json, ctypes
from pprint import pprint

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

Mouse = MouseController()
Keyboard = KeyboardController()

PROCESS_PER_MONITOR_DPI_AWARE = 2

ID = 0
CONTENT = 1
TIME_STAMP = 2

MOUSE_CLICKS = {
    0: Button.left, 
    1: Button.right, 
    2: Button.middle,
}

def setMousePosition(data):
    # KEY: 1
    # It's kinda self explanatory
    coordinates = tuple(data)
    Mouse.position = coordinates


def pressMouse(data):
    coords, button_key, press = data 
    button = MOUSE_CLICKS[button_key]
    setMousePosition(coords)
    if press == True:
        Mouse.press(button)
    else:
        Mouse.release(button)


def scroll(data):
    scroll_x, scroll_y = data
    Mouse.scroll(scroll_x, scroll_y)


def typeText(data):
    Keyboard.type(data)

def getData(file_name):
    with open(file_name) as f:
        return json.loads(f.read())


ACTION_TYPES = {
    0: typeText,
    1: setMousePosition,
    2: pressMouse,
    3: scroll,
}

def do(data):
    CURR_TIME_PASSED = 0
    for command in data:
        # Waiting until activation time
        time.sleep(command[TIME_STAMP]-CURR_TIME_PASSED)
        # Executing corresponding command
        ACTION_TYPES[command[ID]](command[CONTENT])
        # Setting new activation time
        CURR_TIME_PASSED = command[TIME_STAMP]
    

def getNextTime(time_until_next):
    curr_time = time.strftime('%H:%M:%S')

    hrs, mins, secs = [int(i) for i in curr_time.split(':')]
    secs += int(time_until_next)

    mins += int(secs/60)
    secs = secs%60
    hrs += int(mins/60)
    mins = mins%60
    hrs = hrs%24

    return str(hrs)+':'+str(mins)+':'+str(secs)




if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

    file_name = input("What sequence do you want to run (without the .vfd)? ").replace(' ','_') + '.vfd'
    repeat = int(input("How often do you want the code to repeat (in hours) (enter as just a number)? "))*60*60
    print("Beginning repetition in 5 seconds. Press control+C in this window to exit the program.")
    time.sleep(5)

    data = getData(file_name)
    
    while True:
        start_time = time.time()

        print("Beginning action sequence at", time.strftime('%H:%M:%S'))
        do(data)
        print("Finishing action sequence at", time.strftime('%H:%M:%S'))

        end_time = time.time()
        time_until_next = repeat-end_time + start_time
        next_seq_time = getNextTime(time_until_next)

        print("Running next sequence at", next_seq_time)
        time.sleep(repeat-end_time+start_time)
        

