import wpilib
import wpilib.drive

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.left = wpilib.Talon(12)
        #self.left2 = wpilib.Talon(13)
        self.right = wpilib.Talon(14)
        #self.right2 = wpilib.Talon(15)
        #self.left = wpilib.SpeedControllerGroup(self.left1, self.left2)
        #self.right = wpilib.SpeedControllerGroup(self.right1, self.right2)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.timer = wpilib.Timer()

    def teleopPeriodic(self):
        self.drive.tankDrive(self.leftStick.getY(), self.rightStick.getY())

if __name__ == "__main__":
    wpilib.run(MyRobot)
