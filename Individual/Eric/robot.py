import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        #init motor controllers
        #init joysticks
        pass

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.drive.tankDrive(self.leftStick.getY(), self.rightStick.getY()) # I think this is how tank driving works, y-axis control on both joysticks


if __name__ == "__main__":
    wpilib.run(MyRobot)
