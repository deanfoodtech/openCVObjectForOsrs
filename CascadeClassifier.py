import cv2 as cv
import numpy as np
import os
from time import time
from windowcapturefast import WindowCapture

#initialize the windowcapture class
wincap = WindowCapture('RuneLite - Da12kLorcl')

loop_time = time()
while True:
    #get an update image of the game
    screenshot = wincap.get_screenshot()
    #display the image
    cv.imshow('unprocessed', screenshot)

    #debug the loop rate
    print('FPS {}'.format(1/(time()-loop_time)))
    loop_time = time()

    #wait 1ms everyloop to process the keypress
    key = cv.waitKey(1)
    if key == ord('q'):
        #listening to q press to close
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.png'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.png'.format(loop_time), screenshot)
print("done")


