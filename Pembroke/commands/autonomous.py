from wpilib.command import CommandGroup

from commands.drive import driveStraightCombined
from commands.drive import driveStraightDistance
from commands.drive import turnAngle

from subsystems import HatchMech

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraight')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        self.addSequential(DriveStraightDistance(distance=90, timeout=100)) #just off hab platformclass LeftCargo(CommandGroup):

class Turn90(CommandGroup):
    def __init__(self):
        super().__init__('Turn90')
        TurnAngle = turnAngle.TurnAngle
        self.addSequential(TurnAngle(angle=90, timeout=20))

class LeftCargo(CommandGroup):
    def __init__(self):
        super().__init__('LeftCargo')
        TurnAngle = turnAngle.TurnAngle

        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=194.5, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=90, timeout=5))
        self.addSequential(DriveStraightCombined(distance=21.13, angle=90, timeout=5))
        self.addSequential(EjectHatch())

class DriveStraightSide(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraightSide')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined

        self.addSequential(DriveStraightCombined(distance=194, angle=0, timeout=10)) #just off hab platform


class RightCargo(CommandGroup):
    def __init__(self):
        super().__init__('RightCargo')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=194.5, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=-90, timeout=5))
        self.addSequential(DriveStraightCombined(distance=21.13, angle=-90, timeout=5))
        self.addSequential(EjectHatch())

class CenterCargo(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargo')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=173.25, angle=0, timeout=.75))
        self.addSequential(EjectHatch())

class LeftCargoLevel2(CommandGroup):
    def __init__(self):
        super().__init__('LeftCargoLevel2')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=271, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=90, timeout=5))
        self.addSequential(DriveStraightCombined(distance=5.6, angle=90, timeout=5))
        self.addSequential(EjectHatch())

class RightCargoLevel2(CommandGroup):
    def __init__(self):
        super().__init__('RightCargoLevel2')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=271, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=-90, timeout=5))
        self.addSequential(DriveStraightCombined(distance=17.6, angle=-90, timeout=5))
        self.addSequential(EjectHatch())

class CenterCargoLevel2Left(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargoLevel2Left')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=153.63, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=90, timeout=5))
        self.addSequential(DriveStraightCombined(distance=28.87, angle=90, timeout=5))
        self.addSequential(TurnAngle(angle=0, timeout=5))
        self.addSequential(DriveStraightCombined(distance=19.12, angle=0, timeout=5))
        self.addSequential(EjectHatch())

class CenterCargoLevel2Right(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargoLevel2Right')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=153.63, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=-90, timeout=5))
        self.addSequential(DriveStraightCombined(distance=28.87, angle=-90, timeout=5))
        self.addSequential(TurnAngle(angle=0, timeout=5))
        self.addSequential(DriveStraightCombined(distance=19.12, angle=0, timeout=5))
        self.addSequential(EjectHatch())
