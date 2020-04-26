from pynput.mouse import Button, Controller as MouseControl
from pynput.keyboard import Key, Controller as KeyControl
from time import sleep as s

Mouse = MouseControl()
Keyboard = KeyControl()

holdKeyData = {
                'shift': Key.shift,
                'ctrl': Key.ctrl.value,
              }

def changeMousePos(x,y):
    ''' Moves the mouse to the x & y position given. '''
    Mouse.position = (x,y)

def moveMouse(x,y):
    ''' Moves the mouse x pixels right and y pixels down. '''
    Mouse.move(x,y)

def click(LorR, times):
    ''' Clicks the left mouse button. '''
    if LorR == 'l':
        b = Button.left
    else:
        b = Button.right
    Mouse.click(b, int(times))

def holdMouse():
    ''' Holds the left mouse button. '''
    Mouse.press(Button.right)

def releaseMouse():
    ''' Releases the left mouse button. '''
    Mouse.left(Button.left)

def scroll(amount):
    ''' Scrolls the mouse down based on the amount given. '''
    Mouse.scroll(0, int(amount))

def LclickAt(x,y):
    currx,curry = Mouse.position
    changeMousePos(x,y)
    click('l', 1)
    changeMousePos(currx,curry)
    s(2)


def doKey(letter):
    ''' Types the letter given. '''
    Keyboard.press(letter)
    Keyboard.release(letter)

def doText(text):
    for letter in text:
        doKey(letter)

def holdKey(key):
    Keyboard.press(holdKeyData[key])

def releaseKey(key):
    Keyboard.release(holdKeyData[key])
    



def gumtreeThing():
    # Clicking on Profile from main page
    LclickAt(1182, 158)
    # clicking on manage ads
    LclickAt(1105, 299)
    s(5)
    #scrolling to the edit button on the ad
    scroll(-50)
    s(5)
    print(Mouse.position)
    # clicking the edit ad button
    LclickAt(486.43359375, 655.91015625)
    s(5)
    # scrolling to the bottom of the page
    scroll(-20000)
    s(3)
    print(Mouse.position)
    #clicking save page
    LclickAt(157.8671875, 456.203125)
    


if __name__ == "__main__":
    s(3)
    gumtreeThing()
    print(Mouse.position)
    