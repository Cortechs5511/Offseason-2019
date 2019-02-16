import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from commands.climber import liftRobot

class AutoClimb(TimedCommand):

    def __init__(self):
        super().__init__('AutoClimb')
        self.frontSensor = #switch syntax
        self.backSensor = #switch syntax
        self.frontEncoder = #encoder syntax
        self.backEncoder = #encoder syntax
        self.requires(self.getRobot().drive)
        self.requires(self.getRobot().climber)
        self.climber = self.getRobot().climber
        self.DT = self.getRobot().drive
        self.LiftRobot = commands.climber.liftRobot.LiftRobot

    def initialize(self):
        pass

    def execute(self):
        while not self.climber.isFullyExtendedFront():
            self.LiftRobot('both')
        while not forwardSensor:
            self.LiftRobot('')
    def isFinished(self):
        pass
        
    def interrupted(self):
        self.end()

    def end(self):
        pass
