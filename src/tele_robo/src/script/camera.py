#! /usr/bin/env python

import roslib
import rospy
import os,sys
import time
from std_msgs.msg import String
from picam import CameraFunctions
import re 

class Camera:

    def __init__(self):
        print("cam")
        self.initCam = CameraFunctions()

    def camControlSubscribe(self):
        camSub = rospy.Subscriber('cam_control',String, self.callBack)
        rospy.spin()

    def callBack(self,msg):
        rospy.loginfo(msg.data)
        msg_type = (msg.data).split('_')
        if msg_type[0] == 'cap':
            if(msg.data=='cap_p100'):
                self.preview()
            elif(msg.data=='cap_p400'):
                self.closePreview()
            elif(msg.data=='cap_p500'):
                self.trackView()
        elif (msg_type[0]=='cam-control'):
            _iso = msg_type[1]
            _shutter = msg_type[2]
            _frames = msg_type[3]
            _analogGain = msg_type[4]
            _awbMode = eval(msg_type[5])
            _awbGain = eval(msg_type[6])
            self.camControl(_iso,_shutter,_frames,_analogGain,_awbMode,_awbGain)
        elif msg_type[0]=='capture':
            if(msg_type[1]=='s101'):
                self.takePicture()
            elif(msg_type[1]=='s102'):
                numberOfImages = msg_type[2].split(':')[1]
                nameOfObject = msg_type[3].split(':')[1]
                self.takePictureContinue(numberOfImages,nameOfObject)
            elif(msg_type[1]=='s103'):
                self.videoCapture()

    def preview(self):
        self.initCam.view()

    def trackView(self):
        self.initCam.trackingView()
    
    def closePreview(self):
        self.initCam.closeView()

    def brightnessControl(self,valB):
        self.initCam.brightness(valB)
    
    def contrastControl(self,valC):
        self.initCam.contrast(valC)

    def isoControl(self,valI):
        self.initCam.iso(valI)

    def shutterControl(self,valS):
        self.initCam.shutterSpeed(valS)




    def camControl(self,v1,v2,v3,v4,v5,v6):
        self.initCam.camControl(v1,v2,v3,v4,v5,v6)

    def takePicture(self):
        self.initCam.takePic()

    def takePictureContinue(self,nImg,name):
        self.initCam.takePicCon(nImg,name)

    def videoCapture(self):
        self.initCam.videoCapture()


if __name__ == '__main__':
    rospy.init_node('primary_camera')
    try:
        cam = Camera()
        cam.camControlSubscribe()
    except rospy.ROSInterruptException: pass