import wpilib
from wpilib import Encoder
from wpilib import SmartDashboard
from wpilib import TimedRobot

class MyRobot(TimedRobot):

    def robotInit(self):

        self.rightEncoder = wpilib.Encoder(0,1)
        self.leftEncoder = wpilib.Encoder(2,3)

    def robotPeriodic(self):

        SmartDashboard.putNumber("Right Count", self.rightEncoder.get())
        SmartDashboard.putNumber("Left Count", self.leftEncoder.get())
        SmartDashboard.putNumber("Right Distance", self.rightEncoder.getDistance())
        SmartDashboard.putNumber("Left Distance", self.leftEncoder.getDistance())
    
if __name__ == "__main__":
    wpilib.run(MyRobot)