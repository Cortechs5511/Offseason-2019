import wpilib
from wpilib.command import CommandGroup
from commands.drive import driveStraightDistance
from commands.drive import rotateAuton
from commands.hatch import ejectHatch

class AutoSingleHatch(CommandGroup):
    def __init__(self):
        super().__init__('AutoSingleHatch')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        RotateAuton = rotateAuton.autonRotation
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=212.8, timeout=15))
        self.addSequential(RotateAuton(angle=90, timeout=15))
        self.addSequential(DriveStraightDistance(distance=21.13, timeout=15))
        self.addSequential(EjectHatch())
