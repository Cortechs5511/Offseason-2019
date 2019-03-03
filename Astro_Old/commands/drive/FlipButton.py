import wpilib
from wpilib.command import Command


class FlipButton(Command):
    def __init__(self):
        super().__init__('Flip')
        robot = self.getRobot()
        self.drive = robot.drive

    def initialize(self):
        if self.drive.flipped: self.drive.flipped = False
        else: self.drive.flipped = True

    def isFinished(self):
        return True
