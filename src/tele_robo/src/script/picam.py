#! /usr/bin/env python

from picamera import PiCamera
from trackingCamModule import ObjecOnImage
from tracking_motor_altitude_control import MotorControl
import time
import os,sys
from datetime import date, datetime
from fractions import Fraction
import copy

class CameraFunctions:

    def __init__(self):
        self.cam = PiCamera(resolution=(4056, 3040), framerate=Fraction(1, 6))
       
        self.frame_rate = 6
        self.shutter_speed = 10**5
        
        self.current_analog_gain = 12.0
        self.current_awb_mode = "off"
        self.drc = 'high'
        self.current_iso = 100

    def cameraCheck(self):
        try:
            self.cam.resolution = (600, 452)
        except:
            self.__init__()
            self.cam.resolution = (600, 452)

    def view(self):
        self.cameraCheck()
        self.cam.start_preview(fullscreen=False, window = (3, 120, 600, 452))
        self.cam.framerate = 30
       
    def trackingView(self):
        self.cameraCheck()
        self.cam.start_preview(fullscreen=False, window = (3, 120, 600, 452))
        self.cam.framerate = 30
        initMotorControl = MotorControl()
        initMotorControl.gpioPinSetup()
        while True:
            
            self.cam.capture('/home/pi/Documents/Tele_robo/src/tele_robo/foo.jpg')
            initImageAnalysis = ObjecOnImage('/home/pi/Documents/Tele_robo/src/tele_robo/foo.jpg')
            initImageAnalysis.readImage()
            initImageAnalysis.shape()
            initImageAnalysis.contour()
            self.cam.annotate_text_size = 20
            self.cam.annotate_text = str(initImageAnalysis.locationX)+","+str(initImageAnalysis.locationY)
            initMotorControl.tracking(int(initImageAnalysis.locationX),int(initImageAnalysis.locationY))

    def camControl(self,_iso,_shutter,_frames,_analogGain,_awbMode,_awbGain):
        self.cameraCheck()
        self.current_iso = copy.deepcopy(int(_iso))
        self.cam.iso = int(_iso)

        self.current_shutter_speed = copy.deepcopy(int(_shutter)*10**3)
        self.cam.shutter_speed = int(_shutter)*10**3

        self.current_frame_rate = copy.deepcopy(int(_frames))
        self.cam.framerate = int(_frames)

        self.current_analog_gain = copy.deepcopy(float(_analogGain))
        
        if _awbMode:
            self.current_awb_mode = copy.deepcopy('auto')
            self.cam.awb_mode = 'auto'
        else:
            self.current_awb_mode = copy.deepcopy('off')
            self.cam.awb_mode = 'off'

        self.current_awb_gain = copy.deepcopy(float(_awbGain)/10.0)
        self.cam.awb_gains = float(_awbGain)/10.0
        print("\n\n============>",self.cam.analog_gain)


    def closeView(self):
        self.cam.stop_preview()        

    def takePic(self):
        self.cam.start_preview()
        self.cam.resolution = (4056 ,3040)
        time.sleep(2)
        try:
            today= date.today()
            os.system('mkdir images/'+str(today.strftime("%d-%m-%Y")))
        except:
            pass
        self.cam.capture('images/'+str(today.strftime("%d-%m-%Y"))+"/single_random_"+str(int(time.time()))+'.jpg',format='jpeg',bayer=True)
        self.cam.stop_preview()
        

    def takePicCon(self,nI):
        for _ in range(int(nI)):
            self.takePic()
 

    def videoCapture(self):
        try:
            self.cam.close()
        except Exception as e:
            print(e)
        try:
            today= date.today()
            os.system('mkdir video/'+str(today.strftime("%d-%m-%Y")))
        except:
            pass
        os.system('raspivid -t 30000'+\
            ' -w 4056'+\
            ' -h 3040'+\
            ' -fps 25'+\
            ' -b 25000000'+\
            ' -o video/'+str(today.strftime("%d-%m-%Y"))+"/"+str(int(time.time()))+'.h264')

    