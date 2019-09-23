import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.frontLeft = wpilib.Spark(1)
        self.midLeft = wpilib.Spark(2)
        self.rearLeft = wpilib.Spark(3)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.midLeft, self.rearLeft)

        self.frontRight = wpilib.Spark(4)
        self.midRight = wpilib.Spark(5)
        self.rearRight = wpilib.Spark(6)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.midRight, self.rearRight)

        self.drive = DifferentialDrive(self.left, self.right) # lines 8-18 are from documentation
        self.leftStick = wpilib.Joystick(1)
        self.rightStick = wpilib.Joystick(2)
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            self.drive.tankDrive(0.5, 0.5, True)  # Drive forwards at half speed
        elif self.leftStick.getY() == 0 and self.rightStick.getY() == 0: # using this in ideal situation with perfect joysticks
            self.drive.arcadeDrive(-1, 1)  # Turn left in circles at max speed (not very good)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.drive.tankDrive(self.leftStick.getY(), self.rightStick.getY()) # I think this is how tank driving works, y-axis control on both joysticks


if __name__ == "__main__":
    wpilib.run(MyRobot)
