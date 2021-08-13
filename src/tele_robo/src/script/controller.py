import time

class SpeedController:
    def __init__(self):
        self.gainX = 2.2
        self.gainY = 1.6

    def motionControl(self,currentLocX,currentLocY):
        speedY = 9.0 + float(currentLocY)/self.gainY
        speedX = 9.0 + float(currentLocX)/self.gainX
        print("Speed",speedX,speedY)
        dirX = 0; dirY = 0
        if speedX < 0:
            dirX = 1
        if speedY < 0:
            dirY = 1
        return [speedX*100,speedY*100,dirX,dirY]


# x = SpeedController()
# locX = 400
# locY = -360
# spEarth = 9.1
# while True:
#     sp = x.motionControl(locX,locY)
#     if abs(sp[0]) < 9.0:
#         sp[0] = 0
#     if abs(sp[1]) < 9.0:
#         sp[1] = 0
#     locX = (locX - sp[0]) + spEarth
#     locY = locY - sp [1] + spEarth
#     print (locX,locY)
#     time.sleep(1)
