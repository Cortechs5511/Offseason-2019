# does the drivetrain stuff
import wpilib
from wpilib.command.subsystem import Subsystem
from commands.joystickdrive import joystickDrive
from wpilib.command import Command


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
        self.rightEncoder = wpilib.Encoder(0, 1) # these serve no purpose as of right now
        self.leftEncoder = wpilib.Encoder(2, 3) # must figure out lambda thing first

    def setSpeed(self, leftSpeed, rightSpeed):
        self.left.set(leftSpeed * 0.9)
        self.right.set(rightSpeed * 0.9)

    def getEncoders(self):
        right = self.rightEncoder.getDistance()
        left = self.leftEncoder.getDistance()
        return right, left

    def initDefaultCommand(self):
        self.setDefaultCommand(joystickDrive())
