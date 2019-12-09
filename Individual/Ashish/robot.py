# timed robot
import wpilib
import math
from networktables import NetworkTables

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

        self.leftEncoder = wpilib.Encoder(8, 9)
        self.leftEncoder.setDistancePerPulse(1/2 * math.pi / 256)
        self.leftEncoder.setSamplesToAverage(10)

    def teleopPeriodic(self):
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

    def getDistance(self):


if __name__ == "__main__":
    wpilib.run(MyRobot)
