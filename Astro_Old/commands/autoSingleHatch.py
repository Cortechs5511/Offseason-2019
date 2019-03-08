import wpilib
from wpilib.command import CommandGroup
from commands.drive import driveStraightDistance
from commands.drive import turnAngle
from commands.hatch import ejectHatch

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraight')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        self.addSequential(DriveStraightDistance(distance=212.8, timeout=15))

class LeftCargo(CommandGroup):
    def __init__(self):
        super().__init__('LeftCargo')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=212.8, timeout=15))
        self.addSequential(TurnAngle(angle=90, timeout=25))
        self.addSequential(DriveStraightDistance(distance=21.13, timeout=15))
        self.addSequential(EjectHatch())

class RightCargo(CommandGroup):
    def __init__(self):
        super().__init__('RightCargo')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=212.8, timeout=15))
        self.addSequential(TurnAngle(angle=-90, timeout=15))
        self.addSequential(DriveStraightDistance(distance=21.13, timeout=15))
        self.addSequential(EjectHatch())

class CenterCargo(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargo')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=173.25, timeout=15))
        self.addSequential(EjectHatch())

class LeftCargoLevel2(CommandGroup):
    def __init__(self):
        super().__init__('LeftCargoLevel2')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=271, timeout=15))
        self.addSequential(TurnAngle(angle=90, timeout=15))
        self.addSequential(DriveStraightDistance(distance=17.6, timeout=15))
        self.addSequential(EjectHatch())

class RightCargoLevel2(CommandGroup):
    def __init__(self):
        super().__init__('RightCargoLevel2')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=271, timeout=15))
        self.addSequential(TurnAngle(angle=-90, timeout=15))
        self.addSequential(DriveStraightDistance(distance=17.6, timeout=15))
        self.addSequential(EjectHatch())

class CenterCargoLevel2Left(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargoLevel2Left')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=153.63, timeout=15))
        self.addSequential(TurnAngle(angle=90, timeout=15))
        self.addSequential(DriveStraightDistance(distance=28.87, timeout=15))
        self.addSequential(TurnAngle(angle=0, timeout=15))
        self.addSequential(DriveStraightDistance(distance=19.12, timeout=1))
        self.addSequential(EjectHatch())

class CenterCargoLevel2Right(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargoLevel2Right')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = ejectHatch.EjectHatch
        self.addSequential(DriveStraightDistance(distance=153.63, timeout=15))
        self.addSequential(TurnAngle(angle=-90, timeout=15))
        self.addSequential(DriveStraightDistance(distance=28.87, timeout=15))
        self.addSequential(TurnAngle(angle=0, timeout=15))
        self.addSequential(DriveStraightDistance(distance=19.12, timeout=1))
        self.addSequential(EjectHatch())
