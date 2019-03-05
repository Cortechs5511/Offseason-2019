from navx.ahrs import AHRS as NavX
import wpilib
import ctre

class Sensors():
    def sensorsInit(self):
        #self.navx = NavX.create_i2c()
        #self.navx = None
        #self.yaw = 0
        pass

    def sensorsPeriodic(self):
        #self.yaw = self.navx.getYaw()
        #self.leftVal = self.leftEncoder.get()
        #self.rightVal = self.rightEncoder.get()
        pass

'''Sensors need to be in the subsystem that they belong in
    For example: self.pitch and self.roll were moved into Climber.py
    self.yaw should be moved into Drive.py, as well as the encoders
    In the end, there should be no Sensors.py as a subsystem'''
