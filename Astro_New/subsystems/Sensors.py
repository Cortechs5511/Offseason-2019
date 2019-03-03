import navx
import wpilib
import ctre

class Sensors():
    def sensorsInit(self):
        self.navx = navx.AHRS.create_spi()
        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def sensorsPeriodic(self):
        self.yaw = self.navx.getYaw()
        self.pitch = self.navx.getPitch()
        self.roll = self.navx.getRoll()
        #self.leftVal = self.leftEncoder.get()
        #self.rightVal = self.rightEncoder.get()

    def getSensorPitch(self):
        return self.pitch

    def getSensorRoll(self):
        return self.roll
