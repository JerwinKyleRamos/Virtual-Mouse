import pyautogui

#Move Cursor
def move_cursor(x, y):
    pyautogui.moveTo(x, y)



#Right Click
def right_click(x,y):
    pyautogui.click(button='right')

#Left Click
def left_click(x,y):
    pyautogui.click(button='left')