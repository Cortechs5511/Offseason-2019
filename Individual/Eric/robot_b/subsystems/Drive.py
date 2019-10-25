# does the drivetrain stuff
import wpilib
from wpilib.smartdashboard import SmartDashboard
from wpilib.command.subsystem import Subsystem
from commands.joystickdrive import joystickDrive
from wpilib.command import Command
import math

class Drive(Subsystem):

    def __init__(self):
        super().__init__("Drive")
        Command.pageDrive = lambda x=0: self
        self.frontRight = wpilib.Talon(0)
        self.rearRight = wpilib.Talon(1)
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)
        self.frontLeft = wpilib.Talon(2)
        self.rearLeft = wpilib.Talon(3)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)
        self.leftEncoder = wpilib.Encoder(8, 9)
        self.leftEncoder.setDistancePerPulse(1/3 * math.pi / 256) # 4 inch wheels?
        self.leftEncoder.setSamplesToAverage(10)
        self.rightEncoder = wpilib.Encoder(8, 9)
        self.rightEncoder.setDistancePerPulse(1/3 * math.pi / 256) # 4 inch wheels?
        self.rightEncoder.setSamplesToAverage(10)
        #left = self.leftEncoder.getDistance()
        #SmartDashboard.putNumber("distance", left)

    def setSpeed(self, leftSpeed, rightSpeed):
        self.left.set(leftSpeed * 0.9)
        self.right.set(rightSpeed * 0.9)
        left = self.leftEncoder.getDistance()
        SmartDashboard.putNumber("distance", left)

    def getEncoders(self):
        left = self.leftEncoder.getDistance()
        #right = self.rightEncoder.getDistance()
        SmartDashboard.putNumber("distance", left)
        return left

    def initDefaultCommand(self):
        self.setDefaultCommand(joystickDrive())

    def periodic(self):
        self.getEncoders()
