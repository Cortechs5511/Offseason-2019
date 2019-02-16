import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand

class AutoClimb(TimedCommand):

    def __init__(self):
        super().__init__('AutoClimb')

        self.requires(self.getRobot().drive)
        self.requires(self.getRobot().climber)
        self.climber = self.getRobot().climber
        self.DT = self.getRobot().drive



    def initialize(self):

    def execute(self):
        self.climber.lift(0.9)
        self.climber.wheelForward()
        self.climber.lift(-0.4)
        self.climber.liftFront(-0.9)

    def isFinished(self):

    def interrupted(self):
        self.end()

    def end(self):
