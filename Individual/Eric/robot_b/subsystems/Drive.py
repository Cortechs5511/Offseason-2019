# does the drivetrain stuff
import wpilib
from wpilib.command.subsystem import Subsystem
from commands.joystickdrive import joystickDrive
from wpilib.command import Command


class Drive(Subsystem):
    def __init__(self):
        super().__init__("Drive")
        Command.pageDrive = lambda x=0: self # I cannot believe that adding this made the whole thing work. Wow. That is pretty cool. Now onto finding a more efficient way of doing this.
        self.frontLeft = wpilib.Talon(0)
        self.rearLeft = wpilib.Talon(1)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)
        self.frontRight = wpilib.Talon(2)
        self.rearRight = wpilib.Talon(3)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

    def setSpeed(self, leftSpeed, rightSpeed):
        self.left.set(leftSpeed)
        self.right.set(rightSpeed)

    def initDefaultCommand(self):
        self.setDefaultCommand(joystickDrive())
