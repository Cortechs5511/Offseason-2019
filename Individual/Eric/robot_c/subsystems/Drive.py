# does the drivetrain stuff
import wpilib
import ctre
from wpilib.command.subsystem import Subsystem
from commands.joystickdrive import joystickDrive
from wpilib.command import Command
import oi
import math

class Drive(Subsystem):

    def __init__(self):
        super().__init__("Drive")
        Command.pageDrive = lambda x=0: self

        self.left1 = ctre.WPI_TalonSRX(10)
        self.left2 = ctre.WPI_VictorSPX(11)
        self.left3 = ctre.WPI_VictorSPX(12)
        self.right1 = ctre.WPI_TalonSRX(20)
        self.right2 = ctre.WPI_VictorSPX(21)
        self.right3 = ctre.WPI_VictorSPX(22)

        self.left2.follow(self.left1)
        self.left3.follow(self.left1)
        self.right2.follow(self.right1)
        self.right3.follow(self.right1)

        self.leftEncoder = wpilib.Encoder(0, 1)
        self.leftEncoder.setDistancePerPulse(1/3 * math.pi / 256) # 4 inch wheels?
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(2, 3)
        self.rightEncoder.setDistancePerPulse(-1/3 * math.pi / 256)
        self.rightEncoder.setSamplesToAverage(10)

    def getEncoders(self):
        left = self.leftEncoder.getDistance()
        right = self.rightEncoder.getDistance()
        return [left, right]

    def setSpeed(self, leftSpeed, rightSpeed):
        leftOutput = 0.04 + (abs(leftSpeed) ** 1.5) * 0.86
        rightOutput = 0.04 + (abs(rightSpeed) ** 1.5) * 0.86
        if leftSpeed < 0:
            leftOutput = -leftOutput
        if rightSpeed < 0:
            rightOutput = -rightOutput
        if abs(leftSpeed) <= 0.05:
            leftOutput = 0
        if abs(rightSpeed) <= 0.05:
            rightOutput = 0

        if oi.halfSpeedButton() == True:
            speedMult = 0.5
        else:
            speedMult = 1

        if oi.flipButton() == True:
            speedMult = -speedMult

        if abs(leftSpeed) <= 0.05:
            leftOutput = 0
        if abs(rightSpeed) <= 0.05:
            rightOutput = 0

        self.left1.set(-leftOutput * float(speedMult))
        self.right1.set(-rightOutput * float(speedMult))

    def initDefaultCommand(self):
        self.setDefaultCommand(joystickDrive())
