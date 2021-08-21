#! /usr/bin/env python

import roslib
import rospy
from std_msgs.msg import String
import os,sys
import RPi.GPIO as GPIO
import time
from controller import SpeedController

class MotorControl:

    def __init__(self):
        

        self.PWM_INPUT_ALT = 2
        self.PIN_INPUT_ALT_1 = 3
        self.PIN_INPUT_ALT_2 = 14

        self.PWM_INPUT_HR = 17
        self.PIN_INPUT_HR_1 = 27
        self.PIN_INPUT_HR_2 = 15

        self.pulseWidthAlt = None
        self.pulseWidthHr = None
        self.stopAltMotor = True
        self.stopHRMotor = True

    def gpioPinSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.PWM_INPUT_HR,GPIO.OUT)
        GPIO.setup(self.PIN_INPUT_HR_1,GPIO.OUT)
        GPIO.setup(self.PIN_INPUT_HR_2,GPIO.OUT)

        GPIO.setup(self.PWM_INPUT_ALT,GPIO.OUT)
        GPIO.setup(self.PIN_INPUT_ALT_1,GPIO.OUT)
        GPIO.setup(self.PIN_INPUT_ALT_2,GPIO.OUT)

        


        self.pulseWidthAlt = GPIO.PWM(self.PWM_INPUT_ALT,100)
        self.pulseWidthHr = GPIO.PWM(self.PWM_INPUT_HR,100)
        self.pulseWidthAlt.start(0)
        self.pulseWidthHr.start(0)


    def motorControlSubscribe(self):
        altMotorSub = rospy.Subscriber('motor_control',String, self.callBack)
        rospy.spin()

    def directionMsgParse(self,msg):
        if msg == 'False':
            msg = 0
        else:
            msg = 1
        return msg

    def callBack(self,msg):
        rospy.loginfo(msg.data)
        msg_type = (msg.data).split('_')
        
        if msg_type[0] == 'altmotor':
            self.stopAltMotor = False
            time.sleep(2)
            rospy.loginfo("init"+(msg_type[1])+(msg_type[2]))
            self.altRun(int(msg_type[1]),self.directionMsgParse(msg_type[2]))
       
        elif msg_type[0] == 'hrmotor':
            self.stopHRMotor = False
            time.sleep(2)
            rospy.loginfo("init"+(msg_type[1])+(msg_type[2]))
            self.hrRun(int(msg_type[1]),self.directionMsgParse(msg_type[2]))
        
          
    def testMotor(self):
        for i in range(100):
            print(i)
            self.pulseWidthHr.ChangeDutyCycle(i)
            GPIO.output(self.PIN_INPUT_HR_1,GPIO.LOW)
            GPIO.output(self.PIN_INPUT_HR_2,GPIO.HIGH)
            time.sleep(1)

    def testMotorR(self):
        for i in range(100):
            print(i)
            self.pulseWidthHr.ChangeDutyCycle(i)
            GPIO.output(self.PIN_INPUT_HR_1,GPIO.HIGH)
            GPIO.output(self.PIN_INPUT_HR_2,GPIO.LOW)
            time.sleep(1)

    def altRun(self,speed,dirV):
        self.stopAltMotor = True
        speed = float(speed)/float(10)
        while self.stopAltMotor == True:
            print(speed)
            rospy.loginfo(str(speed))
            self.pulseWidthAlt.ChangeDutyCycle(speed)
            if dirV==1:
                rospy.loginfo("right")
                GPIO.output(self.PIN_INPUT_ALT_1,GPIO.HIGH)
                GPIO.output(self.PIN_INPUT_ALT_2,GPIO.LOW)
            else:
                rospy.loginfo("left")
                GPIO.output(self.PIN_INPUT_ALT_1,GPIO.LOW)
                GPIO.output(self.PIN_INPUT_ALT_2,GPIO.HIGH)

    def tracking(self,xIn,yIn):
        initSpeedController = SpeedController()
        speed = initSpeedController.motionControl(xIn,yIn)
        self.contHrRun(speed[0],speed[2])
        self.contAltRun(speed[1],speed[3])
        #time.sleep(1)

    def contHrRun(self,speed,dirV):
        speed = abs(float(speed)/float(10))
        rospy.loginfo(str(speed))
        self.pulseWidthHr.ChangeDutyCycle(speed)
        if dirV==1:
            rospy.loginfo("right")
            GPIO.output(self.PIN_INPUT_HR_1,GPIO.HIGH)
            GPIO.output(self.PIN_INPUT_HR_2,GPIO.LOW)
        else:
            rospy.loginfo("left")
            GPIO.output(self.PIN_INPUT_HR_1,GPIO.LOW)
            GPIO.output(self.PIN_INPUT_HR_2,GPIO.HIGH)
    

    def contAltRun(self,speed,dirV):
        speed = abs(float(speed)/float(100))
        rospy.loginfo(str(speed))
        self.pulseWidthAlt.ChangeDutyCycle(speed)
        if dirV==1:
            rospy.loginfo("right")
            GPIO.output(self.PIN_INPUT_ALT_1,GPIO.HIGH)
            GPIO.output(self.PIN_INPUT_ALT_2,GPIO.LOW)
        else:
            rospy.loginfo("left")
            GPIO.output(self.PIN_INPUT_ALT_1,GPIO.LOW)
            GPIO.output(self.PIN_INPUT_ALT_2,GPIO.HIGH)
        

    
    
    def hrRun(self,speed,dirV):
        self.stopHRMotor = True
        speed = float(speed)/float(100)
        while self.stopHRMotor == True:
            rospy.loginfo(str(speed))
            self.pulseWidthHr.ChangeDutyCycle(speed)
            if dirV==1:
                rospy.loginfo("right")
                GPIO.output(self.PIN_INPUT_HR_1,GPIO.HIGH)
                GPIO.output(self.PIN_INPUT_HR_2,GPIO.LOW)
            else:
                rospy.loginfo("left")
                GPIO.output(self.PIN_INPUT_HR_1,GPIO.LOW)
                GPIO.output(self.PIN_INPUT_HR_2,GPIO.HIGH)
    
if __name__ == '__main__':
    rospy.init_node('motor_control')
    try:
        allMotors = MotorControl()
        allMotors.gpioPinSetup()
        allMotors.motorControlSubscribe()
    except rospy.ROSInterruptException: pass



# x = MotorControl()
# x.gpioPinSetup()
# x.testMotor()
# x.testMotorR()

