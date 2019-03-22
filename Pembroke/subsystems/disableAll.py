import wpilib
from wpilib.command import Command
import subsystems
from subsystems import CargoMech, Climber, Drive, HatchMech, Limelight

class DisableAll(Command):

    def __init__(self):
        super().__init__('Disable All')
        self.robot = self.getRobot()
        self.requires(self.robot.cargo)
        self.requires(self.robot.climber)
        self.requires(self.robot.drive)
        self.requires(self.robot.hatch)

        self.cargo = self.robot.cargo
        self.climber = self.robot.climber
        self.drive = self.robot.drive
        self.hatch = self.robot.hatch

    def initialize(self):
        pass

    def execute(self):
        self.robot.scheduler.removeAll()
        self.cargo.disable()
        self.climber.disable()
        self.drive.disable()
        self.hatch.disable()

    def isFinished(self):
        return True
