import wpilib
import ctre

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)
