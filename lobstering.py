import cv2 as cv
import pyautogui
import pytesseract
import random
import time
import thread as thread
import win32api
import win32con, win32gui, win32ui
from windowcapturefast import WindowCapture
from vision import Vision
from threading import Thread

wincap = WindowCapture('RuneLite - Da12kLorcl')
targetsgroup = random.choice([
    'shark1.png', 'shark2.png', 'shark3.png',
])
targets_appeared = Vision(targetsgroup)
found = targetsgroup
is_bot_in_action = False

kwbox =(1177, 548)
kwbox2 =(1274, 569)


def click_if_tree_in_box(treebox_left_top, treebox_right_bottom):
    # Capture the screen within the specified box
    screenshot = pyautogui.screenshot(region=(treebox_left_top[0], treebox_left_top[1], treebox_right_bottom[0] - treebox_left_top[0], treebox_right_bottom[1] - treebox_left_top[1]))

    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(screenshot).lower()
    print(extracted_text)
    # Check if "tree" appears in the extracted text
    return "hot" in extracted_text or "or" in extracted_text

def bot_actions(rectangles):
    if len(rectangles) > 0:
        targets = targets_appeared.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(target[0], target[1])
        if click_if_tree_in_box(kwbox, kwbox2):
            pyautogui.click()
            print('I found {}'.format(found))

        time.sleep(1)
    #let the main loop know this process is completed
    global is_bot_in_action
    #using glob because we don't want to create the local varieble!!! heck yeah
    is_bot_in_action = False

while True:

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # do the object detection
    rectangles = targets_appeared.find(screenshot,0.35)
    found = targetsgroup
    targetsgroup = random.choice([
        'shark1.png', 'shark2.png', 'shark3.png',
    ])
    #draw the detected results on the original img
    output_img = targets_appeared.draw_rectangles(screenshot, rectangles)

    #desplay the processed img
    cv.imshow('I see them', output_img)


    #take a bot action
    #run the funtion in the thread that separate form the main
    #so the code can continue while loop while bot performing actions
    if not is_bot_in_action:
        #to start a new thread if bot is not in action
        is_bot_in_action = True
        t = Thread(target = bot_actions, args=(rectangles,))
        t.start()

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    # loop_time = time()
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break