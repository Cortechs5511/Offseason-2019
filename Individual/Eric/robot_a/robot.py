# not a command based robot
import wpilib
import wpilib.drive

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.frontLeft = wpilib.Talon(2)
        self.rearLeft = wpilib.Talon(3)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight = wpilib.Talon(0)
        self.rearRight = wpilib.Talon(1)
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        #self.drive = wpilib.TankDrive(self.left, self.right)
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def teleopInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        if self.timer.get() <= 0.1:
            self.left.set(0)
            self.right.set(0)
            pass
        elif self.timer.get() >= 6:
            self.left.set(0)
            self.right.set(0)
            pass
        elif self.timer.get() <= 0.45:
            self.left.set(0.85)
            self.right.set(0.85)
        else:
            self.left.set(1 / (float(2.54 * self.timer.get() ** 0.9999))) #This is a placeholder until I can figure out something better
            self.right.set(1 / (float(2.54 * self.timer.get() ** 0.9999)))

    def teleopPeriodic(self):
        leftInput = float(self.leftStick.getY()) * 0.9
        rightInput = float(self.rightStick.getY()) * 0.9
        #self.left.set(leftInput)
        #self.right.set(rightInput)
        if abs(leftInput) >= 0.05:
            self.left.set(leftInput)
        else:
            self.left.set(0)
        if abs(rightInput) >= 0.05:
            self.right.set(rightInput)
        else:
            self.right.set(0)

if __name__ == "__main__":
    wpilib.run(MyRobot)
