from wpilib.command import CommandGroup

from commands.drive import driveStraightCombined
from commands.drive import driveStraightDistance
from commands.drive import turnAngle
from commands.drive import setFixedDT

from subsystems import HatchMech

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraight')
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        self.addSequential(DriveStraightDistance(distance=90, timeout=100)) #just off hab platformclass LeftCargo(CommandGroup):

class LeftCargo(CommandGroup):
    def __init__(self):
        super().__init__('LeftCargo')
        TurnAngle = turnAngle.TurnAngle

        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        EjectHatch = HatchMech.EjectHatch
        SetFixedDT = setFixedDT.SetFixedDT

        self.addSequential(DriveStraightCombined(distance=50, angle=0, timeout=3.5, p=0.06, i=0, d=.336))
        self.addSequential(DriveStraightCombined(distance=144.5, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=90, timeout=2.5))
        self.addSequential(SetFixedDT(0.3,0.3, timeout=3))
        self.addSequential(EjectHatch())
        '''self.addSequential(SetFixedDT(-0.3,-0.3, timeout=1))
        self.addSequential(TurnAngle(angle=0, timeout=2.5))
        self.addSequential(SetFixedDT(-0.3,-0.3, timeout=3))'''

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
        SetFixedDT = setFixedDT.SetFixedDT

        self.addSequential(DriveStraightCombined(distance=50, angle=0, timeout=3.5, p=0.06, i=0, d=.336))
        self.addSequential(DriveStraightCombined(distance=144.5, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=-90, timeout=2.5))
        self.addSequential(SetFixedDT(0.3,0.3, timeout=3))
        self.addSequential(EjectHatch())

class CenterCargo(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargo')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        EjectHatch = HatchMech.EjectHatch

        self.addSequential(DriveStraightCombined(distance=138.25, angle=0, timeout=5))
        #self.addSequential(EjectHatch())

class CenterCargoPart2(CommandGroup):
    def __init__(self):
        super().__init__('CenterCargoPart2')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        EjectHatch = HatchMech.EjectHatch
        TurnAngle = turnAngle.TurnAngle
        SetFixedDT = setFixedDT.SetFixedDT

        self.addSequential(EjectHatch())
        self.addSequential(SetFixedDT(0,0, timeout=1))
        self.addSequential(SetFixedDT(-0.3,-0.3, timeout=2))
        '''self.addSequential(DriveStraightCombined(distance=-10, angle=0, timeout=.75))
        self.addSequential(TurnAngle(angle=60, timeout=2))
        self.addSequential(DriveStraightCombined(distance=-142.81, angle=0, timeout=5))
        self.addSequential(TurnAngle(angle=0, timeout=2))
        self.addSequential(DriveStraightCombined(distance=-10, angle=0, timeout=.75))'''

class AutoAlign(CommandGroup):
    def __init__(self,angle,dist1,dist2):
        super().__init__('autoAlign')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        self.addSequential(DriveStraightCombined(distance=dist1, angle=angle, timeout=5))
        self.addSequential(TurnAngle(angle=180, timeout=2.5))
        self.addSequential(DriveStraightCombined(distance=dist2, angle=180, timeout=5))

class StraightAlign(CommandGroup):
    def __init__(self,angle):
        super().__init__('autoAlign')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        self.addSequential(DriveStraightCombined(distance=70, angle=angle, timeout=5))
