import wpilib
from wpilib import SmartDashboard as sd
from wpilib import Spark
import rev
from rev import CANSparkMax

class MyRobot(wpilib.TimedRobot):
    """ Small program to verify Neo motor and encoder are working. """

    def robotInit(self):
      #self.neo: CANSparkMax = CANSparkMax(5, rev.MotorType.kBrushless)
      self.neo: Spark = Spark(0)
      sd.putNumber("Neo Power", 0.5)

    def robotPeriodic(self):
      #sd.putNumber("Neo Encoder", self.neo.getEncoder().getPosition())
      pass
      
    def teleopPeriodic(self):
      self.neo.set(sd.getNumber("Neo Power", 0.5))

if  __name__ == '__main__':
    wpilib.run(MyRobot)
