import time, json
from pprint import pprint

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

Mouse = MouseController()
Keyboard = KeyboardController()

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

def getData():
    with open("population.vfd") as f:
        return json.loads(f.read())


ACTION_TYPES = {
    0: typeText,
    1: setMousePosition,
    2: pressMouse,
    3: scroll,
}

def do():
    data = getData()

    CURR_TIME_PASSED = 0
    for command in data:
        # Waiting until activation time
        time.sleep(command[TIME_STAMP]-CURR_TIME_PASSED)
        # Executing corresponding command
        ACTION_TYPES[command[ID]](command[CONTENT])
        # Setting new activation time
        CURR_TIME_PASSED = command[TIME_STAMP]
    
if __name__ == "__main__":
    repeat = int(input("How often do you want the code to repeat (in hours) (enter as just a number)? "))*60*60
    print("Beginning repetition in 5 seconds. Press control+C in this window to exit the program.")
    time.sleep(5)
    
    while True:
        start_time = time.time()
        do()
        end_time = time.time()
        time.sleep(repeat-end_time+start_time)
        

