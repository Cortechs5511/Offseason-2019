# timed robot
import wpilib
import math

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.frontRight = wpilib.Talon(0)
        self.rearRight = wpilib.Talon(1)
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        self.frontLeft = wpilib.Talon(2)
        self.rearLeft = wpilib.Talon(3)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.timer = wpilib.Timer()

        self.leftEncoder = wpilib.Encoder(0, 1)
        self.leftEncoder.setDistancePerPulse(1/2 * math.pi / 256)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(2, 3)
        self.rightEncoder.setDistancePerPulse(-1/2 * math.pi / 256)
        self.rightEncoder.setSamplesToAverage(10)

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        self.leftEncoder.getDistance()
        self.rightEncoder.getDistance()
        time = float(self.timer.get())
        if time <= 0.1:
            self.left.set(0)
            self.right.set(0)
            pass
        elif time >= 6:
            self.left.set(0)
            self.right.set(0)
            pass
        elif time <= 1:
            self.left.set((0.8)/(1+7*2**-(time*8)))
            self.right.set((0.8)/(1+7*2**-(time*8)))
        else:
            self.left.set((2)/(1+1.5**(time))) #This is a placeholder until I can figure out something better
            self.right.set((2)/(1+1.5**(time)))

    def teleopPeriodic(self):
        self.leftEncoder.getDistance()
        self.rightEncoder.getDistance()
        leftInput = float(self.leftStick.getY()) * 0.9
        rightInput = float(self.rightStick.getY()) * 0.9
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
