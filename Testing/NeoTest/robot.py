import wpilib
from wpilib import SmartDashboard as sd
from wpilib import Spark
import rev
from rev import CANSparkMax

class MyRobot(wpilib.TimedRobot):
    """ Small program to verify Neo motor and encoder are working. """

    def robotInit(self):
        self.neo0: CANSparkMax = CANSparkMax(3, rev.MotorType.kBrushless)
        self.neo1: CANSparkMax = CANSparkMax(11, rev.MotorType.kBrushless)

        neos = wpilib.SpeedControllerGroup(self.neo0, self.neo1)

        self.neo0.clearFaults()
        self.neo1.clearFaults()

        sd.putNumber("Neo Power", 0)

        self.neo0.setOpenLoopRampRate(5)
        self.neo1.setOpenLoopRampRate(5)

    def teleopInit(self):
        self.neo0.getEncoder().setPosition(0)
        self.neo1.getEncoder().setPosition(0)

    def teleopPeriodic(self):
        sd.putNumber("Neo Encoder", self.neo0.getEncoder().getPosition())
        speed = sd.getNumber("Neo Power", 0)
        self.neo0.set(speed)
        self.neo1.set(speed)

if __name__ == '__main__':
    wpilib.run(MyRobot)
