from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from wpilib import SmartDashboard

from commands.drive.diffDrive import DiffDrive
from commands.drive.drivePath import DrivePath
from commands.drive.driveStraightCombined import DriveStraightCombined
from commands.drive.driveStraightDistance import DriveStraightDistance
from commands.drive.driveStraightTime import DriveStraightTime
from commands.drive.driveVision import DriveVision
from commands.drive.setFixedDT import SetFixedDT
from commands.drive.setSpeedDT import SetSpeedDT
from commands.drive.turnAngle import TurnAngle
from commands.hatch.ejectToggle import EjectToggle
import commands.sequences as seq

class TestPath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("TestPath")
        self.addSequential(DrivePath(name="Test", follower=follower, timeout=15))

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__("DriveStraight")
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))

def dashboardInit():
    pass

def dashboardPeriodic():
    pass



'''command to deliver hatch to front post'''
class AutoFrontHatch(CommandGroup):
    def __init__(self):
        super().__init__("AutoFrontHatch")
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))
        self.addSequential(WaitCommand(3))
        self.addSequential(EjectToggle())
        self.addSequential(WaitCommand(.5))

