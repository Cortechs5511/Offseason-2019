import wpilib
from wpilib.command import Command
import subsystems
from subsystems import CargoMech, Climber, Drive, HatchMech, Limelight
'''
from commands.cargo.wristIntake.py import wristIntake
from commands.cargo.wristMove.py import WristMove
from commands.climber.autoClimb.py import autoClimb
from commands.climber.liftRobot.py import liftRobot
from commands.climber.lowerRobot.py import LowerRobot
from commands.climber.setSpeedWheel.py import setSpeedWheel
from commands.drive.align.py import Align
from commands.drive.bump.py import Bump
from commands.drive.diffDrive.py import DiffDrive
from commands.drive.drivePath.py import drivePath
from commands.drive.driveStraightCombined.py import driveStraightCombined
from commands.drive.driveStraightDistance.py import driveStraightDistance
from commands.drive.driveStraightTime.py import driveStraightTime
from commands.drive.driveVision.py import DriveVision
from commands.drive.FlipButton.py import FlipButton
from commands.drive.measured.py import Measured
from commands.drive.relativeTurn.py import RelativeTurn
from commands.drive.rotateAuton.py import RotateAuton
from commands.drive.setSpeedDT.py import SetSpeedDT
from commands.drive.turnAngle.py import TurnAngle
from commands.hatch.ejectHatch.py import EjectHatch
from commands.hatch.ejectToggle.py import EjectToggle
from commands.hatch.joystickPiston.py import JoystickPiston
from commands.hatch.slideToggle.py import SlideToggle
'''

class DisableAll(Command):

    def __init__(self):
        super().__init__('Disable All')
        self.robot = self.getRobot()
        self.requires(self.robot.CargoMech)
        self.requires(self.robot.Climber)
        self.requires(self.robot.Drive)
        self.requires(self.robot.HatchMech)

        self.CargoMech = subsystems.CargoMech 
        self.Climber = subsystems.Climber 
        self.Drive = subsystems.Drive 
        self.HatchMech = subsystems.HatchMech 

    def initialize(self):
        pass

    def execute(self):

        self.CargoMech.stop()
        self.Climber.stop()
        self.Drive.stop()
        self.HatchMech.stop()

    
    def isFinished(self):
        return True