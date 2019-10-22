import wpilib
import ctre

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        self.frontLeft = wpilib.Talon(2)
        self.backLeft = wpilib.Talon(3)
        self.leftMotors = wpilib.SpeedControllerGroup(self.frontLeft, self.backLeft)

        self.frontRight = wpilib.Talon(0)
        self.backRight = wpilib.Talon(1)
        self.rightMotors = wpilib.SpeedControllerGroup(self.frontRight, self.backRight)

        self.leftJs = Joystick(0)
        self.rightJs = Joystick(1)
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        self.maxSpeed = .9
        if self.timer <= .1:
            self.leftMotors.set(0)
            self.rightMotors.set(0)
        elif self.timer > .1:
            self.leftMotors.set(maxSpeed)
            self.leftMotors.set(maxSpeed)
        elif self.timer >= 8:
            self.leftMotors.set(.4*maxSpeed)
            self.rightMotors.set(.4*maxSpeed)

    def teleopInit(self):
        self.timer.reset()
        self.timer.start()
    def teleopPeriodic(self):
        leftInput = float(self.leftJs.getY() * self.maxSpeed)
        rightInput = float(self.rightJs.getY() * self.maxSpeed)

        if abs(leftInput) >= .04:
            self.leftMotors.set(leftInput)
        else:
            self.leftMotors.set(0)
        if abs(rightInput) >= .04:
            self.rightMotors.set(rightInput)
        else:
            self.rightMotors.set(0)

if __name__ == "__main__":
    wpilib.run(MyRobot)
