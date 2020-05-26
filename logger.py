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

file_name = 'default.vfd'


# Write File Function
def writeFile():
    '''Writes the actions made by the user to a file. In main thread.'''
    del actions[0]
    print('Writing File...')
    with open(file_name, 'w') as f:
        # Putting the actions into the file as a json file
        json.dump(actions, f)
    print("Done!")




# Keyboard Functions
def key_onPress(key):
    '''Triggering off the press of a key, logs that key. In Key Thread.'''
    # Threaded in key_thread

    # [KEY_TYPED, ['ukldsfjkdsj\n'], time]

    # Turning key into a usable string
    key = str(key).replace("'", '')

    # Turning space into a character
    if key == "Key.space": 
        key = ' '

    if key == "Key.enter":
        key = '\n' 
    
    # If the user pressed backspace, removing last letter
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
        # Merging data
        if actions[LATEST_ACTION][ID] == KEY_TYPED:
            actions[LATEST_ACTION][CONTENT] = actions[LATEST_ACTION][CONTENT] + key
        else:
            actions.append([KEY_TYPED, key, time.time()-start_time])




def key_onRelease(key):
    '''Triggering off the press of a key, exits the program on escape. In Key Thread.'''
    if key == Key.esc:
        print("ESC key pressed. Actions no longer logged.")
        writeFile()
        print("Terminating program.")
        sys.exit()

        



# Mouse Functions
def onMove(x,y):
    '''Triggering off the movement of the mouse, logs it to actions. In Mouse Thread'''
    # Generalising data for better storage
    command = (int(x/2)*2, int(y/2)*2)
    # Optimizing data by removing irrelevant actions
    if actions[LATEST_ACTION][ID] == MOUSE_MOVE:
        if actions[LATEST_ACTION][CONTENT] != command:
            actions.append((MOUSE_MOVE, command, time.time()-start_time))
    else:
        actions.append((MOUSE_MOVE, command, time.time()-start_time))




def onClick(x, y, button, pressed):
    '''Triggering off the clicking and release of the mouse, logs it to actions. In Mouse Thread'''
    button = str(button)
    if button == "Button.middle": button = MIDDLE_BUTTON
    elif button == "Button.left": button = LEFT_BUTTON
    else: button = RIGHT_BUTTON

    actions.append((MOUSE_CLICK, ((int(x), int(y)), button, pressed), time.time()-start_time))



def onScroll(x, y, dx, dy):
    '''
    Triggering off the clicking and release of the mouse, logs it to actions. In Mouse Thread. 
    Not recommended for use, as it is buggy.
    '''
    action = (dx, dy)
    actions.append((MOUSE_SCROLL, action, time.time()-start_time))




# Listener functions
def mouseListener():
    '''Distributes all mouse actions in the Mouse Thread'''
    with MouseListener(on_move=onMove, on_click=onClick, on_scroll=onScroll) as l:
        l.join()

def keyboardListener():
    '''Distributes all keyboard actions in the Key Thread'''
    with KeyboardListener(on_press=key_onPress, on_release=key_onRelease) as listener:
        listener.join()



# Main Function
if __name__ == "__main__":
    # Creating 2 new threads
    mouse_thread = threading.Thread(target=mouseListener)
    key_thread = threading.Thread(target=keyboardListener)

    file_name = input("Name the sequence you would like to create (alphanumeric characters): ").replace(' ','_') + '.vfd'

    # Setting up daemon in mouse_thread to sys.exit() later
    mouse_thread.daemon = True
    print("You have 5 seconds to navigate before tracking begins.")
    print("Press ESC to terminate the program.")
    print("Scrolling is not recommended.")
    time.sleep(5)
    print("Beginning the logging of actions.")
    
    mouse_thread.start()
    key_thread.start()
