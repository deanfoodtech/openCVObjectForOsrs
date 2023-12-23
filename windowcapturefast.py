import cv2 as cv
import numpy as np
import pyautogui
from time import time
import win32api
import win32con, win32gui, win32ui

#when functions exit inside the class, we call it methods! the we need properties which are variebles inside this class
class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    #constructor = the first method that gets called when the class initailized
    def __init__(self, window_name=None):
        # find the handle for the window we want to capture
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        """# save the image as a bitmap file
        dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')"""
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        #drop the Alpha channel, or cv.mathTemplate() will throw an error
        img = np.ascontiguousarray(img)
        return img

    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

        """loop_time = time()
        while True:
            screenshot = get_screenshot(self)
            cv.imshow('Fast Vision', screenshot)

            print('FPS {}'.format(1/(time()-loop_time)))
            if cv.waitKey(1) == ord('q'):
                cv.destroyWindow()
                break"""
    """loop_time = time()
    while True:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)#opencv can only read np.array (it will be in RGB though)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        cv.imshow('Computer vision', screenshot)
    
        print('FPS {}'.format(1/(time()- loop_time)))
        loop_time = time()
        #press 'q' with the output window focused to exit
        #wait 1ms every loop to process the key pressed
        if cv.waitKey(1) == ord('q'):
            cv.destroyWindow()
            break
    """

    print('done')
    def list_window_name(self):
        def winEmumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEmumHandler(), None)