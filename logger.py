'''
Key & Mouse Logger by Andrey Avramenko
Note: Doesn't work for Mac's "command" key or Windows' "windows" key


Codes for the log:
KEY_TYPED = 0
MOUSE_MOVE = 1
MOUSE_CLICK = 2
MOUSE_RELEASE = 3
MOUSE_SCROLL = 4
'''
import threading
import time, sys, json

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key

X_COORD = 0
Y_COORD = 1

ID = 0
CONTENT = 1
TIME_STAMP = 2

LATEST_ACTION = -1

KEY_TYPED = 0
MOUSE_MOVE = 1
MOUSE_CLICK = 2
MOUSE_SCROLL = 3

LEFT_BUTTON = 0
RIGHT_BUTTON = 1
MIDDLE_BUTTON = 2


actions = ['placeholder']
start_time = time.time()


# Write File Function
def writeFile():
    del actions[0]
    with open("log.andreyiscool", 'w') as f:
        json.dump(actions, f)




# Keyboard Functions
def key_onPress(key):
    # Threaded in key_thread

    # [KEY_TYPED, ['ukldsfjkdsj\n'], time]

    # Turning key into a usable string
    key = str(key).replace("'", '')
    print(key)

    # Turning space into a character
    if key == "Key.space": 
        key = ' '

    if key == "Key.enter":
        key = '\n' 
        print("working 1")
    
    # If the user pressed backspace
    if key == "Key.backspace":
        # Removing last character from latest action
        if actions[LATEST_ACTION][ID] == KEY_TYPED:
            # Example of prev_data: ['andreyiscool\nf']
            prev_data = actions[LATEST_ACTION][CONTENT]
            if len(prev_data) == 1:
                del actions[LATEST_ACTION]
            else:
                actions[LATEST_ACTION][CONTENT] = prev_data[:-1]
                actions[LATEST_ACTION][TIME_STAMP] = time.time()-start_time

    if "Key" not in key:
        print("working 2")
        # Merging data
        if actions[LATEST_ACTION][ID] == KEY_TYPED:
            actions[LATEST_ACTION][CONTENT] = actions[LATEST_ACTION][CONTENT] + key
        else:
            actions.append([KEY_TYPED, key, time.time()-start_time])
        print("{0} pressed".format(key))


def key_onRelease(key):
    ''' Turns the release of "escape" into a way to exit the program '''
    # Threaded in key_thread
    if key == Key.esc:
        writeFile()
        sys.exit()

        



# Mouse Functions
def onMove(x,y):
    command = (int(x/2)*2, int(y/2)*2)
    print(command)
    # Optimizing data by removing irrelevant actions
    if actions[LATEST_ACTION][ID] == MOUSE_MOVE:
        print("this is proccing 1")
        if actions[LATEST_ACTION][CONTENT] != command:
            print("this is proccing2")
            actions.append((MOUSE_MOVE, command, time.time()-start_time))
    else:
        actions.append((MOUSE_MOVE, command, time.time()-start_time))




def onClick(x, y, button, pressed):
    print(pressed)
    button = str(button)
    if button == "Button.middle": button = MIDDLE_BUTTON
    elif button == "Button.left": button = LEFT_BUTTON
    else: button = RIGHT_BUTTON

    actions.append((MOUSE_CLICK, ((int(x), int(y)), button, pressed), time.time()-start_time))
    
    print('{0} {1} at {2}'.format('Pressed' if pressed else 'Released', button, (x, y)))





def onScroll(x, y, dx, dy):
    # WTF WHY DOES IT ROUND TO INT?

    # if actions[LATEST_ACTION][ID] == MOUSE_SCROLL:
    #     prev_scro

    action = (dx, dy)
    actions.append((MOUSE_SCROLL, action, time.time()-start_time))












# Listener functions
def mouseListener():
    with MouseListener(on_move=onMove, on_click=onClick, on_scroll=onScroll) as l:
        l.join()

def keyboardListener():
    # Threaded in key_thread
    with KeyboardListener(on_press=key_onPress, on_release=key_onRelease) as listener:
        listener.join()



# Main Function
if __name__ == "__main__":
    mouse_thread = threading.Thread(target=mouseListener)
    key_thread = threading.Thread(target=keyboardListener)

    # Setting up daemon in mouse_thread to sys.exit() later
    mouse_thread.daemon = True

    # time.sleep(5)
    
    mouse_thread.start()
    key_thread.start()
