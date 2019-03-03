import navx
import wpilib
import ctre


class Sensors():
    def sensorsInit(self):
        self.navx = navx.AHRS.create_spi()

    def sensorsPeriodic(self):
        self.yaw = self.navx.getYaw()
        self.pitch = self.navx.getPitch()
        self.roll = self.navx.getRoll()
        #self.leftVal = self.leftEncoder.get()
        #self.rightVal = self.rightEncoder.get()

    def getPitch(self):
        return self.pitch

    def getRoll(self):
        return self.roll
