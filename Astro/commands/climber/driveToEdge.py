import wpilib
from wpilib.command import Command
from commands.climber import setSpeedWheel

class DriveToEdge(Command):
    def __init__(self, Mode):
        super().__init__('DriveToEdge')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.mode = Mode

    def initialize(self):
        pass

    def execute(self):
        if self.mode == "front":
            self.climber.wheelForward()
        elif self.mode == "back":
            self.climber.wheelForward()

    def interrupted(self):
        self.end()

    def end(self):
        self.climber.stopDrive()

    def isFinished(self):
        if self.mode == "front" and self.climber.isFrontOverGround():
            return True
        elif self.mode == "back" and self.climber.isBackOverGround():
            return True

        return False
