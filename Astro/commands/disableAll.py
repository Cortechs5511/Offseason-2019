import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from commands.cargo.wristintake import 
class AutoClimb(TimedCommand):

    def __init__(self):
        super().__init__('AutoClimb')

        self.requires(self.getRobot().drive)
        self.requires(self.getRobot().climber)
        self.climber = self.getRobot().climber
        self.DT = self.getRobot().drive



    def initialize(self):

    def execute(self):
       
    def isFinished(self):

    def interrupted(self):
        self.end()

    def end(self):
