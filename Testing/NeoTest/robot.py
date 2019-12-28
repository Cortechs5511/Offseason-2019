import wpilib
from wpilib import SmartDashboard as sd
from wpilib import Spark
import rev
from rev import CANSparkMax

class MyRobot(wpilib.TimedRobot):
    """ Small program to verify Neo motor and encoder are working. """

    def robotInit(self):
        self.neo: CANSparkMax = CANSparkMax(3, rev.MotorType.kBrushless)
        self.neo.clearFaults()
        #self.neo: Spark = Spark(0)
        sd.putNumber("Neo Power", 0)
        self.neo.setOpenLoopRampRate(5)

    def teleopInit(self):
        self.neo.getEncoder().setPosition(0)

    def teleopPeriodic(self):
        sd.putNumber("Neo Encoder", self.neo.getEncoder().getPosition())
        self.neo.set(sd.getNumber("Neo Power", 0.5))
        self.neo.set(sd.getNumber("Neo Power", 0))

if __name__ == '__main__':
    wpilib.run(MyRobot)
