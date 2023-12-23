import cv2
import cv2 as cv
import numpy as np

class Vision():#the object is in the  init function only need momsterpath in this class
    #declair our property variebles
    tree_img = None
    tree_w = 0
    tree_h = 0
    method = None
    #constructor
    def __init__(self, monster_path, method=cv.TM_CCOEFF_NORMED):
        self.tree_img = cv.imread(monster_path, cv.IMREAD_UNCHANGED)#this is the object created by the vision class
        self.tree_w = self.tree_img.shape[1]
        self.tree_h = self.tree_img.shape[0]
        self.method = method

    def find(self, forest_img, threshold=0.3, debug_mode=None):
        #read the file using opencv

        #converting all picture to cv-readable format
        # tree_imgs = []
        # for png in ['tree1.png', 'tree2.png', 'tree3.png']:
        #     tree_imgs.append(cv.imread(png, cv.IMREAD_UNCHANGED))
        # Read the images
        #target is gray now let's change the forest

        # Convert images to grayscale
        #forest_img = cv2.cvtColor(forest_img, cv2.COLOR_BGR2GRAY)
        #matching -- run opencv algorithm
        result = cv.matchTemplate(forest_img, self.tree_img, self.method)

        locations = np.where(result >=threshold)
        #print(locations)#will return array of y1,y2,y3... and array of x1,x2,x3...
        #The first arrayrepresents the row indices (y-coordinates) of values result >=threshold.
        #to turn them to tuples (x,y)
        locations = list(zip(*locations[::-1]))#in order for zip()to work, location had to be reversed
        # print(locations)
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.tree_w, self.tree_h]
            rectangles.append(rect)
            rectangles.append(rect)
        # a rect is a list contains 4 int indicating the location topleft loc,w and h
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5) #atleast 1 rect exist to form a group and 0.5 is the distance limit

        return rectangles

    def get_click_points(self, rectangles):
        points = []
        for x,y,w,h in rectangles:
            """        #determine the center of box position
            top_left = (x,y)
            bottome_right = (x+w, y+h)
            #draw a box
            cv.rectangle(forest_img1, top_left, bottome_right, line_color, line_type)"""
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            #save points
            points.append((center_x,center_y))

        return points

    def draw_rectangles(self, forest_img, rectangles):
        line_color = (0, 0, 255)
        line_type = cv.LINE_4
        for (x,y,w,h) in rectangles:
            #determine box position
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw a box
            cv.rectangle(forest_img, top_left, bottom_right, line_color, line_type)
        #instead of imshow, we return the canvas image
        return forest_img
        #given a list [x,y] and a canvas image to draw on
        #find the center of the box to provide the cross loc
    def draw_crossmark(self, forest_img, points):
        #these are BGR
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS
        for (center_x, center_y) in points:
            #draw at center
            cv.drawMarker(forest_img, (center_x,center_y), marker_color, marker_type)
        return forest_img

#to see if this fuction works
# points = findTheTarget('tree1.png', 'forest.png', threshold=0.3,debug_mode='points')