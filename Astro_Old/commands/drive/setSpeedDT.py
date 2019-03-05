import math
import wpilib
#from robot import MyRobot
#from subsystems.Drive import Drive
import map
from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard
from wpilib.drive.differentialdrive import DifferentialDrive
class SetSpeedDT(TimedCommand):

    def __init__(self, timeout = 0):
        super().__init__('SetSpeedDT', timeoutInSeconds = timeout)
        self.robot = self.getRobot()
        self.requires(self.robot.drive)
        self.DT = self.robot.drive
        invert = True
        if invert == True:
            self.Joystick0 = self.robot.joystick1
            self.Joystick1 = self.robot.joystick0
        else:
            self.Joystick0 = self.robot.joystick0
            self.Joystick1 = self.robot.joystick1
        SmartDashboard.putNumber("gain",1)
        self.maxspeed = 1.00 #In addition to normal reducing factor in Drive.py
        self.diffDrive = DifferentialDrive(self.DT.left,self.DT.right)
        self.diffDrive.setName("Drive", "Differential Drive")
        self.diffDrive.setSafetyEnabled(False)

    def initialize(self):
        self.DT.setDirect()

    def execute(self):
        left = -self.Joystick0.getY()
        right = -self.Joystick1.getY()
        flip = self.DT.isFlipped()
# half-speed
        if self.robot.readDriverRightButton(map.halfSpeed):
            left = left / 2
            right = right / 2
        if (abs(left)<0.025) and (abs(right)<0.025):
            gain = SmartDashboard.getNumber("gain",1)
        else:
            if self.robot.readDriverRightButton(map.flip):
                self.DT.tankDrive (-right * self.maxspeed ,-left * self.maxspeed)
            else:
                self.DT.tankDrive(left * self.maxspeed ,right * self.maxspeed)
    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
