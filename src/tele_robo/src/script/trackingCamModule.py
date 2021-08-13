import cv2
import os
import matplotlib.pyplot as plt

class ObjecOnImage:

    def __init__(self,img):

        self.img = img
        self.rImg = None
        self.originX = 0
        self.originY = 0
        self.locationX = 0
        self.locationY = 0

    def readImage(self):
        self.rImg = cv2.imread(self.img)

    def shape(self):
        print(self.rImg.shape)
        w, h, channel = self.rImg.shape
        self.originX = int(h/2)
        self.originY = int(w/2)
        
    def contour(self):
        
        image2Gray = cv2.cvtColor(self.rImg, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(image2Gray, 120, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(
                                   image = thresh, 
                                   mode = cv2.RETR_TREE, 
                                   method = cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        try:
            cMax = contours[0]
            x, y, w, h = cv2.boundingRect(cMax)
            print(x,y)
            self.locationX = int(x+w/2) - self.originX 
            self.locationY = self.originY - int(y+h/2)
        except:
            pass
        # img_copy = self.rImg.copy()
        # img_box = cv2.rectangle(img_copy, (x, y), (x+w, y+h), color = (0, 255, 0), thickness = 5)
        # cv2.circle(img_copy, (self.originX,self.originY), 2, (0,255,0), 5)
        # cv2.imwrite('/home/pi/Documents/tele_ros/src/tele_robo/b.jpg',img_box)
        # print(self.locationX,self.locationY)
        
