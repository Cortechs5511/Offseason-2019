import navx
import wpilib
from wpilib import TimedRobot
class MyRobot(TimedRobot):
    def robotInit(self):
        self.sd = wpilib.SmartDashboard
        self.navx = navx.AHRS.create_spi()
    def robotPeriodic(self):
        self.sd.putNumber("Yaw",self.navx.getYaw())
        self.sd.putNumber("Pitch",self.navx.getPitch())
        self.sd.putNumber("Roll",self.navx.getRoll())
if __name__ == "__main__":
    wpilib.run(MyRobot)