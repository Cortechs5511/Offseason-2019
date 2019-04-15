from wpilib.command import CommandGroup

from commands.drive import driveStraightCombined
from commands.drive import driveStraightDistance
from commands.drive import turnAngle
from wpilib.command import Command
from commands.drive import setFixedDT
from wpilib import SmartDashboard

from subsystems import HatchMech

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraight')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        DriveStraightDistance = driveStraightDistance.DriveStraightDistance
        self.addSequential(DriveStraightCombined(distance=30, timeout=100)) #just off hab platformclass LeftCargo(CommandGroup):

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
    def __init__(self,angle,dist1,dist2,angle0):
        super().__init__('autoAlign')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        if angle0 != 1000:
            self.addSequential(TurnAngle(angle=angle0, timeout=2.5))
            self.addSequential(DriveStraightCombined(distance=dist1, angle=angle0, timeout=5))
            self.addSequential(TurnAngle(angle=0, timeout=2.5))
            self.addSequential(DriveStraightCombined(distance=dist2, angle=0, timeout=5))
        elif dist2 == 1000:
            self.addSequential(DriveStraightCombined(distance=dist1, angle=angle, timeout=5))
        else:
            self.addSequential(DriveStraightCombined(distance=dist1, angle=angle, timeout=5))
            self.addSequential(TurnAngle(angle=0, timeout=2.5))
            self.addSequential(DriveStraightCombined(distance=dist2, angle=0, timeout=5))

class StraightAlign(CommandGroup):
    def __init__(self,angle):
        super().__init__('autoAlign')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        self.addSequential(DriveStraightCombined(distance=70, angle=angle, timeout=5))

class AutoAlignTuning(CommandGroup):
    def __init__(self,angle,dist1,dist2,angle0):
        super().__init__('autoAlignTuning')
        DriveStraightCombined = driveStraightCombined.DriveStraightCombined
        TurnAngle = turnAngle.TurnAngle
        self.addSequential(DriveStraightCombined(distance=30, angle=angle, timeout=5))
        self.addSequential(TurnAngle(angle=0, timeout=2.5))
        self.addSequential(DriveStraightCombined(distance=30, angle=0, timeout=5))

class LimeLightAutoAlign(Command):
    def __init__(self, robot):
        super().__init__("StartAutoAlign")
        self.robot = robot

    def initialize(self):
        path = self.robot.limelight.getPath()
        angle = path[0]
        dist1 = path[1]
        dist2 = path[2]
        angle0 = path[3]
        SmartDashboard.putNumber("AutoAlignAngle", angle)
        SmartDashboard.putNumber("AutoAlignDist1", dist1)
        SmartDashboard.putNumber("AutoAlignDist2", dist2)
        SmartDashboard.putNumber("AutoAlignAngle0", angle0)
        aat = AutoAlign(angle, dist1, dist2, angle0)
        aat.start()

    def isFinished(self):
        return True

class TurnAngle(CommandGroup):
    def __init__(self):
        super().__init__('TurnAngle')
        TurnAngle = turnAngle.TurnAngle
        self.addSequential(TurnAngle(angle=0, timeout=3))
