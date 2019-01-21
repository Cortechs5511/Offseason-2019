from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from wpilib import SmartDashboard

from commands.DriveStraightCombined import DriveStraightCombined
from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightTime import DriveStraightTime
from commands.DrivePath import DrivePath
from commands.TurnAngle import TurnAngle

from commands.setFixedDT import setFixedDT

import commands.Sequences as seq
#PATHFINDER AUTOS

class TestPath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("TestPath")
        self.addSequential(DrivePath(name="Test", follower=follower, timeout=15))

'''STANDARD AUTOS'''

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__("DriveStraight")
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))

def UpdateDashboard():
    follower = "PathFinder"
