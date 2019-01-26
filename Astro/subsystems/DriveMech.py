import math
import ctre
import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
from wpilib import SmartDashboard as sd

from sim import simComms


class FlipButton(Command):
    def __init__(self):
        super().__init__('Flip')
        robot = self.getRobot()
        self.driveMechanism = robot.driveMechanism
        
    def initialize(self):
        pass

    def execute(self):
        
        if self.driveMechanism.flipped:
            self.driveMechanism.flipped = True
        else:
            self.driveMechanism.flipped = False 
    def interrupted(self):
        self.end()

    def end(self):
        pass
      #  self.driveMechanism.stopDrive()

    def isFinished(self):
        return True 

class HumanDrive(Command):
    def __init__(self):
        super().__init__('driveMechanism')
        robot = self.getRobot()
        self.driveMechanism = robot.driveMechanism
        self.requires(self.driveMechanism)



    def initialize(self):
        pass

    def execute(self):
        pass
        self.driveMechanism.drive()

    def interrupted(self):
        self.end()

    def end(self):
        self.driveMechanism.stopDrive()

    def isFinished(self):
        return False

class DriveMechanism(Subsystem):

    def __init__(self, Robot):
      
        """ Create all physical parts used by subsystem. """
        super().__init__('Drive')
        # Set to true for extra info to smart dashboard
        self.debug = True
        self.flipped = False

    def driveInit(self):
        self.driveLeft1 = wpilib.TalonSRX()
        self.driveLeft2 = wpilib.VictorSP()
        self.driveLeft3 = wpilib.VictorSP()
        self.leftEncoder = wpilib.Encoder(0,1)
        self.rightEncoder = wpilib.Encoder(2,3)
        self.driveRight1 = wpilib.TalonSRX()
        self.driveRight2 = wpilib.VictorSP()
        self.driveRight3 = wpilib.VictorSP()
        self.driveLeft2.follow(self.driveLeft2)
        self.driveLeft3.follow(self.driveLeft3)
        self.rightLeft2.follow(self.driveRight1)
        self.rightLeft3.follow(self.driveRight1)
        self.leftDriveController = wpilib.Joystick()
        self.rightDriveController = wpilib.Joystick()

    def drive(self, leftSpeed, rightSpeed):
        self.driveLeft1.set(leftSpeed)
        self.driveRight1.set(rightSpeed)
    
    def stopDrive(self):

        self.driveLeft1 = 0 
        self.driveRight1 = 0
     

    def disable(self):
        """ Disables subsystem and puts everything back to starting position. """
        self.stopDrive()

    def updateDashboard(self):
        """ Put diagnostics out to smart dashboard. """
        SmartDashboard.putBoolean("Driving Reverse", self.flipped)

    def subsystemInit(self):
        """ Adds subsystem specific commands. """
        if self.debug:
            SmartDashboard.putData("Flipped_drive", FlipButton())
     




