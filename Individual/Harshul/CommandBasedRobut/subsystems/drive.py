from wpilib.command.subsystem import Subsystem
from wpilib import Talon
import subsystems
from commands.getPower import GetPower
import robotmap
from wpilib.smartdashboard import SmartDashboard as sd

class Drive(Subsystem):
    def __init__(self):
        self.frontLeft = Talon(robotmap.talons["frontLeft"])
        self.frontRight = Talon(robotmap.talons["frontRight"])
        self.backLeft = Talon(robotmap.talons["backLeft"])
        self.backRight = Talon(robotmap.talons["backRight"])
        #sd.putData("Drive", self)

    def setPower(self, leftPower, rightPower):
        self.frontLeft.set(leftPower)
        self.backLeft.set(leftPower)
        self.frontRight.set(rightPower)
        self.backRight.set(rightPower)
        print("lP", leftPower)
        print("lP", rightPower)

    def initDefaultCommand(self):
        sd.putString("Drive", "initDefault")
        self.setDefaultCommand(GetPower())
