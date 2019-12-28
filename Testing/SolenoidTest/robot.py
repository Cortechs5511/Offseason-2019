import wpilib
from wpilib import SmartDashboard as sd
from wpilib import Solenoid


class MyRobot(wpilib.TimedRobot):
    """ Small program to verify Neo motor and encoder are working. """

    def robotInit(self):
        self.solenoid = Solenoid(0,1)

    def teleopInit(self):
        self.solenoid.set(True)

if __name__ == '__main__':
    wpilib.run(MyRobot)
